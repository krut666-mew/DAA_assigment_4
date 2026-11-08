"""Implementations for Assignment 4: Dynamic Programming and String Processing."""

def lcs(request):
    """Return one longest common subsequence of a and b."""
    a = request["a"]
    b = request["b"]

    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result = []
    i, j = n, m

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
    return {"length": dp[n][m], "sequence": "".join(result)}


def merge(request):
    """Return minimum adjacent-merge cost and a chronological merge plan."""
    sizes = request["sizes"]
    n = len(sizes)

    if n <= 1:
        return {"cost": 0, "plan": []}

    prefix = [0] * (n + 1)
    for i, value in enumerate(sizes):
        prefix[i + 1] = prefix[i] + value

    dp = [[0] * n for _ in range(n)]
    split = [[-1] * n for _ in range(n)]

    for length in range(2, n + 1):
        for left in range(n - length + 1):
            right = left + length - 1
            interval_sum = prefix[right + 1] - prefix[left]
            best = None

            for mid in range(left, right):
                candidate = (
                    dp[left][mid]
                    + dp[mid + 1][right]
                    + interval_sum
                )
                if best is None or candidate < best:
                    best = candidate
                    split[left][right] = mid

            dp[left][right] = best

    plan = []

    def build_plan(left, right):
        if left == right:
            return
        mid = split[left][right]
        build_plan(left, mid)
        build_plan(mid + 1, right)
        plan.append([left, mid, right])

    build_plan(0, n - 1)
    return {"cost": dp[0][n - 1], "plan": plan}


def tree(request):
    """Return a maximum-weight independent set of a tree."""
    n = request["n"]
    weights = request["weights"]
    edges = request["edges"]

    if n == 0:
        return {"weight": 0, "selected": []}

    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Iterative traversal avoids recursion errors on long chains.
    parent = [-1] * n
    parent[0] = 0
    order = [0]

    for u in order:
        for v in graph[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    take = [0] * n
    skip = [0] * n

    for u in reversed(order):
        take[u] = weights[u]
        skip[u] = 0

        for v in graph[u]:
            if parent[v] == u:
                take[u] += skip[v]
                skip[u] += max(take[v], skip[v])

    # Reconstruct one optimal set.
    selected = []
    stack = [(0, False)]

    while stack:
        u, parent_was_taken = stack.pop()
        choose_u = not parent_was_taken and take[u] > skip[u]

        if choose_u:
            selected.append(u)

        for v in graph[u]:
            if parent[v] == u:
                stack.append((v, choose_u))

    return {
        "weight": max(take[0], skip[0]),
        "selected": selected
    }


def naive(request):
    """Find all exact pattern occurrences using direct comparisons."""
    text = request["text"]
    pattern = request["pattern"]
    n, m = len(text), len(pattern)

    if m == 0:
        return {"positions": list(range(n + 1))}

    if m > n:
        return {"positions": []}

    positions = []

    for start in range(n - m + 1):
        j = 0
        while j < m and text[start + j] == pattern[j]:
            j += 1
        if j == m:
            positions.append(start)

    return {"positions": positions}


def _prefix_function(pattern):
    """Build the KMP prefix-function array."""
    m = len(pattern)
    pi = [0] * m
    j = 0

    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        pi[i] = j

    return pi


def kmp(request):
    """Find all exact pattern occurrences using KMP."""
    text = request["text"]
    pattern = request["pattern"]
    n, m = len(text), len(pattern)

    if m == 0:
        return {"positions": list(range(n + 1))}

    if m > n:
        return {"positions": []}

    pi = _prefix_function(pattern)
    positions = []
    j = 0

    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == m:
            positions.append(i - m + 1)
            j = pi[j - 1]

    return {"positions": positions}


def rk(request):
    """Find all exact occurrences using Rabin-Karp with verification."""
    text = request["text"]
    pattern = request["pattern"]
    n, m = len(text), len(pattern)

    if m == 0:
        return {"positions": list(range(n + 1))}

    if m > n:
        return {"positions": []}

    base = 31
    mod = 101
    highest_power = pow(base, m - 1, mod)

    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % mod
        window_hash = (window_hash * base + ord(text[i])) % mod

    positions = []

    for start in range(n - m + 1):
        if window_hash == pattern_hash:
            # A hash match is only a candidate. Verify every character.
            if text[start:start + m] == pattern:
                positions.append(start)

        if start < n - m:
            outgoing = ord(text[start])
            incoming = ord(text[start + m])

            window_hash = (
                (window_hash - outgoing * highest_power) * base
                + incoming
            ) % mod

    return {"positions": positions}


def suffix(request):
    """Build a suffix array, Kasai LCP array and longest repeated substring."""
    text = request["text"]
    n = len(text)

    if n == 0:
        return {"sa": [], "lcp": [], "repeated": ""}

    sa = list(range(n))
    rank = [ord(ch) for ch in text]
    length = 1

    # Prefix doubling: sort suffixes by pairs of ranks.
    while length < n:
        sa.sort(
            key=lambda i: (
                rank[i],
                rank[i + length] if i + length < n else -1
            )
        )

        new_rank = [0] * n

        for i in range(1, n):
            previous = sa[i - 1]
            current = sa[i]

            previous_pair = (
                rank[previous],
                rank[previous + length] if previous + length < n else -1
            )
            current_pair = (
                rank[current],
                rank[current + length] if current + length < n else -1
            )

            new_rank[current] = (
                new_rank[previous]
                + (previous_pair != current_pair)
            )

        rank = new_rank

        if rank[sa[-1]] == n - 1:
            break

        length *= 2

    # Kasai algorithm for adjacent LCP values.
    inverse = [0] * n
    for i, suffix_start in enumerate(sa):
        inverse[suffix_start] = i

    lcp = [0] * n
    common = 0

    for start in range(n):
        position = inverse[start]

        if position == 0:
            continue

        previous_start = sa[position - 1]

        while (
            start + common < n
            and previous_start + common < n
            and text[start + common] == text[previous_start + common]
        ):
            common += 1

        lcp[position] = common

        if common > 0:
            common -= 1

    longest = max(lcp)
    repeated = ""

    if longest > 0:
        best_position = lcp.index(longest)
        repeated_start = sa[best_position]
        repeated = text[repeated_start:repeated_start + longest]

    return {
        "sa": sa,
        "lcp": lcp,
        "repeated": repeated
    }


def aho(request):
    """Count all dictionary patterns in each text using Aho-Corasick."""
    patterns = request["patterns"]
    texts = request["texts"]
    pattern_count = len(patterns)

    # Trie transitions and failure links.
    transitions = [{}]
    failure = [0]
    terminal = [[]]

    # Insert patterns. Duplicate patterns share a terminal state.
    for pattern_id, pattern in enumerate(patterns):
        state = 0

        for ch in pattern:
            next_state = transitions[state].get(ch)

            if next_state is None:
                next_state = len(transitions)
                transitions[state][ch] = next_state
                transitions.append({})
                failure.append(0)
                terminal.append([])

            state = next_state

        terminal[state].append(pattern_id)

    # Build failure links using BFS.
    from collections import deque

    queue = deque()
    bfs_order = [0]

    for child in transitions[0].values():
        failure[child] = 0
        queue.append(child)

    while queue:
        state = queue.popleft()
        bfs_order.append(state)

        for ch, child in transitions[state].items():
            fallback = failure[state]

            while fallback and ch not in transitions[fallback]:
                fallback = failure[fallback]

            failure[child] = transitions[fallback].get(ch, 0)
            queue.append(child)

    # Search each text independently.
    all_counts = []

    for text in texts:
        visits = [0] * len(transitions)
        state = 0

        for ch in text:
            while state and ch not in transitions[state]:
                state = failure[state]

            state = transitions[state].get(ch, 0)
            visits[state] += 1

        # Propagate visits to failure states in reverse BFS order.
        for node in reversed(bfs_order[1:]):
            visits[failure[node]] += visits[node]

        row = [0] * pattern_count

        for node, pattern_ids in enumerate(terminal):
            for pattern_id in pattern_ids:
                row[pattern_id] = visits[node]

        all_counts.append(row)

    return {"counts": all_counts}
