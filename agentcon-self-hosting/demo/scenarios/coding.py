"""Scenario: repair a tiny invoice library whose test suite fails, one dependent bug at a time.

Every test runs the whole pipeline (parse -> price -> invoice -> render), so an early bug raises or
mismatches before a later bug can show. `make_scenario(n)` injects the first n bugs; the suite is
green only when all n are fixed. Each step depends on the previous test output, which is exactly
what makes batching impossible.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import weakref
from pathlib import Path
from typing import Any

from scenario import Scenario

PARSE_PY = '''"""Parse order lines such as 'usb-cable x3 @ 250' (sku, quantity, unit price in cents)."""
import re

LINE = re.compile(r"^(?P<sku>[a-z-]+) x(?P<qty>\\d+) @ (?P<price>\\d+)$")


def parse_line(text):
    m = LINE.match(text.strip())
    if m is None:
        raise ValueError(f"bad line: {text!r}")
    return m["sku"], int(m["qty"]), int(m["price"])


def parse_order(text):
    return [parse_line(line) for line in text.splitlines() if line.strip()]
'''

PRICING_PY = '''"""Line pricing in integer cents."""

BULK_MIN = 10
BULK_PERCENT = 10


def line_total(qty, price):
    total = qty * price
    if qty >= BULK_MIN:
        total -= total * BULK_PERCENT // 100
    return total
'''

INVOICE_PY = '''"""Build an invoice from an order; tax is rounded to the nearest cent."""
from parse import parse_order
from pricing import line_total

TAX_PERCENT = 8


def build_invoice(text):
    lines = [(sku, qty, line_total(qty, price)) for sku, qty, price in parse_order(text)]
    subtotal = sum(total for _, _, total in lines)
    tax = (subtotal * TAX_PERCENT + 50) // 100
    return {"lines": lines, "subtotal": subtotal, "tax": tax, "total": subtotal + tax}
'''

RENDER_PY = '''"""Plain-text invoice rendering."""


def money(cents):
    return f"${cents // 100}.{cents % 100:02d}"


def render(inv):
    rows = [f"{sku:<12}{qty:>4}{money(total):>10}" for sku, qty, total in inv["lines"]]
    rows.append(f"{'TOTAL':<16}{money(inv['total']):>10}")
    return "\\n".join(rows)
'''

TEST_FILE = "test_invoice.py"
TEST_PY = '''from invoice import build_invoice
from render import render


def check(order, subtotal, tax, total, text):
    inv = build_invoice(order)
    assert inv["subtotal"] == subtotal
    assert inv["tax"] == tax
    assert inv["total"] == total
    assert render(inv) == text


def test_two_lines_with_bulk_discount():
    check(
        "usb-cable x10 @ 899\\nmouse-pad x2 @ 909",
        9909, 793, 10702,
        "usb-cable     10    $80.91\\nmouse-pad      2    $18.18\\nTOTAL              $107.02",
    )


def test_round_prices():
    check(
        "hdmi-cord x10 @ 305\\nlaptop-stand x2 @ 250",
        3245, 260, 3505,
        "hdmi-cord     10    $27.45\\nlaptop-stand   2     $5.00\\nTOTAL               $35.05",
    )


def test_larger_order():
    check(
        "desk-lamp x10 @ 1080\\nkey-cap x2 @ 250",
        10220, 818, 11038,
        "desk-lamp     10    $97.20\\nkey-cap        2     $5.00\\nTOTAL              $110.38",
    )


def test_three_lines():
    check(
        "usb-cable x10 @ 899\\nmouse-pad x2 @ 909\\nstylus x1 @ 301",
        10210, 817, 11027,
        "usb-cable     10    $80.91\\nmouse-pad      2    $18.18\\nstylus         1     $3.01\\nTOTAL"
        "              $110.27",
    )
'''
TOTAL_TESTS = TEST_PY.count("def test_")

CLEAN_FILES = {
    "parse.py": PARSE_PY,
    "pricing.py": PRICING_PY,
    "invoice.py": INVOICE_PY,
    "render.py": RENDER_PY,
    TEST_FILE: TEST_PY,
}

# (file, buggy text, correct text), in the order they surface. Bug k is invisible until k-1 is fixed.
BUGS: list[tuple[str, str, str]] = [
    ("parse.py", "(?P<sku>[a-z]+)", "(?P<sku>[a-z-]+)"),
    ("pricing.py", "if qty > BULK_MIN:", "if qty >= BULK_MIN:"),
    ("invoice.py", "tax = subtotal * TAX_PERCENT // 100", "tax = (subtotal * TAX_PERCENT + 50) // 100"),
    ("render.py", "{cents % 100}", "{cents % 100:02d}"),
]

MAX_BUGS = len(BUGS)
DEFAULT_BUGS = 3
MAX_OUTPUT_LINES = 60
TEST_TIMEOUT_S = 20

TASK = (
    "The test suite of a small invoice library (parse order lines, price them with a bulk discount, "
    "add tax, render the invoice) is failing. Make the whole suite pass by fixing the source files, "
    "not the tests, then report what you fixed."
)

SYSTEM_PROMPT = """You are a coding agent repairing a small Python project with a failing test suite. Tools:
run_tests (run the suite), grep (regex search over the source), read_file (read one file),
edit_file (replace one exact snippet) and done (finish).
Workflow: run the tests, read the failure carefully, read the file it points to, fix it with an exact
edit_file (old must match the file text exactly once), then run the tests again. Repeat until every
test passes, then call done with a short summary. Do not edit the test file. Fixing one problem may
reveal another, so always re-run the tests after an edit.
Call exactly one tool at a time and respond only with tool calls. Do not answer in plain text."""

REQUIRED_STEPS = ["run_tests", "read_file", "edit_file"]
TERMINAL_TOOL = "done"

NUDGES = {
    "retry": "That was not a valid tool call. Respond with exactly one tool call from the allowed tools.",
    "step_blocked": "You cannot finish yet. Run the tests, read the failing file and fix it first.",
    "prerequisite": "Out of order. Run the tests, read the file the failure points to, then edit it.",
    "fatal": "Too many invalid responses.",
}


def tool_schemas() -> list[dict[str, Any]]:
    def fn(name: str, desc: str, **props: str) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": name,
                "description": desc,
                "parameters": {
                    "type": "object",
                    "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
                    "required": list(props),
                },
            },
        }

    return [
        fn("run_tests", "Run the project's test suite and return the (trimmed) pytest output."),
        fn("grep", "Regex search over the project's .py files; returns path:line:text matches.", pattern="regex"),
        fn("read_file", "Read one project file.", path="path relative to the project, e.g. parse.py"),
        fn(
            "edit_file",
            "Replace one snippet in a file. 'old' must appear exactly once in the file.",
            path="path relative to the project",
            old="exact existing text, must occur exactly once",
            new="replacement text",
        ),
        fn("done", "Finish. Only after the tests pass on a fresh run.", summary="what you fixed"),
    ]


def project_files(bugs: int) -> dict[str, str]:
    """The project text with the first `bugs` bugs injected."""
    if not 1 <= bugs <= MAX_BUGS:
        raise ValueError(f"bugs must be between 1 and {MAX_BUGS}, got {bugs}")
    files = dict(CLEAN_FILES)
    for name, buggy, clean in BUGS[:bugs]:
        assert files[name].count(clean) == 1, (name, clean)
        files[name] = files[name].replace(clean, buggy)
    return files


def solve_script(bugs: int) -> list[tuple[str, dict[str, Any]]]:
    """A known-correct tool-call sequence: run, read, fix per bug; then verify and finish."""
    project_files(bugs)  # validates the range
    steps: list[tuple[str, dict[str, Any]]] = []
    for name, buggy, clean in BUGS[:bugs]:
        steps += [
            ("run_tests", {}),
            ("read_file", {"path": name}),
            ("edit_file", {"path": name, "old": buggy, "new": clean}),
        ]
    steps += [("run_tests", {}), ("done", {"summary": f"Fixed {bugs} bug(s); all tests pass."})]
    return steps


_SUMMARY_TIME = re.compile(r"\s+in\s+[\d.]+s(\s+\(.*\))?$")
_COUNT = re.compile(r"(\d+) (passed|failed|error|errors)")


def _clean_output(raw: str) -> str:
    lines = [_SUMMARY_TIME.sub("", ln.rstrip()) for ln in raw.splitlines()]
    if len(lines) > MAX_OUTPUT_LINES:
        keep_tail = 12
        head = lines[: MAX_OUTPUT_LINES - keep_tail - 1]
        lines = [*head, f"... ({len(lines) - len(head) - keep_tail} lines trimmed)", *lines[-keep_tail:]]
    return "\n".join(lines)


class CodingWorkspace:
    """A private temp copy of the project plus the five tools; tracks what has been done."""

    def __init__(self, bugs: int) -> None:
        self.bugs = bugs
        self.root = Path(tempfile.mkdtemp(prefix="coding-demo-")).resolve()
        self._finalizer = weakref.finalize(self, shutil.rmtree, str(self.root), True)
        for name, text in project_files(bugs).items():
            (self.root / name).write_text(text)
        self.steps: list[str] = []
        self.final: str | None = None
        self._edits = 0
        self._edits_at_last_run = 0

    def close(self) -> None:
        self._finalizer()

    def run(self, tool: str, args: dict[str, Any]) -> tuple[str, str | None]:
        """Return (output, error). Exactly one is non-empty."""
        handler = getattr(self, f"_tool_{tool}", None)
        if handler is None or tool not in {t["function"]["name"] for t in tool_schemas()}:
            return "", f"unknown tool {tool!r}"
        output, error = handler(args)
        if error is None:
            self.steps.append(tool)
        return output, error

    def _resolve(self, raw: Any) -> tuple[Path | None, str | None]:
        rel = str(raw or "")
        if not rel.strip():
            return None, "path is required"
        p = Path(rel)
        if p.is_absolute() or ".." in p.parts:
            return None, f"path {rel!r} must be relative to the project and may not contain '..'"
        target = (self.root / p).resolve()
        if target != self.root and self.root not in target.parents:
            return None, f"path {rel!r} escapes the project"
        return target, None

    def _pytest(self) -> str:
        env = {
            "PATH": os.environ.get("PATH", ""),
            "HOME": os.environ.get("HOME", str(self.root)),
            "LANG": "C.UTF-8",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONHASHSEED": "0",
            "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "NO_COLOR": "1",
        }
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=short"],
                cwd=self.root,
                env=env,
                capture_output=True,
                text=True,
                timeout=TEST_TIMEOUT_S,
                check=False,
            )
        except subprocess.TimeoutExpired:
            return f"test run timed out after {TEST_TIMEOUT_S}s"
        return _clean_output(proc.stdout + proc.stderr)

    def _tool_run_tests(self, _args: dict[str, Any]) -> tuple[str, str | None]:
        self._edits_at_last_run = self._edits
        return self._pytest(), None

    def _tool_grep(self, args: dict[str, Any]) -> tuple[str, str | None]:
        try:
            rx = re.compile(str(args.get("pattern", "")))
        except re.error as exc:
            return "", f"invalid regex: {exc}"
        hits = []
        for path in sorted(self.root.glob("*.py")):
            for no, line in enumerate(path.read_text().splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{path.name}:{no}:{line}")
        return ("\n".join(hits[:40]) if hits else "no matches"), None

    def _tool_read_file(self, args: dict[str, Any]) -> tuple[str, str | None]:
        target, err = self._resolve(args.get("path"))
        if err or target is None:
            return "", err
        if not target.is_file():
            return "", f"no such file {args.get('path')!r}; files: {', '.join(sorted(p.name for p in self.root.glob('*.py')))}"
        return target.read_text(), None

    def _tool_edit_file(self, args: dict[str, Any]) -> tuple[str, str | None]:
        target, err = self._resolve(args.get("path"))
        if err or target is None:
            return "", err
        if target.name == TEST_FILE:
            return "", f"{TEST_FILE} is read-only; fix the source files instead"
        if not target.is_file():
            return "", f"no such file {args.get('path')!r}"
        old, new = args.get("old"), args.get("new")
        if not isinstance(old, str) or not old or not isinstance(new, str):
            return "", "edit_file requires non-empty string 'old' and string 'new'"
        text = target.read_text()
        count = text.count(old)
        if count != 1:
            return "", f"'old' occurs {count} times in {args.get('path')}; it must occur exactly once (add context to make it unique)"
        target.write_text(text.replace(old, new))
        self._edits += 1
        return f"edited {args.get('path')}", None

    def _tool_done(self, args: dict[str, Any]) -> tuple[str, str | None]:
        if self._edits == 0:
            return "", "no_changes: no edit has been made, so nothing was fixed"
        if self._edits_at_last_run != self._edits:
            return "", "unverified: you edited files since the last run_tests; run the tests before finishing"
        summary = str(args.get("summary", ""))
        if not summary.strip():
            return "", "done requires a non-empty 'summary' argument"
        self.final = summary
        return "accepted", None

    def score(self) -> float:
        counts = {"passed": 0, "failed": 0, "error": 0}
        for n, kind in _COUNT.findall(self._pytest()):
            counts[kind.rstrip("s") if kind == "errors" else kind] += int(n)
        return min(counts["passed"], TOTAL_TESTS) / TOTAL_TESTS


def make_scenario(bugs: int) -> Scenario:
    project_files(bugs)  # validate
    return Scenario(
        name="coding" if bugs == DEFAULT_BUGS else f"coding-{bugs}",
        system_prompt=SYSTEM_PROMPT,
        task=TASK,
        tools=tool_schemas(),
        new_workspace=lambda: CodingWorkspace(bugs),
        required_steps=list(REQUIRED_STEPS),
        terminal_tool=TERMINAL_TOOL,
        prerequisites=[
            {"tool": "read_file", "requires": "run_tests"},
            {"tool": "edit_file", "requires": "read_file"},
        ],
        nudges=dict(NUDGES),
    )


LADDER = {n: make_scenario(n) for n in (1, 2, 3, 4)}
SCENARIO = LADDER[DEFAULT_BUGS]
