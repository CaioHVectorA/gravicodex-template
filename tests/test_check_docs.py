from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.check_docs import audit, parse_frontmatter, scan


class DocumentationChecks(unittest.TestCase):
    def check_tree(self, files):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, text in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding="utf-8")
            return audit(root)

    def test_valid_relative_links_accents_and_encoded_paths(self):
        _, errors = self.check_tree({
            "README.md": "# Base\n[Guia](docs/guia%20local.md#decisão)\n[Local](#base)",
            "docs/guia local.md": "# Decisão\n[Voltar](../README.md)\n",
        })
        self.assertEqual([], errors)

    def test_missing_file_and_missing_anchor_fail(self):
        _, errors = self.check_tree({
            "README.md": "# Base\n[x](ausente.md)\n[y](#inexistente)\n",
        })
        self.assertEqual(2, len(errors))
        self.assertTrue(any("destino inexistente" in error for error in errors))
        self.assertTrue(any("âncora inexistente" in error for error in errors))

    def test_code_examples_are_not_navigation(self):
        _, errors = self.check_tree({
            "README.md": "# Base\n`[x](ausente.md)`\n```md\n[x](ausente.md)\n```\n",
        })
        self.assertEqual([], errors)

    def test_shorter_fence_does_not_close_block(self):
        _, _, unclosed = scan("# Base\n````md\n```\n")
        self.assertEqual(2, unclosed)
        _, _, closed = scan("~~~~\n```\n~~~~\n")
        self.assertIsNone(closed)

    def test_external_links_are_not_requested_and_spaces_work(self):
        _, errors = self.check_tree({
            "README.md": "# Base\n[x](https://example.invalid/x)\n[y](<com espaço.md>)",
            "com espaço.md": "# Outro\n",
        })
        self.assertEqual([], errors)

    def test_duplicate_heading_and_entry_budget_fail(self):
        _, errors = self.check_tree({
            "AGENTS.md": "# Base\n# Base\n" + "á" * 1600,
        })
        self.assertEqual(2, len(errors))
        self.assertTrue(any("limite" in error for error in errors))
        self.assertTrue(any("duplicadas" in error for error in errors))

    def test_links_cannot_escape_root(self):
        _, errors = self.check_tree({"README.md": "# Base\n[x](../outside.md)"})
        self.assertTrue(any("fora da raiz" in error for error in errors))

    def test_dependency_documentation_is_ignored(self):
        metrics, errors = self.check_tree({
            "README.md": "# Base\n",
            "node_modules/pkg/README.md": "[x](missing.md)",
        })
        self.assertEqual([], errors)
        self.assertEqual(1, len(metrics))

    def test_starters_allow_up_to_16_kib_and_fail_above(self):
        ok_body = "# Starter\n" + ("a" * 10_000)
        _, ok_errors = self.check_tree({"docs/starters/iot.md": ok_body})
        self.assertEqual([], ok_errors)

        too_big = "# Starter\n" + ("a" * 17_000)
        _, big_errors = self.check_tree({"docs/starters/iot.md": too_big})
        self.assertTrue(any("16384" in error for error in big_errors))

    def test_valid_antigravity_rules_skills_agents_and_hooks(self):
        _, errors = self.check_tree({
            ".agents/rules/md.md": (
                "---\n"
                "trigger: glob\n"
                'globs: "*.md, docs/**/*.md"\n'
                'description: "Regras MD"\n'
                "---\n"
                "# MD\n"
            ),
            ".agents/rules/verify.md": (
                "---\n"
                "trigger: model_decision\n"
                'description: "Validar mudanças"\n'
                "---\n"
                "# Verify\n"
            ),
            ".agents/skills/demo/SKILL.md": (
                "---\n"
                "name: demo\n"
                'description: "Skill de teste"\n'
                "---\n"
                "# Demo\n"
            ),
            ".agents/agents/auditor.md": (
                "---\n"
                "name: auditor\n"
                'description: "Auditor read-only"\n'
                "tools:\n"
                "  - view_file\n"
                "  - grep_search\n"
                "subagent: true\n"
                "mainAgent: false\n"
                "model: flash\n"
                "---\n"
                "# System Prompt\n"
            ),
            ".agents/hooks.json": (
                '{"snap": {"enabled": true, "SessionStart": '
                '[{"type": "command", "command": "python3 scripts/session_snapshot.py", "timeout": 5}]}}'
            ),
        })
        self.assertEqual([], errors)

    def test_invalid_rules_frontmatter_triggers_and_24kb_limit(self):
        _, errors = self.check_tree({
            ".agents/rules/no_fm.md": "# Sem frontmatter\n",
            ".agents/rules/bad_trigger.md": "---\ntrigger: alwaysOn\n---\n# Bad\n",
            ".agents/rules/no_desc.md": "---\ntrigger: model_decision\n---\n# No desc\n",
            ".agents/rules/no_globs.md": "---\ntrigger: glob\n---\n# No globs\n",
            ".agents/rules/huge.md": "---\ntrigger: always_on\n---\n# Huge\n" + ("x" * 24_100),
            ".agents/rules/nested/sub.md": "---\ntrigger: always_on\n---\n# Sub\n",
        })
        joined = "\n".join(errors)
        self.assertIn("no_fm.md", joined)
        self.assertIn("trigger inválido", joined)
        self.assertIn("no_desc.md", joined)
        self.assertIn("no_globs.md", joined)
        self.assertIn("24000", joined)
        self.assertIn("sub.md", joined)

    def test_invalid_skill_agent_and_legacy_workflows(self):
        _, errors = self.check_tree({
            ".agents/skills/empty/SKILL.md": "---\nname: empty\n---\n# Empty\n",
            ".agents/agents/bad.md": "---\nname: only-name\n---\n# Bad\n",
            ".agents/workflows/old.md": "# Legacy\n",
        })
        joined = "\n".join(errors)
        self.assertIn("SKILL.md", joined)
        self.assertIn("bad.md", joined)
        self.assertIn(".agents/workflows/", joined)

    def test_invalid_hooks_json_cases(self):
        _, malformed_errors = self.check_tree({".agents/hooks.json": "{not json"})
        self.assertTrue(any("JSON inválido" in e for e in malformed_errors))

        _, bad_event_errors = self.check_tree({
            ".agents/hooks.json": '{"x": {"UnknownEvent": [{"command": "echo hi"}]}}'
        })
        self.assertTrue(any("não suportado" in e for e in bad_event_errors))

        _, bad_tool_shape = self.check_tree({
            ".agents/hooks.json": '{"x": {"PreToolUse": [{"command": "echo hi"}]}}'
        })
        self.assertTrue(any("hooks" in e for e in bad_tool_shape))

    def test_parse_frontmatter_handles_lists_and_unclosed(self):
        fm, start, err = parse_frontmatter("---\nname: a\ntools:\n  - view_file\n---\n# Title\n")
        self.assertIsNone(err)
        self.assertEqual(6, start)
        self.assertEqual(["view_file"], fm["tools"])

        _, _, unclosed_err = parse_frontmatter("---\nname: a\n# no close")
        self.assertIsNotNone(unclosed_err)

    def test_cli_help_flag(self):
        completed = subprocess.run(
            [sys.executable, "scripts/check_docs.py", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode)
        self.assertIn("--root", completed.stdout)


if __name__ == "__main__":
    unittest.main()
