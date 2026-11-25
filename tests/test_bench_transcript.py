import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.bench_transcript import (
    analyze_transcript,
    format_comparison_report,
    format_single_report,
)


class BenchTranscriptTests(unittest.TestCase):
    def _write_jsonl(self, directory, name, lines):
        path = Path(directory) / name
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def test_single_transcript_with_tokens_and_tools(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_jsonl(
                directory,
                "session.jsonl",
                [
                    json.dumps({"role": "user", "content": "Audite o repo"}),
                    json.dumps({
                        "role": "model",
                        "toolCalls": [
                            {"name": "grep_search"},
                            {"name": "view_file"},
                            {"name": "view_file"},
                        ],
                        "usageMetadata": {
                            "promptTokenCount": 1200,
                            "candidatesTokenCount": 300,
                            "cachedContentTokenCount": 800,
                        },
                    }),
                    "{malformed line",
                ],
            )
            summary = analyze_transcript(path)
            self.assertEqual(2, summary["events"])
            self.assertEqual(1, summary["malformed_lines"])
            self.assertEqual(2, summary["turns"])
            self.assertEqual(3, summary["tool_calls"])
            self.assertEqual({"view_file": 2, "grep_search": 1}, summary["tools"])
            self.assertEqual(1200, summary["tokens"]["input"])
            self.assertEqual(300, summary["tokens"]["output"])
            self.assertEqual(800, summary["tokens"]["cached"])
            self.assertEqual(1500, summary["tokens"]["total"])

            report = format_single_report(summary)
            self.assertIn("view_file: 2", report)
            self.assertIn("entrada=1200", report)

    def test_missing_tokens_reported_as_not_measured(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self._write_jsonl(
                directory,
                "no_tokens.jsonl",
                [
                    json.dumps({"role": "user"}),
                    json.dumps({"type": "tool_call", "name": "run_command"}),
                ],
            )
            summary = analyze_transcript(path)
            self.assertIsNone(summary["tokens"]["input"])
            self.assertIsNone(summary["tokens"]["total"])
            report = format_single_report(summary)
            self.assertIn("não medidos", report)

    def test_before_after_comparison_and_cli_flags(self):
        repo_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as directory:
            before = self._write_jsonl(
                directory,
                "before.jsonl",
                [
                    json.dumps({"role": "user"}),
                    json.dumps({"role": "model", "toolCall": {"name": "view_file"}, "usage": {"inputTokens": 2000, "outputTokens": 400}}),
                    json.dumps({"role": "model", "toolCall": {"name": "view_file"}, "usage": {"inputTokens": 1000, "outputTokens": 200}}),
                ],
            )
            after = self._write_jsonl(
                directory,
                "after.jsonl",
                [
                    json.dumps({"role": "user"}),
                    json.dumps({"role": "model", "toolCall": {"name": "view_file"}, "usage": {"inputTokens": 1500, "outputTokens": 300}}),
                ],
            )
            comp = format_comparison_report(analyze_transcript(before), analyze_transcript(after))
            self.assertIn("Tokens entrada", comp)
            self.assertIn("-1500 (-50.0%)", comp)

            cli = subprocess.run(
                [sys.executable, "scripts/bench_transcript.py", "--before", str(before), "--after", str(after), "--json"],
                capture_output=True,
                text=True,
                cwd=str(repo_root),
                check=False,
            )
            self.assertEqual(0, cli.returncode)
            payload = json.loads(cli.stdout)
            self.assertEqual(2, payload["before"]["tool_calls"])
            self.assertEqual(1, payload["after"]["tool_calls"])

            help_res = subprocess.run(
                [sys.executable, "scripts/bench_transcript.py", "--help"],
                capture_output=True,
                text=True,
                cwd=str(repo_root),
                check=False,
            )
            self.assertEqual(0, help_res.returncode)
            self.assertIn("--before", help_res.stdout)


if __name__ == "__main__":
    unittest.main()
