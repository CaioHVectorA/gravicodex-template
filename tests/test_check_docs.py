from pathlib import Path
import tempfile
import unittest

from scripts.check_docs import audit, scan


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


if __name__ == "__main__":
    unittest.main()
