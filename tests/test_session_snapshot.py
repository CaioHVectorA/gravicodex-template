import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.session_snapshot import (
    MAX_MESSAGE_BYTES,
    build_snapshot_message,
    detect_mode,
    run_hook,
)


class SessionSnapshotTests(unittest.TestCase):
    def test_template_and_product_mode_detection(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            proj = root / "docs" / "context" / "project.md"
            proj.parent.mkdir(parents=True)

            proj.write_text("# Projeto\n\n## Ao criar um produto\nTexto.\n", encoding="utf-8")
            self.assertEqual("TEMPLATE", detect_mode(root))

            proj.write_text("# Projeto Real\n\nAPI de pedidos em produção.\n", encoding="utf-8")
            self.assertEqual("PRODUTO", detect_mode(root))

    def test_valid_session_start_payload_and_byte_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs" / "context").mkdir(parents=True)
            (root / "docs" / "context" / "project.md").write_text(
                "# Projeto\n\n## Ao criar um produto\n", encoding="utf-8"
            )
            (root / "docs" / "context" / "commands.md").write_text(
                "| Intenção | Comando | Quando |\n| --- | --- | --- |\n"
                "| Testar | `python3 -m unittest` | Sempre |\n",
                encoding="utf-8",
            )
            (root / "node_modules" / "pkg").mkdir(parents=True)
            (root / "node_modules" / "pkg" / "index.js").write_text("x", encoding="utf-8")
            (root / "AGENTS.md").write_text("# Acordo\n", encoding="utf-8")

            stdin_payload = json.dumps({
                "conversationId": "test-uuid",
                "workspacePaths": [str(root)],
                "modelName": "gemini-3.6-flash-medium",
            })
            out = run_hook(stdin_payload)
            self.assertIn("injectSteps", out)
            msg = out["injectSteps"][0]["systemMessage"]["systemMessage"]
            self.assertIn("Modo: TEMPLATE", msg)
            self.assertIn("python3 -m unittest", msg)
            self.assertNotIn("node_modules", msg)
            self.assertLessEqual(len(msg.encode("utf-8")), MAX_MESSAGE_BYTES)

    def test_snapshot_truncates_safely_within_1500_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for idx in range(30):
                d = root / f"pasta_muito_longa_com_acento_ação_{idx:02d}"
                d.mkdir()
                for child in range(15):
                    (d / f"arquivo_extenso_descrição_{child:02d}.md").write_text("x", encoding="utf-8")
            msg = build_snapshot_message(root)
            encoded = msg.encode("utf-8")
            self.assertLessEqual(len(encoded), MAX_MESSAGE_BYTES)
            # Ensure valid UTF-8 round-trip
            self.assertEqual(msg, encoded.decode("utf-8"))

    def test_fail_open_on_invalid_json_or_missing_workspace(self):
        self.assertEqual({}, run_hook("{invalid json"))
        self.assertEqual({}, run_hook("[]"))
        self.assertEqual({}, run_hook("", workspace_override=Path("/nonexistent/path/xyz")))

    def test_cli_stdin_and_help(self):
        repo_root = Path(__file__).resolve().parents[1]
        payload = json.dumps({"workspacePaths": [str(repo_root)]})
        completed = subprocess.run(
            [sys.executable, "scripts/session_snapshot.py"],
            input=payload,
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            check=False,
        )
        self.assertEqual(0, completed.returncode)
        parsed = json.loads(completed.stdout)
        msg = parsed["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("Modo: TEMPLATE", msg)
        self.assertLessEqual(len(msg.encode("utf-8")), MAX_MESSAGE_BYTES)

        help_res = subprocess.run(
            [sys.executable, "scripts/session_snapshot.py", "--help"],
            capture_output=True,
            text=True,
            cwd=str(repo_root),
            check=False,
        )
        self.assertEqual(0, help_res.returncode)
        self.assertIn("--workspace", help_res.stdout)


if __name__ == "__main__":
    unittest.main()
