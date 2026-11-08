
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "Python" / "source"))

from algorithms import naive, kmp, rk

text = "abacabadabacaba" * 2000
pattern = "abacaba"

request = {"text": text, "pattern": pattern}

algorithms = [
    ("Naive", naive),
    ("KMP", kmp),
    ("Rabin-Karp", rk),
]

reference = None

for name, algorithm in algorithms:
    start = time.perf_counter()
    result = algorithm(request)
    elapsed = time.perf_counter() - start

    if reference is None:
        reference = result["positions"]
    elif result["positions"] != reference:
        raise AssertionError(f"{name} returned different positions")

    print(
        f"{name}: {elapsed:.6f} seconds, "
        f"{len(result['positions'])} matches"
    )

print("All three algorithms returned identical positions.")
