import json
import tempfile
import unittest
from pathlib import Path

from measure import DENY, junit, summarize


def rec(type_, content, ts, **extra):
    return json.dumps({"type": type_, "timestamp": ts, "message": {"content": content}, **extra})


def assistant(id_, ts, inp, out):
    return json.dumps({"type": "assistant", "timestamp": ts, "message": {
        "id": id_, "model": "claude-opus-5-5",
        "usage": {"input_tokens": inp, "cache_read_input_tokens": 100, "output_tokens": out}}})


class SummarizeTest(unittest.TestCase):
    def test_counts(self):
        human = {"origin": {"kind": "human"}}
        lines = [
            rec("user", "make a kata", "2026-11-13T10:00:00Z", **human),
            assistant("m1", "2026-11-13T10:00:05Z", 10, 5),
            assistant("m1", "2026-11-13T10:00:06Z", 10, 5),  # same response, second line: not double counted
            rec("user", [{"type": "tool_result", "content": DENY + ". STOP"}], "2026-11-13T10:01:00Z"),
            rec("user", [{"type": "text", "text": "[Request interrupted by user]"}], "2026-11-13T10:02:00Z"),
            rec("user", "<local-command-caveat>", "2026-11-13T10:03:00Z", isMeta=True),
            rec("user", [{"type": "tool_result", "content": "ok"}], "2026-11-13T10:04:00Z"),
            rec("user", "subagent prompt", "2026-11-13T10:05:00Z", isSidechain=True, **human),
            rec("user", "looks good", "2026-11-13T10:30:00Z", **human),
            "not json",
        ]
        s = summarize(lines)
        self.assertEqual((s["messages"], s["denials"], s["interrupts"], s["interventions"]), (2, 1, 1, 4))
        self.assertEqual((s["input_tokens"], s["output_tokens"]), (110, 5))
        self.assertEqual(s["minutes"], 30.0)
        self.assertEqual(s["models"], {"claude-opus-5-5"})


class JunitTest(unittest.TestCase):
    def test_pass_rate(self):
        with tempfile.TemporaryDirectory() as d:
            Path(d, "TEST-A.xml").write_text('<testsuite tests="5" failures="1" errors="1" skipped="1"/>')
            Path(d, "TEST-B.xml").write_text('<testsuite tests="3" failures="0" errors="0" skipped="0"/>')
            self.assertEqual(junit(Path(d)), (5, 7))


if __name__ == "__main__":
    unittest.main()
