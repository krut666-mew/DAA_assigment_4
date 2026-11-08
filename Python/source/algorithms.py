"""Implement algorithm bodies. See docs/guide/CONTRACTS.md; inputs and outputs are dictionaries."""

def lcs(request):
    """Find one longest common subsequence of two strings."""
    a = request["a"]
    b = request["b"]

    n = len(a)
    m = len(b)

    # dp[i][j] = LCS length for a[:i] and b[:j]
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    # Build the DP table
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct one optimal subsequence
    result = []
    i = n
    j = m

    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()

    return {
        "length": dp[n][m],
        "sequence": "".join(result)
    }


def merge(request):
    """Plan the cheapest sequence of adjacent block merges when the original order must be preserved. Implement merge according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO merge")

def tree(request):
    """Choose a maximum-value set when neighbouring vertices are incompatible and conflicts form a tree. Implement tree according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO tree")

def naive(request):
    """Establish a simple exact-search baseline against which the other two searches can be checked. Implement naive according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO naive")

def kmp(request):
    """Reuse information about matched prefixes to avoid restarting the search after every mismatch. Implement kmp according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO kmp")

def rk(request):
    """Reject windows with unequal fingerprints and verify every equal-hash candidate. Implement rk according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO rk")

def suffix(request):
    """Order the text suffixes and use adjacent common prefixes to find repeated substrings. Implement suffix according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO suffix")

def aho(request):
    """Build one dictionary automaton and count its patterns in several independent texts. Implement aho according to docs/guide/CONTRACTS.md."""
    raise NotImplementedError("TODO aho")
