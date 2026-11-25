"""Offline summary and comparison tool for Antigravity transcript.jsonl logs."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys


INPUT_TOKEN_KEYS = ("inputTokens", "promptTokens", "promptTokenCount", "input_tokens", "prompt_tokens")
OUTPUT_TOKEN_KEYS = (
    "outputTokens",
    "completionTokens",
    "candidatesTokenCount",
    "output_tokens",
    "completion_tokens",
)
CACHED_TOKEN_KEYS = (
    "cachedTokens",
    "cachedContentTokenCount",
    "cacheReadInputTokens",
    "cache_read_input_tokens",
    "cached_tokens",
)
TOTAL_TOKEN_KEYS = ("totalTokens", "totalTokenCount", "total_tokens")
USAGE_CONTAINERS = ("usage", "usageMetadata", "tokenUsage", "metrics", "metadata")


def _extract_int(mapping, keys):
    for key in keys:
        value = mapping.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    return None


def _collect_usage(obj, totals):
    if not isinstance(obj, dict):
        return
    for bucket, keys in (
        ("input", INPUT_TOKEN_KEYS),
        ("output", OUTPUT_TOKEN_KEYS),
        ("cached", CACHED_TOKEN_KEYS),
        ("total", TOTAL_TOKEN_KEYS),
    ):
        found = _extract_int(obj, keys)
        if found is not None:
            totals[bucket] = (totals[bucket] or 0) + found

    for container_key in USAGE_CONTAINERS:
        nested = obj.get(container_key)
        if isinstance(nested, dict):
            _collect_usage(nested, totals)


def _extract_tool_names(obj):
    names = []
    if not isinstance(obj, dict):
        return names

    # Single tool call fields
    for key in ("toolCall", "tool_call", "functionCall", "function_call"):
        val = obj.get(key)
        if isinstance(val, dict):
            tool_name = val.get("name") or val.get("toolName") or val.get("tool")
            if isinstance(tool_name, str) and tool_name.strip():
                names.append(tool_name.strip())

    # Plural tool calls lists
    for key in ("toolCalls", "tool_calls", "functionCalls", "function_calls"):
        val = obj.get(key)
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict):
                    fn = item.get("function") if isinstance(item.get("function"), dict) else item
                    tool_name = fn.get("name") or fn.get("toolName") or fn.get("tool")
                    if isinstance(tool_name, str) and tool_name.strip():
                        names.append(tool_name.strip())

    # Direct tool event entries
    entry_type = str(obj.get("type", "")).lower()
    if entry_type in {"tool_call", "tool_use", "function_call"}:
        tool_name = obj.get("name") or obj.get("toolName") or obj.get("tool")
        if isinstance(tool_name, str) and tool_name.strip():
            names.append(tool_name.strip())

    # Common nested wrappers (step, message, content, parts)
    for nested_key in ("step", "message", "data", "payload"):
        nested = obj.get(nested_key)
        if isinstance(nested, dict):
            names.extend(_extract_tool_names(nested))
    for list_key in ("content", "parts"):
        items = obj.get(list_key)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    names.extend(_extract_tool_names(item))
    return names


def _is_turn_record(obj):
    if not isinstance(obj, dict):
        return False
    role = str(obj.get("role", "")).lower()
    if role in {"user", "model", "assistant"}:
        return True
    entry_type = str(obj.get("type", "")).lower()
    if entry_type in {"turn", "user_message", "model_response", "assistant_message", "invocation"}:
        return True
    if "invocationNum" in obj or "turn" in obj:
        return True
    msg = obj.get("message")
    if isinstance(msg, dict) and str(msg.get("role", "")).lower() in {"user", "model", "assistant"}:
        return True
    return False


def analyze_transcript(path):
    path = Path(path)
    events = 0
    malformed = 0
    turns = 0
    tools = Counter()
    tokens = {"input": None, "output": None, "cached": None, "total": None}

    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                malformed += 1
                continue
            if not isinstance(record, dict):
                malformed += 1
                continue
            events += 1
            if _is_turn_record(record):
                turns += 1
            for tool_name in _extract_tool_names(record):
                tools[tool_name] += 1
            _collect_usage(record, tokens)

    if tokens["total"] is None and (tokens["input"] is not None or tokens["output"] is not None):
        tokens["total"] = (tokens["input"] or 0) + (tokens["output"] or 0)

    return {
        "file": str(path),
        "events": events,
        "malformed_lines": malformed,
        "turns": turns,
        "tool_calls": sum(tools.values()),
        "tools": dict(tools.most_common()),
        "tokens": tokens,
    }


def _fmt_token(value):
    return "não medidos" if value is None else str(value)


def _fmt_delta(before_val, after_val):
    if before_val is None or after_val is None:
        return "não medidos"
    diff = after_val - before_val
    sign = "+" if diff > 0 else ""
    if before_val > 0:
        pct = (diff / before_val) * 100.0
        return f"{sign}{diff} ({sign}{pct:.1f}%)"
    return f"{sign}{diff}"


def format_single_report(summary):
    tokens = summary["tokens"]
    lines = [
        f"Arquivo: {summary['file']}",
        f"Eventos válidos: {summary['events']} (linhas inválidas: {summary['malformed_lines']})",
        f"Turnos detectados: {summary['turns']}",
        f"Chamadas de ferramenta: {summary['tool_calls']}",
        (
            "Tokens: "
            f"entrada={_fmt_token(tokens['input'])}, "
            f"saída={_fmt_token(tokens['output'])}, "
            f"cache={_fmt_token(tokens['cached'])}, "
            f"total={_fmt_token(tokens['total'])}"
        ),
    ]
    if summary["tools"]:
        lines.append("Distribuição por ferramenta:")
        for name, count in summary["tools"].items():
            lines.append(f"  - {name}: {count}")
    else:
        lines.append("Distribuição por ferramenta: nenhuma chamada detectada")
    return "\n".join(lines)


def format_comparison_report(before, after):
    rows = [
        ("Eventos válidos", str(before["events"]), str(after["events"]), _fmt_delta(before["events"], after["events"])),
        ("Turnos detectados", str(before["turns"]), str(after["turns"]), _fmt_delta(before["turns"], after["turns"])),
        (
            "Chamadas de ferramenta",
            str(before["tool_calls"]),
            str(after["tool_calls"]),
            _fmt_delta(before["tool_calls"], after["tool_calls"]),
        ),
        (
            "Tokens entrada",
            _fmt_token(before["tokens"]["input"]),
            _fmt_token(after["tokens"]["input"]),
            _fmt_delta(before["tokens"]["input"], after["tokens"]["input"]),
        ),
        (
            "Tokens saída",
            _fmt_token(before["tokens"]["output"]),
            _fmt_token(after["tokens"]["output"]),
            _fmt_delta(before["tokens"]["output"], after["tokens"]["output"]),
        ),
        (
            "Tokens cache",
            _fmt_token(before["tokens"]["cached"]),
            _fmt_token(after["tokens"]["cached"]),
            _fmt_delta(before["tokens"]["cached"], after["tokens"]["cached"]),
        ),
        (
            "Tokens total",
            _fmt_token(before["tokens"]["total"]),
            _fmt_token(after["tokens"]["total"]),
            _fmt_delta(before["tokens"]["total"], after["tokens"]["total"]),
        ),
    ]
    lines = [
        f"Antes:  {before['file']}",
        f"Depois: {after['file']}",
        "",
        "| Métrica | Antes | Depois | Delta |",
        "| --- | --- | --- | --- |",
    ]
    for label, b_val, a_val, delta in rows:
        lines.append(f"| {label} | {b_val} | {a_val} | {delta} |")

    all_tools = sorted(set(before["tools"]) | set(after["tools"]))
    if all_tools:
        lines.append("")
        lines.append("Ferramentas (antes -> depois):")
        for tool in all_tools:
            b_cnt = before["tools"].get(tool, 0)
            a_cnt = after["tools"].get(tool, 0)
            lines.append(f"  - {tool}: {b_cnt} -> {a_cnt} ({_fmt_delta(b_cnt, a_cnt)})")
    return "\n".join(lines)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="bench_transcript.py",
        description=(
            "Resume e compara métricas objetivas de arquivos transcript.jsonl do Antigravity "
            "(turnos, chamadas de ferramenta e tokens quando presentes no log)."
        ),
    )
    parser.add_argument(
        "transcript",
        nargs="?",
        type=Path,
        help="Caminho para um único arquivo transcript.jsonl.",
    )
    parser.add_argument("--before", type=Path, help="Transcript de referência (baseline).")
    parser.add_argument("--after", type=Path, help="Transcript pós-mudança para comparação.")
    parser.add_argument("--json", action="store_true", help="Emite saída estruturada em JSON.")
    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.before or args.after:
        if not (args.before and args.after):
            parser.error("Use --before e --after juntos para comparação.")
        if args.transcript:
            parser.error("Não combine argumento posicional com --before/--after.")
        for candidate in (args.before, args.after):
            if not candidate.is_file():
                print(f"Erro: arquivo não encontrado: {candidate}", file=sys.stderr)
                return 1
        before_data = analyze_transcript(args.before)
        after_data = analyze_transcript(args.after)
        if args.json:
            print(json.dumps({"before": before_data, "after": after_data}, ensure_ascii=False, indent=2))
        else:
            print(format_comparison_report(before_data, after_data))
        return 0

    if not args.transcript:
        parser.error("Informe um arquivo transcript.jsonl ou o par --before e --after.")
    if not args.transcript.is_file():
        print(f"Erro: arquivo não encontrado: {args.transcript}", file=sys.stderr)
        return 1

    data = analyze_transcript(args.transcript)
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(format_single_report(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
