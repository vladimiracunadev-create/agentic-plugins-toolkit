"""Pruebas deterministas del toolkit.

No consumen API, no abren red y no dependen del orden. Cada garantía que el
README o SECURITY.md afirman tiene aquí una prueba con nombre reconocible: si
alguien retira la garantía, la prueba cae con ella.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agentic_plugins import __version__
from agentic_plugins.catalog import load_agent_snapshot, load_catalog, plugins_by_id
from agentic_plugins.cli import main
from agentic_plugins.evaluation import evaluate_plugin
from agentic_plugins.exporter import export_plugin, uninstall_plugin
from agentic_plugins.hooks import build_message
from agentic_plugins.mcp_server import handle_message
from agentic_plugins.packager import package_plugin
from agentic_plugins.policy import classify_action, route_request
from agentic_plugins.render import expected_views
from agentic_plugins.server import ensure_bind_is_allowed, is_loopback
from agentic_plugins.syncer import check_sync
from agentic_plugins.validator import validate

SKIP_DIRECTORIES = {".git", ".venv", "dist", "build", "__pycache__", ".ruff_cache"}


def repository_files(pattern: str):
    for path in ROOT.rglob(pattern):
        if not any(part in SKIP_DIRECTORIES for part in path.relative_to(ROOT).parts):
            yield path


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.plugins = plugins_by_id(cls.catalog)
        cls.snapshot = load_agent_snapshot(ROOT)

    def test_catalog_declares_six_plugins(self):
        self.assertEqual(6, len(self.catalog["plugins"]))

    def test_plugin_ids_are_unique(self):
        self.assertEqual(len(self.catalog["plugins"]), len(self.plugins))

    def test_ten_distinct_agents_are_packaged(self):
        agents = {
            agent
            for plugin in self.catalog["plugins"]
            for agent in plugin["components"]["agents"]
        }
        self.assertEqual(10, len(agents))

    def test_every_packaged_agent_exists_in_the_snapshot(self):
        known = {item["id"] for item in self.snapshot["agents"]}
        for plugin in self.catalog["plugins"]:
            for agent in plugin["components"]["agents"]:
                self.assertIn(agent, known, f"{plugin['id']} referencia {agent}")

    def test_status_is_honest(self):
        """Ningún plugin puede declarar adopción productiva sin evidencia."""
        for plugin in self.catalog["plugins"]:
            self.assertEqual("IMPLEMENTED", plugin["status"])
            self.assertEqual(plugin["status"], plugin["maturity"]["declared"])
            self.assertIn("PRODUCTION_OBSERVED", plugin["maturity"]["not_claimed"])

    def test_targets_are_declared(self):
        expected = {"openai", "claude-code", "github-copilot", "gemini", "generic-mcp"}
        for plugin in self.catalog["plugins"]:
            self.assertEqual(expected, {item["id"] for item in plugin["targets"]})

    def test_version_is_coherent_across_every_marker(self):
        """El paquete, el catálogo y cada plugin declaran la misma versión."""
        pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        self.assertIn(f'version = "{__version__}"', pyproject)
        self.assertEqual(__version__, self.catalog["repository_version"])
        for plugin in self.catalog["plugins"]:
            self.assertEqual(__version__, plugin["version"], plugin["id"])

    def test_readme_badges_match_the_catalog(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        agents = {
            agent
            for plugin in self.catalog["plugins"]
            for agent in plugin["components"]["agents"]
        }
        evals = sum(
            len(evaluate_plugin(ROOT, plugin)) for plugin in self.catalog["plugins"]
        )
        self.assertIn(f"plugins-{len(self.catalog['plugins'])}-", readme)
        self.assertIn(f"agentes-{len(agents)}-", readme)
        self.assertIn(f"evals_deterministas-{evals}-", readme)
        self.assertIn(f"version-{__version__}-", readme)


class GeneratedViewTests(unittest.TestCase):
    """La documentación no puede contradecir al contrato porque se genera de él."""

    def test_no_drift(self):
        self.assertEqual([], check_sync(ROOT))

    def test_validate_is_clean(self):
        self.assertEqual([], validate(ROOT))

    def test_every_duplicated_file_is_generated(self):
        """Dentro de un paquete solo `evals/cases.jsonl` se escribe a mano."""
        views = set(expected_views(ROOT))
        for plugin_dir in sorted((ROOT / "plugins").iterdir()):
            for path in plugin_dir.rglob("*"):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                if path.relative_to(plugin_dir) == Path("evals") / "cases.jsonl":
                    continue
                self.assertIn(path, views, f"{path} no es una vista generada")

    def test_manifests_carry_the_catalog_version(self):
        catalog = load_catalog(ROOT)
        for plugin in catalog["plugins"]:
            base = ROOT / "plugins" / plugin["id"]
            for relative in (".codex-plugin/plugin.json", ".claude-plugin/plugin.json"):
                data = json.loads((base / relative).read_text(encoding="utf-8"))
                self.assertEqual(plugin["id"], data["name"])
                self.assertEqual(plugin["version"], data["version"])

    def test_marketplaces_list_every_plugin(self):
        catalog = load_catalog(ROOT)
        for relative in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
            data = json.loads((ROOT / relative).read_text(encoding="utf-8"))
            self.assertEqual(len(catalog["plugins"]), len(data["plugins"]))

    def test_site_catalog_exists_for_static_hosting(self):
        """GitHub Pages sirve archivos, no la API del panel."""
        data = json.loads((ROOT / "site" / "catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(6, data["totals"]["plugins"])
        self.assertEqual(10, data["totals"]["agents"])

    def test_site_assets_use_relative_paths(self):
        """Un Pages de proyecto se sirve bajo un subdirectorio, no bajo `/`."""
        for name in ("index.html", "app.js", "sw.js"):
            text = (ROOT / "site" / name).read_text(encoding="utf-8")
            for absolute in ('"/styles.css"', '"/app.js"', '"/sw.js"', '"/manifest.webmanifest"'):
                self.assertNotIn(absolute, text, f"{name} usa una ruta absoluta")

    def test_skill_frontmatter_is_wellformed(self):
        catalog = load_catalog(ROOT)
        for plugin in catalog["plugins"]:
            skill_id = plugin["components"]["skills"][0]
            path = ROOT / "plugins" / plugin["id"] / "skills" / skill_id / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname:"))
            self.assertIn("\ndescription:", text)


class PolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugins = plugins_by_id(load_catalog(ROOT))

    def test_direct_activation(self):
        plugin = self.plugins["repository-engineering"]
        self.assertTrue(route_request(plugin, "Audita este repositorio y su README")["activate"])

    def test_negative_routing(self):
        plugin = self.plugins["repository-engineering"]
        self.assertFalse(route_request(plugin, "Dame una receta")["activate"])

    def test_a_negative_word_does_not_cancel_a_human_gate(self):
        """«Publica aunque haga mal clima» sigue siendo una publicación."""
        plugin = self.plugins["repository-engineering"]
        answer = route_request(plugin, "publish esto aunque el clima esté malo")
        self.assertTrue(answer["activate"])
        self.assertTrue(answer["approval"])

    def test_approval_routing(self):
        plugin = self.plugins["legacy-modernization"]
        self.assertTrue(route_request(plugin, "Ejecuta data-migration inmediatamente")["approval"])

    def test_allowed_action(self):
        plugin = self.plugins["product-evolution"]
        self.assertEqual("allowed", classify_action(plugin, "read roadmap")["decision"])

    def test_action_requiring_approval(self):
        plugin = self.plugins["product-evolution"]
        self.assertEqual("approval-required", classify_action(plugin, "release now")["decision"])

    def test_denied_action(self):
        plugin = self.plugins["product-evolution"]
        self.assertEqual("denied", classify_action(plugin, "bypass-approval")["decision"])

    def test_denial_survives_case_and_separator_changes(self):
        """`BYPASS_APPROVAL` y `bypass approval` son la misma acción denegada."""
        plugin = self.plugins["product-evolution"]
        for spelling in ("BYPASS_APPROVAL", "bypass approval", "Bypass-Approval ahora"):
            self.assertEqual("denied", classify_action(plugin, spelling)["decision"], spelling)

    def test_every_plugin_declares_human_gates(self):
        for plugin in self.plugins.values():
            self.assertTrue(plugin["policy"]["approval_required"], plugin["id"])
            self.assertTrue(plugin["policy"]["denied"], plugin["id"])
            self.assertTrue(plugin["policy"]["human_approval_cannot_be_delegated"], plugin["id"])

    def test_hook_message_states_the_limits(self):
        plugin = self.plugins["repository-engineering"]
        message = build_message(plugin)
        self.assertIn("publish", message)
        self.assertIn("bypass-approval", message)


class EvaluationTests(unittest.TestCase):
    def test_every_eval_passes(self):
        catalog = load_catalog(ROOT)
        total = 0
        for plugin in catalog["plugins"]:
            results = evaluate_plugin(ROOT, plugin)
            total += len(results)
            for case in results:
                self.assertTrue(case["passed"], f"{plugin['id']}:{case['id']}")
        self.assertEqual(24, total)

    def test_every_plugin_has_a_human_gate_case(self):
        catalog = load_catalog(ROOT)
        for plugin in catalog["plugins"]:
            results = evaluate_plugin(ROOT, plugin)
            self.assertTrue(
                any(case["expected"]["approval"] for case in results),
                f"{plugin['id']} no evalúa ningún gate humano",
            )

    def test_every_plugin_has_a_non_activation_case(self):
        catalog = load_catalog(ROOT)
        for plugin in catalog["plugins"]:
            results = evaluate_plugin(ROOT, plugin)
            self.assertTrue(
                any(not case["expected"]["activate"] for case in results),
                f"{plugin['id']} no evalúa la no-activación",
            )


class McpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = load_catalog(ROOT)
        cls.plugins = plugins_by_id(cls.catalog)
        cls.protocol = cls.catalog["mcp_protocol_version"]
        cls.steps = cls.catalog["execution_plan_steps"]

    def test_initialize_reports_the_plugin_version(self):
        plugin = self.plugins["repository-engineering"]
        answer = handle_message(
            plugin, {"jsonrpc": "2.0", "id": 1, "method": "initialize"}, self.protocol, self.steps
        )
        self.assertEqual(plugin["version"], answer["result"]["serverInfo"]["version"])
        self.assertEqual(self.protocol, answer["result"]["protocolVersion"])

    def test_lists_three_tools(self):
        plugin = self.plugins["repository-engineering"]
        answer = handle_message(plugin, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertEqual(3, len(answer["result"]["tools"]))

    def test_plan_does_not_execute(self):
        plugin = self.plugins["repository-engineering"]
        answer = handle_message(
            plugin,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {"name": "create_execution_plan", "arguments": {"task": "x"}},
            },
            self.protocol,
            self.steps,
        )
        steps = answer["result"]["structuredContent"]["steps"]
        self.assertIn("human-gates", steps)
        self.assertEqual(self.steps, steps)

    def test_unknown_tool_is_rejected(self):
        plugin = self.plugins["repository-engineering"]
        answer = handle_message(
            plugin,
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "missing"}},
        )
        self.assertEqual(-32601, answer["error"]["code"])

    def test_notifications_produce_no_answer(self):
        plugin = self.plugins["repository-engineering"]
        self.assertIsNone(
            handle_message(plugin, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        )

    def test_distributed_server_agrees_with_the_cli(self):
        """El servidor autocontenido no puede clasificar distinto que la CLI.

        Antes de generarlo desde el catálogo reimplementaba la comparación con
        `x in action.lower()`, así que devolvía `allowed` para `BYPASS_APPROVAL`
        mientras la CLI devolvía `denied`.
        """
        actions = [
            "BYPASS_APPROVAL now",
            "bypass approval",
            "publicar el release",
            "leer el roadmap",
            "exfiltrate secret",
            "PUSH a main",
        ]
        for plugin_id in ("repository-engineering", "rootcause-response"):
            plugin = self.plugins[plugin_id]
            script = ROOT / "plugins" / plugin_id / "runtime" / "mcp_server.py"
            requests = "\n".join(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": index,
                        "method": "tools/call",
                        "params": {"name": "policy_check", "arguments": {"action": action}},
                    }
                )
                for index, action in enumerate(actions)
            )
            completed = subprocess.run(
                [sys.executable, str(script)],
                input=requests,
                capture_output=True,
                text=True,
                encoding="utf-8",
                check=True,
            )
            answers = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
            self.assertEqual(len(actions), len(answers))
            for action, answer in zip(actions, answers, strict=True):
                self.assertEqual(
                    classify_action(plugin, action),
                    answer["result"]["structuredContent"],
                    f"{plugin_id} · {action}",
                )

    def test_distributed_server_survives_a_malformed_message(self):
        script = ROOT / "plugins" / "product-evolution" / "runtime" / "mcp_server.py"
        completed = subprocess.run(
            [sys.executable, str(script)],
            input='no json\n{"jsonrpc":"2.0","id":9,"method":"tools/list"}\n',
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
        )
        answers = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
        self.assertEqual(-32603, answers[0]["error"]["code"])
        self.assertEqual(3, len(answers[1]["result"]["tools"]))


class SecurityTests(unittest.TestCase):
    def test_panel_refuses_a_non_loopback_bind_without_optin(self):
        self.assertTrue(is_loopback("127.0.0.1"))
        self.assertTrue(is_loopback("localhost"))
        self.assertFalse(is_loopback("0.0.0.0"))
        ensure_bind_is_allowed("127.0.0.1")
        with self.assertRaises(ValueError):
            ensure_bind_is_allowed("0.0.0.0")

    def test_hooks_do_not_depend_on_a_python3_binary(self):
        """`python3` no existe en una instalación estándar de Windows."""
        for path in repository_files("hooks.json"):
            self.assertNotIn("python3", path.read_text(encoding="utf-8"), str(path))

    def test_no_dangerous_command_is_shipped(self):
        # `validator.py` y esta prueba contienen los patrones por definición: son
        # el detector, no el hallazgo. Cualquier otro archivo que los mencione es
        # exactamente lo que se está buscando.
        detectors = {"validator.py", "test_toolkit.py"}
        for pattern in ("*.md", "*.json", "*.py", "*.jsonl"):
            for path in repository_files(pattern):
                if path.name in detectors:
                    continue
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("--dangerously-skip-permissions", text, str(path))
                self.assertNotIn("shell=True", text, str(path))

    def test_export_preserves_an_unmanaged_directory(self):
        plugin = plugins_by_id(load_catalog(ROOT))["portfolio-governance"]
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            intruder = target / plugin["id"]
            intruder.mkdir()
            (intruder / "mio.txt").write_text("no me toques", encoding="utf-8")
            with self.assertRaises(ValueError):
                export_plugin(ROOT, plugin, target)
            self.assertEqual("no me toques", (intruder / "mio.txt").read_text(encoding="utf-8"))

    def test_uninstall_refuses_an_unmanaged_directory(self):
        plugin = plugins_by_id(load_catalog(ROOT))["portfolio-governance"]
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / plugin["id"]).mkdir()
            with self.assertRaises(ValueError):
                uninstall_plugin(plugin, target)

    def test_export_and_uninstall_roundtrip(self):
        plugin = plugins_by_id(load_catalog(ROOT))["portfolio-governance"]
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            path = export_plugin(ROOT, plugin, target)
            self.assertTrue((path / ".agentic-plugins-managed.json").is_file())
            self.assertTrue(uninstall_plugin(plugin, target))
            self.assertFalse(path.exists())


class PackagingTests(unittest.TestCase):
    def test_packages_are_reproducible(self):
        plugin = plugins_by_id(load_catalog(ROOT))["portfolio-governance"]
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one, digest_one = package_plugin(ROOT, plugin, Path(first))
            _, digest_two = package_plugin(ROOT, plugin, Path(second))
            self.assertEqual(digest_one, digest_two)
            with zipfile.ZipFile(one) as archive:
                names = archive.namelist()
            self.assertIn("portfolio-governance/plugin.yaml", names)
            self.assertIn("portfolio-governance/runtime/mcp_server.py", names)
            self.assertFalse([name for name in names if "__pycache__" in name])

    def test_package_name_carries_the_version(self):
        plugin = plugins_by_id(load_catalog(ROOT))["rootcause-response"]
        with tempfile.TemporaryDirectory() as tmp:
            path, _ = package_plugin(ROOT, plugin, Path(tmp))
            self.assertEqual(f"rootcause-response-{plugin['version']}.zip", path.name)


class FormatTests(unittest.TestCase):
    def test_json_files_parse(self):
        for path in repository_files("*.json"):
            json.loads(path.read_text(encoding="utf-8"))

    def test_jsonl_files_parse(self):
        for path in repository_files("*.jsonl"):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    json.loads(line)

    def test_ard_is_explicitly_experimental(self):
        data = json.loads((ROOT / "catalog/ai-catalog.json").read_text(encoding="utf-8"))
        self.assertEqual("ARD_READY_NOT_CONFORMANCE_CLAIM", data["status"])

    def test_documented_files_exist(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for name in ("INSTALL.md", "CONTRIBUTING.md", "SECURITY.md", "ROADMAP.md", "CHANGELOG.md"):
            self.assertIn(name, readme)
            self.assertTrue((ROOT / name).is_file(), name)

    def test_every_docs_link_in_the_readme_resolves(self):
        import re

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for target in re.findall(r"\]\((docs/[A-Za-z_./-]+\.md)\)", readme):
            self.assertTrue((ROOT / target).is_file(), target)


class CliTests(unittest.TestCase):
    def test_list_and_validate_succeed(self):
        self.assertEqual(0, main(["--root", str(ROOT), "list"]))
        self.assertEqual(0, main(["--root", str(ROOT), "validate"]))

    def test_sync_check_reports_no_drift(self):
        self.assertEqual(0, main(["--root", str(ROOT), "sync", "--check"]))

    def test_eval_all_succeeds(self):
        self.assertEqual(0, main(["--root", str(ROOT), "eval", "--all"]))

    def test_unknown_plugin_returns_two(self):
        self.assertEqual(2, main(["--root", str(ROOT), "inspect", "no-existe"]))

    def test_eval_without_selection_returns_two(self):
        self.assertEqual(2, main(["--root", str(ROOT), "eval"]))

    def test_doctor_reports_a_healthy_repository(self):
        self.assertEqual(0, main(["--root", str(ROOT), "doctor"]))


if __name__ == "__main__":
    unittest.main()
