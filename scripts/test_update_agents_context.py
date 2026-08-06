import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest


SCRIPT_PATH = Path(__file__).with_name("update_agents_context.py")
SPEC = importlib.util.spec_from_file_location("update_agents_context", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UpdateAgentsContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.comfy_root = self.root / "ComfyUI"
        self.custom_nodes_root = self.comfy_root / "custom_nodes"
        self.repo_root = self.custom_nodes_root / "ExampleNode"
        self.venv_root = self.comfy_root / ".venv"
        self.python_executable = self.venv_root / "Scripts" / "python.exe"
        self.repo_root.mkdir(parents=True)
        self.python_executable.parent.mkdir(parents=True)
        (self.comfy_root / "folder_paths.py").write_text("", encoding="utf-8")
        self.python_executable.write_text("", encoding="utf-8")
        self.agents_path = self.repo_root / "AGENTS.md"

    def tearDown(self):
        self.temporary_directory.cleanup()

    def arguments(self, *, check=False, python_executable=None):
        return SimpleNamespace(
            agents=str(self.agents_path),
            comfy_root=str(self.comfy_root),
            custom_nodes_root=str(self.custom_nodes_root),
            repo_root=str(self.repo_root),
            venv_root=str(self.venv_root),
            python_executable=python_executable,
            check=check,
        )

    def test_creates_agents_from_template_and_is_idempotent(self):
        self.assertTrue(MODULE.update_agents(self.arguments()))
        created = self.agents_path.read_text(encoding="utf-8")

        self.assertIn(str(self.comfy_root), created)
        self.assertIn("## Repository-Specific Instructions", created)
        self.assertFalse(MODULE.update_agents(self.arguments()))
        self.assertFalse(MODULE.update_agents(self.arguments(check=True)))

    def test_discovers_posix_python_executable(self):
        self.python_executable.unlink()
        python_executable = self.venv_root / "bin" / "python"
        python_executable.parent.mkdir()
        python_executable.write_text("", encoding="utf-8")

        self.assertTrue(MODULE.update_agents(self.arguments()))

        created = self.agents_path.read_text(encoding="utf-8")
        self.assertIn(f"python_executable: {python_executable}", created)

    def test_rejects_venv_without_python_executable(self):
        self.python_executable.unlink()

        with self.assertRaisesRegex(ValueError, "does not contain a Python executable"):
            MODULE.update_agents(self.arguments())

    def test_inserts_missing_block_without_replacing_existing_content(self):
        original = "# Existing Instructions\n\n- Preserve this rule.\n"
        self.agents_path.write_text(original, encoding="utf-8")

        self.assertTrue(MODULE.update_agents(self.arguments()))
        updated = self.agents_path.read_text(encoding="utf-8")

        self.assertTrue(updated.startswith(original))
        self.assertEqual(updated.count(MODULE.START), 1)
        self.assertEqual(updated.count(MODULE.END), 1)

    def test_updates_one_managed_block_and_preserves_surrounding_content(self):
        self.agents_path.write_text(
            f"before\n{MODULE.START}\nstatus: uninitialized\n{MODULE.END}\nafter\n",
            encoding="utf-8",
        )

        MODULE.update_agents(self.arguments())
        updated = self.agents_path.read_text(encoding="utf-8")

        self.assertTrue(updated.startswith("before\n"))
        self.assertTrue(updated.endswith("\nafter\n"))
        self.assertIn(f"repository_root: {self.repo_root}", updated)

    def test_rejects_duplicate_managed_blocks(self):
        block = f"{MODULE.START}\nstatus: uninitialized\n{MODULE.END}"
        self.agents_path.write_text(f"{block}\n{block}\n", encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "multiple managed"):
            MODULE.update_agents(self.arguments())

    def test_preserves_crlf_newlines(self):
        original = (
            f"before\r\n{MODULE.START}\r\nstatus: uninitialized\r\n"
            f"{MODULE.END}\r\nafter\r\n"
        )
        self.agents_path.write_bytes(original.encode("utf-8"))

        MODULE.update_agents(self.arguments())
        updated = self.agents_path.read_bytes().decode("utf-8")

        self.assertNotIn("\n", updated.replace("\r\n", ""))
        self.assertIn(f"repository_root: {self.repo_root}\r\n", updated)

    def test_check_rejects_missing_context_without_writing(self):
        original = "# Existing Instructions\n"
        self.agents_path.write_text(original, encoding="utf-8")

        with self.assertRaisesRegex(ValueError, "not initialized"):
            MODULE.update_agents(self.arguments(check=True))

        self.assertEqual(self.agents_path.read_text(encoding="utf-8"), original)

    def test_rejects_repository_outside_custom_nodes_root(self):
        external_repo = self.root / "ExternalNode"
        external_repo.mkdir()
        args = self.arguments()
        args.repo_root = str(external_repo)
        args.agents = str(external_repo / "AGENTS.md")

        with self.assertRaisesRegex(ValueError, "inside the configured custom-nodes root"):
            MODULE.update_agents(args)

    def test_rejects_agents_path_for_another_repository(self):
        other_repo = self.custom_nodes_root / "OtherNode"
        other_repo.mkdir()
        args = self.arguments()
        args.agents = str(other_repo / "AGENTS.md")

        with self.assertRaisesRegex(ValueError, "target does not match repository root"):
            MODULE.update_agents(args)


if __name__ == "__main__":
    unittest.main()
