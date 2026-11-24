"""Regression tests for the public guardrail and style checkers."""

import contextlib
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from scripts import check_prose, ste_check


class ScannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.blocklist = self.root / "scripts" / "private-blocklist.local"
        self.blocklist.parent.mkdir()
        self.enterContext(mock.patch.object(check_prose, "REPO", str(self.root)))
        self.enterContext(mock.patch.object(check_prose, "BLOCKLIST_PATH", str(self.blocklist)))

    def run_main(self, sync: bool = False) -> tuple[int, str]:
        output = io.StringIO()
        argv = ["check_prose.py"] + (["--sync"] if sync else [])
        with mock.patch("sys.argv", argv), contextlib.redirect_stdout(output):
            status = check_prose.main()
        return status, output.getvalue()

    def test_public_output_redacts_matches_and_blocklist_entries(self) -> None:
        cases = [
            ("aws-access-key", "AKIA" + "A" * 16),
            ("github-token", "gh" + "p_" + "B" * 24),
            ("openai-key", "sk" + "-" + "C" * 24),
            ("slack-token", "xox" + "b-" + "D" * 16),
            ("private-key-block", "-----BEGIN " + "RSA PRIVATE KEY-----"),
            ("bearer-token", "bearer " + "E" * 30),
            ("generic-assignment", "password=" + "F" * 24),
        ]
        private_entry = "private-" + "project-" + "sentinel"
        self.blocklist.write_text(private_entry + "\n", encoding="utf-8")
        text = "\n".join(value for _, value in cases) + "\n" + private_entry.upper()
        (self.root / "sample.txt").write_text(text, encoding="utf-8")
        status, output = self.run_main()
        self.assertEqual(status, 1)
        for number, (label, value) in enumerate(cases, 1):
            with self.subTest(label=label):
                self.assertIn(f"sample.txt:{number}  secret-shaped: {label}", output)
                self.assertNotIn(value[:24], output)
        self.assertIn("sample.txt:8  forbidden content", output)
        self.assertNotIn(private_entry.lower(), output.lower())

    def test_unreadable_input_fails_without_exception_contents(self) -> None:
        path = self.root / "unreadable.txt"
        path.write_text("Text.", encoding="utf-8")
        with mock.patch.object(check_prose, "open", side_effect=PermissionError("sensitive-detail")):
            status, output = self.run_main()
        self.assertEqual(status, 1)
        self.assertIn("unreadable.txt: unable to read", output)
        self.assertNotIn("sensitive-detail", output)

    def test_missing_blocklist_warns_and_still_scans(self) -> None:
        (self.root / "sample.txt").write_text("sk" + "-" + "G" * 24, encoding="utf-8")
        status, output = self.run_main()
        self.assertEqual(status, 1)
        self.assertIn("WARNING no scripts/private-blocklist.local", output)
        self.assertIn("secret-shaped: openai-key", output)

    def test_requested_sync_without_target_fails(self) -> None:
        with mock.patch.dict(os.environ, {"HERMES_SKILLS_DIR": ""}), mock.patch.object(check_prose.os.path, "isdir", return_value=False):
            status, output = self.run_main(sync=True)
        self.assertEqual(status, 1)
        self.assertIn("sync: no installed skill copy found", output)

    def test_explicit_missing_sync_target_fails(self) -> None:
        with mock.patch.dict(os.environ, {"HERMES_SKILLS_DIR": str(self.root / "absent")}):
            status, output = self.run_main(sync=True)
        self.assertEqual(status, 1)
        self.assertIn("sync:", output)

    def test_sync_includes_scanner_and_redacts_drift(self) -> None:
        self.assertIn("scripts/check_prose.py", check_prose.SYNC_PAIRS)
        installed = self.root / "installed"
        for rel in check_prose.SYNC_PAIRS:
            for root in (self.root, installed):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Same text.\n", encoding="utf-8")
        with mock.patch.dict(os.environ, {"HERMES_SKILLS_DIR": str(installed)}):
            self.assertEqual(check_prose.check_sync(), [])
            scanner = installed / "scripts" / "check_prose.py"
            changed = "private-" + "drift-" + "sentinel"
            scanner.write_text(changed, encoding="utf-8")
            status, output = self.run_main(sync=True)
            self.assertEqual(status, 1)
            self.assertIn("sync: differs: scripts/check_prose.py", output)
            self.assertNotIn(changed, output)
            scanner.unlink()
            self.assertEqual(check_prose.check_sync(), ["sync: installed copy missing: scripts/check_prose.py"])
            (self.root / "scripts" / "check_prose.py").unlink()
            self.assertEqual(check_prose.check_sync(), ["sync: repo file missing: scripts/check_prose.py"])

    def test_scanner_and_tests_scan_clean_without_exemption(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        scanner = self.root / "scripts" / "check_prose.py"
        scanner.write_text((source_root / "scripts" / "check_prose.py").read_text(encoding="utf-8"), encoding="utf-8")
        (self.root / "test_checks.py").write_text(Path(__file__).read_text(encoding="utf-8"), encoding="utf-8")
        status, output = self.run_main()
        self.assertEqual(status, 0, output)
        with scanner.open("a", encoding="utf-8") as handle:
            handle.write("\n# " + "sk" + "-" + "H" * 24 + "\n")
        status, output = self.run_main()
        self.assertEqual(status, 1)
        self.assertIn("scripts/check_prose.py:", output)


class ModalAdviceTests(unittest.TestCase):
    def test_strict_modal_advice_preserves_meaning(self) -> None:
        cases = {
            "may": ("You may leave.", ("permission", "uncertainty")),
            "might": ("The request might fail.", ("uncertainty",)),
            "could": ("The request could fail.", ("ability", "permission", "uncertainty", "conditions")),
            "should": ("You should save a copy.", ("advice", "expectation")),
            "shall": ("The supplier shall send a copy.", ("obligation",)),
            "would": ("The request would fail if the server stopped.", ("conditions", "uncertainty")),
        }
        for word, (text, meanings) in cases.items():
            with self.subTest(word=word):
                findings = [f for f in ste_check.check(text, strict=True) if f.rule == "word" and f.message.startswith(f"'{word}'")]
                self.assertEqual(len(findings), 1)
                message = findings[0].message
                self.assertIn("preserve", message)
                for meaning in meanings:
                    self.assertIn(meaning, message)
                self.assertNotIn("->", message)
                self.assertFalse(any(f.rule == "word" and f.message.startswith(f"'{word}'") for f in ste_check.check(text, strict=False)))


if __name__ == "__main__":
    unittest.main()
