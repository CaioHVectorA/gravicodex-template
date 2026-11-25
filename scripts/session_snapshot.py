"""Zero-dependency Antigravity SessionStart snapshot hook (fail-open, <= 1.5 KB)."""

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys


MAX_MESSAGE_BYTES = 1500
GIT_TIMEOUT_SECONDS = 1.5
MAX_STATUS_FILES = 6
MAX_TREE_ENTRIES = 16
MAX_CHILDREN_PER_DIR = 8
MAX_COMMANDS = 4

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".next",
    ".nuxt",
    "target",
    "vendor",
    "coverage",
    ".tox",
    ".idea",
}

TEMPLATE_MARKERS = (
    "## ao criar um produto",
    "ainda não há aplicação de produto",
)

CMD_ROW = re.compile(r"^\|\s*[^|]+\|\s*`([^`]+)`\s*\|")


def _run_git(root, args):
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout


def git_summary(root):
    branch = _run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    if branch is None:
        return "indisponível"
    branch = branch.strip() or "HEAD"
    status_out = _run_git(root, ["status", "--porcelain"])
    if status_out is None:
        return f"branch={branch} (status indisponível)"
    lines = [line for line in status_out.splitlines() if line.strip()]
    if not lines:
        return f"branch={branch} | limpo"
    untracked = sum(1 for line in lines if line.startswith("??"))
    modified = len(lines) - untracked
    sample = [line[3:].strip() for line in lines[:MAX_STATUS_FILES]]
    more = f" (+{len(lines) - MAX_STATUS_FILES})" if len(lines) > MAX_STATUS_FILES else ""
    return (
        f"branch={branch} | {len(lines)} alterações "
        f"(mod={modified}, novo={untracked}): {', '.join(sample)}{more}"
    )


def detect_mode(root):
    project_md = root / "docs" / "context" / "project.md"
    if project_md.is_file():
        try:
            text = project_md.read_text(encoding="utf-8", errors="ignore").lower()
        except OSError:
            return "INDETERMINADO"
        if any(marker in text for marker in TEMPLATE_MARKERS):
            return "TEMPLATE"
        return "PRODUTO"
    if (root / "docs" / "starters").is_dir():
        return "TEMPLATE"
    return "PRODUTO"


def compact_tree(root):
    try:
        entries = sorted(
            (p for p in root.iterdir() if p.name not in IGNORED_DIRS),
            key=lambda p: (not p.is_dir(), p.name.lower()),
        )
    except OSError:
        return "indisponível"

    items = []
    for entry in entries[:MAX_TREE_ENTRIES]:
        if entry.is_dir():
            try:
                children = sorted(
                    (c for c in entry.iterdir() if c.name not in IGNORED_DIRS),
                    key=lambda c: (not c.is_dir(), c.name.lower()),
                )
            except OSError:
                items.append(f"{entry.name}/")
                continue
            names = [f"{c.name}/" if c.is_dir() else c.name for c in children[:MAX_CHILDREN_PER_DIR]]
            if len(children) > MAX_CHILDREN_PER_DIR:
                names.append(f"+{len(children) - MAX_CHILDREN_PER_DIR}")
            if names:
                items.append(f"{entry.name}/({', '.join(names)})")
            else:
                items.append(f"{entry.name}/")
        else:
            items.append(entry.name)
    if len(entries) > MAX_TREE_ENTRIES:
        items.append(f"+{len(entries) - MAX_TREE_ENTRIES} itens")
    return "; ".join(items) if items else "(vazio)"


def verified_commands(root):
    commands_md = root / "docs" / "context" / "commands.md"
    if not commands_md.is_file():
        return []
    try:
        lines = commands_md.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []
    found = []
    for line in lines:
        match = CMD_ROW.match(line.strip())
        if match:
            cmd = match.group(1).replace(r"\|", "|").strip()
            if cmd and cmd not in found:
                found.append(cmd)
            if len(found) >= MAX_COMMANDS:
                break
    return found


def truncate_utf8(text, max_bytes=MAX_MESSAGE_BYTES):
    encoded = text.encode("utf-8")
    if len(encoded) <= max_bytes:
        return text
    suffix = "..."
    budget = max(0, max_bytes - len(suffix.encode("utf-8")))
    cut = encoded[:budget]
    while cut:
        try:
            return cut.decode("utf-8").rstrip() + suffix
        except UnicodeDecodeError:
            cut = cut[:-1]
    return suffix[:max_bytes]


def build_snapshot_message(root):
    root = Path(root).resolve()
    mode = detect_mode(root)
    mode_hint = (
        "TEMPLATE (se o usuário pedir criação/POC de projeto, acione /bootstrap-poc antes de codar)"
        if mode == "TEMPLATE"
        else "PRODUTO"
    )
    cmds = verified_commands(root)
    cmds_text = "; ".join(cmds) if cmds else "consulte docs/context/commands.md"
    lines = [
        f"[GraviCodex Snapshot] Modo: {mode_hint}",
        f"Git: {git_summary(root)}",
        f"Árvore (<=2 níveis): {compact_tree(root)}",
        f"Comandos verificados: {cmds_text}",
    ]
    return truncate_utf8("\n".join(lines), MAX_MESSAGE_BYTES)


def build_hook_output(root):
    message = build_snapshot_message(root)
    return {
        "injectSteps": [
            {
                "systemMessage": {
                    "systemMessage": message,
                    "metadata": {"source": "gravicodex-session-snapshot"},
                }
            }
        ]
    }


def resolve_workspace(payload, fallback_root):
    if isinstance(payload, dict):
        paths = payload.get("workspacePaths")
        if isinstance(paths, list):
            for candidate in paths:
                if isinstance(candidate, str) and candidate.strip():
                    path = Path(candidate).expanduser()
                    if path.is_dir():
                        return path
    return fallback_root


def build_parser():
    parser = argparse.ArgumentParser(
        prog="session_snapshot.py",
        description=(
            "Hook SessionStart do Google Antigravity (stdlib, fail-open). "
            "Lê JSON opcional via stdin e emite injectSteps com snapshot compacto (<= 1,5 KB)."
        ),
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Diretório de workspace para gerar o snapshot manualmente.",
    )
    return parser


def run_hook(stdin_text, workspace_override=None, fallback_root=None):
    default_root = fallback_root or Path(__file__).resolve().parents[1]
    payload = None
    if stdin_text and stdin_text.strip():
        try:
            payload = json.loads(stdin_text)
        except json.JSONDecodeError:
            return {}
        if not isinstance(payload, dict):
            return {}

    target = workspace_override if workspace_override is not None else resolve_workspace(payload, default_root)
    if not Path(target).is_dir():
        return {}
    return build_hook_output(target)


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        stdin_text = ""
        if args.workspace is None and not sys.stdin.isatty():
            stdin_text = sys.stdin.read()
        result = run_hook(stdin_text, workspace_override=args.workspace)
    except Exception:
        result = {}
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
