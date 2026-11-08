
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Python" / "source"))

from algorithms import lcs, merge, tree, naive, kmp, rk, suffix, aho


class TestAssignment4(unittest.TestCase):

    def test_lcs(self):
        result = lcs({"a": "tea_time", "b": "team"})
        self.assertEqual(result["length"], 4)
        self.assertEqual(result["sequence"], "team")

    def test_lcs_empty(self):
        self.assertEqual(
            lcs({"a": "", "b": "abc"}),
            {"length": 0, "sequence": ""}
        )

    def test_merge(self):
        result = merge({"sizes": [2, 3, 4]})
        self.assertEqual(result["cost"], 14)
        self.assertEqual(result["plan"], [[0, 0, 1], [0, 1, 2]])

    def test_merge_empty(self):
        self.assertEqual(merge({"sizes": []}), {"cost": 0, "plan": []})

    def test_tree(self):
        result = tree({
            "n": 3,
            "weights": [4, 9, 6],
            "edges": [[0, 1], [1, 2]]
        })
        self.assertEqual(result["weight"], 10)
        self.assertEqual(set(result["selected"]), {0, 2})

    def test_tree_negative(self):
        result = tree({
            "n": 2,
            "weights": [-5, -2],
            "edges": [[0, 1]]
        })
        self.assertEqual(result["weight"], 0)
        self.assertEqual(result["selected"], [])

    def test_naive_overlaps(self):
        self.assertEqual(
            naive({"text": "aaaaa", "pattern": "aaa"}),
            {"positions": [0, 1, 2]}
        )

    def test_kmp_overlaps(self):
        self.assertEqual(
            kmp({"text": "abababa", "pattern": "aba"}),
            {"positions": [0, 2, 4]}
        )

    def test_rk_collision(self):
        self.assertEqual(
            rk({"text": "abdj", "pattern": "ab"}),
            {"positions": [0]}
        )

    def test_empty_pattern(self):
        request = {"text": "abc", "pattern": ""}
        expected = {"positions": [0, 1, 2, 3]}
        self.assertEqual(naive(request), expected)
        self.assertEqual(kmp(request), expected)
        self.assertEqual(rk(request), expected)

    def test_search_algorithms_agree(self):
        text = "abacabaababacaba"
        pattern = "aba"
        request = {"text": text, "pattern": pattern}
        self.assertEqual(naive(request), kmp(request))
        self.assertEqual(naive(request), rk(request))

    def test_suffix(self):
        result = suffix({"text": "banana"})
        self.assertEqual(result["sa"], [5, 3, 1, 0, 4, 2])
        self.assertEqual(result["lcp"], [0, 1, 3, 0, 0, 2])
        self.assertEqual(result["repeated"], "ana")

    def test_suffix_empty(self):
        self.assertEqual(
            suffix({"text": ""}),
            {"sa": [], "lcp": [], "repeated": ""}
        )

    def test_aho(self):
        result = aho({
            "patterns": ["he", "she", "he"],
            "texts": ["sheshe", "sheshe", ""]
        })
        self.assertEqual(
            result["counts"],
            [[2, 2, 2], [2, 2, 2], [0, 0, 0]]
        )

    def test_aho_empty_dictionary(self):
        self.assertEqual(
            aho({"patterns": [], "texts": ["abc", ""]}),
            {"counts": [[], []]}
        )


if __name__ == "__main__":
    unittest.main()
