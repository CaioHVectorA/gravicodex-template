"""Check the documented Markdown subset without third-party dependencies."""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


LIMITS = {"AGENTS.md": 3 * 1024, "docs/INDEX.md": 4 * 1024}
DEFAULT_LIMIT = 8 * 1024
IGNORED = {".git", ".venv", "node_modules", "vendor", "__pycache__"}
LINK = re.compile(r"!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\s]+)\)")
HEADING = re.compile(r"^ {0,3}#{1,6}\s+(.+?)\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def slug(title):
    title = re.sub(r"\s+#+\s*$", "", title)
    return re.sub(r"\s", "-", re.sub(r"[^\w\s-]", "", title.lower()))


def scan(text):
    """Return headings, literal inline links and unclosed-fence location."""
    headings, links = [], []
    opened = None
    for number, line in enumerate(text.splitlines(), 1):
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


def audit(root):
    root = root.resolve()
    documents, errors, metrics = {}, [], []
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
        limit = LIMITS.get(name, DEFAULT_LIMIT)
        if len(raw) > limit:
            errors.append(f"{name}: {len(raw)} bytes excedem o limite de {limit}")
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
    return metrics, errors


def main():
    root = Path(__file__).resolve().parents[1]
    metrics, errors = audit(root)
    for name, size, words in metrics:
        print(f"{size:5} bytes  {words:4} palavras  {name}")
    total = sum(size for _, size, _ in metrics)
    entry = sum(size for name, size, _ in metrics if name == "AGENTS.md")
    index = sum(size for name, size, _ in metrics if name == "docs/INDEX.md")
    print(f"\n{len(metrics)} documentos; {total} bytes no acervo Markdown.")
    print(f"Entrada: {entry} bytes; índice opcional: {index} bytes. Tokens não medidos.")
    if errors:
        print("\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print("OK: links locais, âncoras, cercas e limites no perfil documentado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
