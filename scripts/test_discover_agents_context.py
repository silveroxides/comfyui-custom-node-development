import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT_PATH = Path(__file__).with_name("discover_agents_context.py")
SPEC = importlib.util.spec_from_file_location("discover_agents_context", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DiscoverAgentsContextTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.comfy_root = self.root / "ComfyUI"
        self.repo_root = self.comfy_root / "custom_nodes" / "ExampleNode"
        self.agents_path = self.repo_root / "AGENTS.md"
        self.repo_root.mkdir(parents=True)
        (self.comfy_root / "folder_paths.py").write_text("", encoding="utf-8")

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_discovers_workspace_and_windows_venv(self):
        python_executable = self.comfy_root / ".venv" / "Scripts" / "python.exe"
        python_executable.parent.mkdir(parents=True)
        python_executable.write_text("", encoding="utf-8")

        context = MODULE.discover_context(self.agents_path)

        self.assertEqual(context["agents_path"], str(self.agents_path.resolve()))
        self.assertEqual(context["candidates"]["comfyui_root"], str(self.comfy_root))
        self.assertEqual(context["candidates"]["custom_nodes_root"], str(self.comfy_root / "custom_nodes"))
        self.assertEqual(context["candidates"]["repository_root"], str(self.repo_root))
        self.assertEqual(context["candidates"]["virtual_environment_root"], str(self.comfy_root / ".venv"))
        self.assertEqual(context["candidates"]["python_executable"], str(python_executable))
        self.assertEqual(context["unresolved"], [])

    def test_discovers_workspace_and_posix_venv(self):
        python_executable = self.comfy_root / "venv" / "bin" / "python"
        python_executable.parent.mkdir(parents=True)
        python_executable.write_text("", encoding="utf-8")

        context = MODULE.discover_context(self.agents_path)

        self.assertEqual(context["candidates"]["virtual_environment_root"], str(self.comfy_root / "venv"))
        self.assertEqual(context["candidates"]["python_executable"], str(python_executable))
        self.assertEqual(context["unresolved"], [])

    def test_reports_unresolved_venv_and_python(self):
        context = MODULE.discover_context(self.agents_path)

        self.assertEqual(context["candidates"]["repository_root"], str(self.repo_root))
        self.assertEqual(context["unresolved"], ["virtual_environment_root", "python_executable"])

    def test_does_not_find_context_outside_comfyui(self):
        external_agents = self.root / "ExternalNode" / "AGENTS.md"
        external_agents.parent.mkdir()

        context = MODULE.discover_context(external_agents)

        self.assertEqual(context["candidates"]["repository_root"], str(external_agents.parent))
        self.assertEqual(
            context["unresolved"],
            ["comfyui_root", "custom_nodes_root", "virtual_environment_root", "python_executable"],
        )


if __name__ == "__main__":
    unittest.main()
