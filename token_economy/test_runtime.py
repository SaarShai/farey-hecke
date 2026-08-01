from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from token_economy.bench import run_framework_smoke
from token_economy.skills import discover_active_skills, run_skill_tests
from token_economy.wiki import SKIP_PARTS, WikiStore


def snapshot(root: Path) -> dict[str, tuple[int, str]]:
    return {
        path.relative_to(root).as_posix(): (
            path.stat().st_mtime_ns,
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        for path in root.rglob("*")
        if path.is_file()
    }


class RuntimeTests(unittest.TestCase):
    def test_wiki_scan_excludes_private_runtime_and_build_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "kept.md").write_text("# Kept\n", encoding="utf-8")
            for part in SKIP_PARTS:
                hidden = root / part / "hidden.md"
                hidden.parent.mkdir(parents=True, exist_ok=True)
                hidden.write_text("# Hidden\n", encoding="utf-8")
            self.assertEqual(WikiStore(root).iter_markdown(), [root.resolve() / "kept.md"])

    def test_framework_benchmark_does_not_mutate_caller_repo(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "token_economy").mkdir()
            (root / "token_economy" / "wiki.py").write_text("class WikiStore: pass\n", encoding="utf-8")
            (root / "prompts" / "subagents").mkdir(parents=True)
            (root / "prompts" / "subagents" / "research-lite.prompt.md").write_text("research\n", encoding="utf-8")
            (root / "wiki").mkdir()
            (root / "wiki" / "index.md").write_text("# Context refresh\n", encoding="utf-8")
            before = snapshot(root)
            result = run_framework_smoke(root, root / "wiki")
            self.assertTrue(result["ok"])
            self.assertEqual(result["caller_repo_writes"], 0)
            self.assertEqual(snapshot(root), before)

    def test_skill_runner_isolates_a_standalone_test(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            skill = root / "skills" / "demo"
            (skill / "tools").mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Demo\n", encoding="utf-8")
            (skill / "tools" / "test_demo.py").write_text("assert __name__ == '__main__'\n", encoding="utf-8")
            result = run_skill_tests(root, ("demo",))
            self.assertTrue(result["ok"])
            self.assertEqual(result["tests"], 1)

    def test_active_skill_discovery_includes_shared_and_excludes_retired(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "skills" / "_shared").mkdir(parents=True)
            active = root / "skills" / "active"
            active.mkdir()
            (active / "SKILL.md").write_text("---\nname: active\n---\n", encoding="utf-8")
            retired = root / "skills" / "retired"
            retired.mkdir()
            (retired / "SKILL.md").write_text("---\nname: retired\nretired: true\n---\n", encoding="utf-8")
            self.assertEqual(discover_active_skills(root), ("_shared", "active"))


if __name__ == "__main__":
    unittest.main()
