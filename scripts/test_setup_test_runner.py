from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import setup_test_runner


class SetupTestRunnerTests(unittest.TestCase):
    def test_provisions_runner_and_broad_manifest(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nodes").mkdir()
            (root / "nodes" / "example.py").write_text("", encoding="utf-8")
            (root / "tests").mkdir()
            (root / "tests" / "test_example.py").write_text("", encoding="utf-8")

            runner, manifest = setup_test_runner.provision(root)

            self.assertEqual(runner.read_bytes(), setup_test_runner.RUNNER_ASSET.read_bytes())
            text = manifest.read_text(encoding="utf-8")
            self.assertIn('"nodes/*.py"', text)
            self.assertIn('"tests/test_example.py"', text)

    def test_refuses_to_overwrite_existing_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "nodes").mkdir()
            (root / "tests").mkdir()
            (root / "tests" / "test_example.py").write_text("", encoding="utf-8")
            (root / "tests" / "run_tests.py").write_text("local", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                setup_test_runner.provision(root)


if __name__ == "__main__":
    unittest.main()
