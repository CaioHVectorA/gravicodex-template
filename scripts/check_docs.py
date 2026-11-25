"""Check Markdown docs and Antigravity customizations using Python stdlib."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


LIMITS = {"AGENTS.md": 3 * 1024, "docs/INDEX.md": 4 * 1024}
STARTER_LIMIT = 16 * 1024
RULE_LIMIT = 24_000
DEFAULT_LIMIT = 8 * 1024
IGNORED = {".git", ".venv", "node_modules", "vendor", "__pycache__", "dist", "build"}

VALID_RULE_TRIGGERS = {"always_on", "model_decision", "glob", "manual"}
LIFECYCLE_HOOK_EVENTS = {"SessionStart", "PreInvocation", "PostInvocation", "Stop"}
TOOL_HOOK_EVENTS = {"PreToolUse", "PostToolUse"}
SUPPORTED_HOOK_EVENTS = LIFECYCLE_HOOK_EVENTS | TOOL_HOOK_EVENTS

LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\s]+)\)")
HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
YAML_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$")


def slug(title):
    title = re.sub(r"\s+#+\s*$", "", title)
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", title.lower()))


def _strip_yaml_comment(value):
    in_single = False
    in_double = False
    for idx, ch in enumerate(value):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            if idx == 0 or value[idx - 1].isspace():
                return value[:idx].rstrip()
    return value.strip()


def _parse_yaml_scalar(raw):
    value = _strip_yaml_comment(raw).strip()
    if not value:
        return ""
    if (len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}):
        return value[1:-1]
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_yaml_scalar(part) for part in inner.split(",")]
    return value


def parse_frontmatter(text):
    """Parse a simple YAML frontmatter block at the start of a Markdown file.

    Returns (data_or_none, body_start_line_1based, error_or_none).
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 1, None

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() in {"---", "..."}:
            end_idx = idx
            break
    if end_idx is None:
        return None, 1, "frontmatter YAML sem delimitador de fechamento '---'"

    data = {}
    current_list_key = None
    for offset, line in enumerate(lines[1:end_idx], 2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            if current_list_key is None:
                return None, end_idx + 2, f"frontmatter linha {offset}: item de lista sem chave"
            data[current_list_key].append(_parse_yaml_scalar(stripped[2:]))
            continue
        match = YAML_KEY.match(line)
        if not match:
            if line.startswith((" ", "\t")) and current_list_key is not None:
                continue
            return None, end_idx + 2, f"frontmatter linha {offset}: sintaxe YAML inválida"
        key, raw_val = match.group(1), match.group(2)
        cleaned = _strip_yaml_comment(raw_val)
        if cleaned == "":
            data[key] = []
            current_list_key = key
        else:
            data[key] = _parse_yaml_scalar(cleaned)
            current_list_key = None

    return data, end_idx + 2, None


def scan(text):
    """Return headings, literal inline links and unclosed-fence location."""
    _, start_line, _ = parse_frontmatter(text)
    headings, links = [], []
    opened = None
    lines = text.splitlines()
    for number, line in enumerate(lines[start_line - 1:], start_line):
        fence = FENCE.match(line)
        if opened:
            if (fence and fence[1][0] == opened[0]
                    and len(fence[1]) >= opened[1] and not fence[2].strip()):
                opened = None
            continue
        if fence:
            opened = (fence[1][0], len(fence[1]), number)
            continue
        heading = HEADING.match(line)
        if heading:
            headings.append(slug(heading[1]))
        prose = re.sub(r"(`+).*?\1", "", line)
        links.extend((number, match[1].strip("<>")) for match in LINK.finditer(prose))
    return headings, links, opened[2] if opened else None


def size_limit_for(name):
    if name in LIMITS:
        return LIMITS[name]
    if name.startswith("docs/starters/"):
        return STARTER_LIMIT
    if name.startswith(".agents/rules/"):
        return RULE_LIMIT
    return DEFAULT_LIMIT


def _non_empty_text(value):
    return isinstance(value, str) and bool(value.strip())


def _non_empty_globs(value):
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return any(isinstance(item, str) and item.strip() for item in value)
    return False


def validate_antigravity_markdown(name, raw_size, frontmatter, fm_error):
    """Validate Antigravity YAML frontmatter contracts for rules, skills and agents."""
    errors = []
    parts = name.split("/")

    # .agents/rules/*.md
    if len(parts) >= 3 and parts[0] == ".agents" and parts[1] == "rules":
        if len(parts) > 3:
            errors.append(
                f"{name}: regra em subpasta de .agents/rules/ é ignorada sem .agents/rules.json"
            )
            return errors
        if raw_size > RULE_LIMIT:
            errors.append(
                f"{name}: {raw_size} bytes excedem o limite oficial do Antigravity de {RULE_LIMIT} bytes"
            )
        if fm_error:
            errors.append(f"{name}: {fm_error}")
            return errors
        if not isinstance(frontmatter, dict):
            errors.append(
                f"{name}: regra em .agents/rules/ exige frontmatter YAML com trigger válido"
            )
            return errors
        trigger = frontmatter.get("trigger")
        if not isinstance(trigger, str) or trigger not in VALID_RULE_TRIGGERS:
            allowed = ", ".join(sorted(VALID_RULE_TRIGGERS))
            errors.append(
                f"{name}: trigger inválido ({trigger!r}); valores aceitos: {allowed}"
            )
        elif trigger == "model_decision" and not _non_empty_text(frontmatter.get("description")):
            errors.append(
                f"{name}: trigger 'model_decision' exige campo 'description' não vazio"
            )
        elif trigger == "glob":
            globs = frontmatter.get("globs", frontmatter.get("glob"))
            if not _non_empty_globs(globs):
                errors.append(
                    f"{name}: trigger 'glob' exige campo 'globs' ou 'glob' não vazio"
                )
        return errors

    # .agents/skills/<name>/SKILL.md
    if len(parts) == 4 and parts[0] == ".agents" and parts[1] == "skills" and parts[3] == "SKILL.md":
        if fm_error:
            errors.append(f"{name}: {fm_error}")
            return errors
        if not isinstance(frontmatter, dict):
            errors.append(f"{name}: skill exige frontmatter YAML com campo 'description'")
            return errors
        if not _non_empty_text(frontmatter.get("description")):
            errors.append(f"{name}: skill exige campo 'description' não vazio")
        return errors

    # .agents/agents/<name>.md or .agents/agents/<name>/agent.md
    is_agent_file = (
        (len(parts) == 3 and parts[0] == ".agents" and parts[1] == "agents")
        or (len(parts) == 4 and parts[0] == ".agents" and parts[1] == "agents" and parts[3] == "agent.md")
    )
    if is_agent_file:
        if fm_error:
            errors.append(f"{name}: {fm_error}")
            return errors
        if not isinstance(frontmatter, dict):
            errors.append(f"{name}: subagente exige frontmatter YAML com 'name' e 'description'")
            return errors
        if not _non_empty_text(frontmatter.get("name")):
            errors.append(f"{name}: subagente exige campo 'name' não vazio")
        if not _non_empty_text(frontmatter.get("description")):
            errors.append(f"{name}: subagente exige campo 'description' não vazio")
        return errors

    return errors


def _validate_handler(location, handler):
    errors = []
    if not isinstance(handler, dict):
        return [f"{location}: handler deve ser um objeto JSON"]
    handler_type = handler.get("type", "command")
    if handler_type != "command":
        errors.append(f"{location}: type inválido ({handler_type!r}); apenas 'command' é suportado")
    if not _non_empty_text(handler.get("command")):
        errors.append(f"{location}: handler exige 'command' string não vazia")
    if "timeout" in handler:
        timeout = handler["timeout"]
        if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
            errors.append(f"{location}: 'timeout' deve ser número positivo em segundos")
    return errors


def validate_hooks_json(root):
    """Validate .agents/hooks.json schema and supported Antigravity hook events."""
    hooks_path = root / ".agents" / "hooks.json"
    if not hooks_path.exists():
        return []
    name = ".agents/hooks.json"
    try:
        data = json.loads(hooks_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"{name}: JSON inválido: {exc}"]

    if not isinstance(data, dict):
        return [f"{name}: raiz deve ser um objeto mapeando nomes de hooks"]

    errors = []
    allowed_keys = SUPPORTED_HOOK_EVENTS | {"enabled"}
    for hook_name, config in data.items():
        if not isinstance(hook_name, str) or not hook_name.strip():
            errors.append(f"{name}: nome de hook vazio")
            continue
        if not isinstance(config, dict):
            errors.append(f"{name}:{hook_name}: configuração do hook deve ser um objeto")
            continue
        unknown = sorted(set(config.keys()) - allowed_keys)
        if unknown:
            errors.append(
                f"{name}:{hook_name}: evento/campo não suportado: {', '.join(unknown)}"
            )
        if "enabled" in config and not isinstance(config["enabled"], bool):
            errors.append(f"{name}:{hook_name}: 'enabled' deve ser booleano")

        events_found = [key for key in config if key in SUPPORTED_HOOK_EVENTS]
        if not events_found:
            errors.append(f"{name}:{hook_name}: nenhum evento suportado configurado")

        for event in events_found:
            entries = config[event]
            if not isinstance(entries, list):
                errors.append(f"{name}:{hook_name}.{event}: deve ser uma lista")
                continue
            if event in LIFECYCLE_HOOK_EVENTS:
                for idx, handler in enumerate(entries):
                    errors.extend(
                        _validate_handler(f"{name}:{hook_name}.{event}[{idx}]", handler)
                    )
            else:
                for idx, group in enumerate(entries):
                    loc = f"{name}:{hook_name}.{event}[{idx}]"
                    if not isinstance(group, dict):
                        errors.append(f"{loc}: grupo de matcher deve ser um objeto")
                        continue
                    if "matcher" in group and not isinstance(group["matcher"], str):
                        errors.append(f"{loc}: 'matcher' deve ser string")
                    group_hooks = group.get("hooks")
                    if not isinstance(group_hooks, list) or not group_hooks:
                        errors.append(f"{loc}: exige lista não vazia 'hooks'")
                        continue
                    for h_idx, handler in enumerate(group_hooks):
                        errors.extend(_validate_handler(f"{loc}.hooks[{h_idx}]", handler))
    return errors


def audit(root):
    root = Path(root).resolve()
    documents, errors, metrics = {}, [], []

    legacy_workflows = root / ".agents" / "workflows"
    if legacy_workflows.is_dir() and any(legacy_workflows.iterdir()):
        errors.append(
            ".agents/workflows/: diretório legado descontinuado no Antigravity; migre para .agents/skills/"
        )

    for path in sorted(root.rglob("*.md")):
        if IGNORED.intersection(path.relative_to(root).parts):
            continue
        name = path.relative_to(root).as_posix()
        if not path.resolve().is_relative_to(root):
            errors.append(f"{name}: arquivo fora da raiz")
            continue
        try:
            raw = path.read_bytes()
            text = raw.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{name}: leitura UTF-8 falhou: {exc}")
            continue
        metrics.append((name, len(raw), len(text.split())))
        limit = size_limit_for(name)
        if len(raw) > limit:
            errors.append(f"{name}: {len(raw)} bytes excedem o limite de {limit}")

        frontmatter, _, fm_error = parse_frontmatter(text)
        errors.extend(validate_antigravity_markdown(name, len(raw), frontmatter, fm_error))

        headings, links, fence = scan(text)
        if fence:
            errors.append(f"{name}:{fence}: cerca de código não fechada")
        if len(headings) != len(set(headings)):
            errors.append(f"{name}: títulos com âncoras duplicadas")
        documents[path.resolve()] = (set(headings), links)

    for path, (_, links) in documents.items():
        name = path.relative_to(root).as_posix()
        for number, target in links:
            location = f"{name}:{number}"
            try:
                url = urlsplit(target)
            except ValueError:
                errors.append(f"{location}: link inválido: {target}")
                continue
            if url.scheme or url.netloc:
                continue
            destination = (path.parent / unquote(url.path)).resolve() if url.path else path
            if not destination.is_relative_to(root):
                errors.append(f"{location}: link fora da raiz: {target}")
            elif not destination.exists():
                errors.append(f"{location}: destino inexistente: {target}")
            elif url.fragment and destination.suffix == ".md":
                anchors = documents.get(destination, (set(), []))[0]
                if unquote(url.fragment) not in anchors:
                    errors.append(f"{location}: âncora inexistente: {target}")

    errors.extend(validate_hooks_json(root))
    return metrics, errors


def build_parser():
    parser = argparse.ArgumentParser(
        prog="check_docs.py",
        description=(
            "Valida integridade de Markdown (links locais, âncoras, cercas e limites em bytes) "
            "e customizações nativas do Google Antigravity (.agents/rules, skills, agents e hooks.json)."
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Raiz do repositório a auditar (padrão: raiz deste repositório).",
    )
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    metrics, errors = audit(args.root)
    for name, size, words in metrics:
        print(f"{size:5} bytes  {words:4} palavras  {name}")
    total = sum(size for _, size, _ in metrics)
    entry = sum(size for name, size, _ in metrics if name == "AGENTS.md")
    index = sum(size for name, size, _ in metrics if name == "docs/INDEX.md")
    starters = sum(size for name, size, _ in metrics if name.startswith("docs/starters/"))
    print(f"\n{len(metrics)} documentos; {total} bytes no acervo Markdown.")
    print(
        f"Entrada: {entry} bytes; índice opcional: {index} bytes; "
        f"starters descartáveis: {starters} bytes. Tokens não medidos."
    )
    if errors:
        print("\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print("OK: Markdown, limites e customizações Antigravity válidos no perfil documentado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
