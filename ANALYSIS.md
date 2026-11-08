# Assignment 4 — Algorithm Analysis

## 1. Longest Common Subsequence (LCS)

**Idea**

The algorithm finds the longest sequence of characters that appears in both strings in the same order. The characters do not need to be next to each other.

**Dynamic programming**

`dp[i][j]` stores the length of the LCS of the first `i` characters of string `a` and the first `j` characters of string `b`.

Base cases:
- `dp[0][j] = 0`
- `dp[i][0] = 0`

Transitions:
- If `a[i-1] == b[j-1]`, then `dp[i][j] = dp[i-1][j-1] + 1`.
- Otherwise, `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`.

After filling the table, the algorithm moves backwards through it to reconstruct one optimal subsequence. When characters match, it adds the character and moves diagonally. Otherwise, it moves to the neighbouring state with the larger value.

**Correctness**

Each state considers the optimal subsequence for two prefixes. Matching characters can extend an optimal solution for the shorter prefixes. When characters differ, an optimal solution must exclude at least one of the two final characters. Therefore, taking the maximum of the two previous states is correct. Backtracking follows these same decisions and reconstructs an optimal subsequence.

**Complexity**

- Time: O(n × m)
- Auxiliary memory: O(n × m)

## 2. Ordered Adjacent-Block Merging

**Idea**

The algorithm finds the minimum total cost of merging all blocks. Only adjacent blocks can be merged, so their original order must be preserved.

**Interval dynamic programming**

`dp[l][r]` stores the minimum cost of merging all blocks from index `l` to index `r` into one block.

A prefix-sum array calculates the total size of any interval in constant time.

Base case:

`dp[i][i] = 0`

Transition:

`dp[l][r] = min(dp[l][k] + dp[k+1][r] + sum(l, r))`

The algorithm checks every possible last split `k`.

**Reconstruction**

The split table remembers the best split for every interval. The algorithm first reconstructs the left and right intervals, then adds their merge operation. This produces a chronological valid plan in which both smaller blocks exist before they are merged.

Each operation is represented by `[l, k, r]`, meaning that intervals `[l, k]` and `[k+1, r]` are merged.

**Correctness**

The final merge of an interval must divide it into two adjacent intervals. Both intervals must already be merged optimally before the final operation. Checking every possible split therefore considers every valid final merge and selects the cheapest one.

**Complexity**

- Time: O(n³)
- Auxiliary memory: O(n²)

## 3. Maximum-Weight Independent Set on a Tree

**Idea**

The algorithm selects vertices with maximum total weight. Two connected vertices cannot both be selected. The empty set is allowed, so negative weights do not force the algorithm to select a vertex.

**Tree dynamic programming**

For each vertex `u`, two values are calculated:

- `take[u]`: best weight when vertex `u` is selected.
- `skip[u]`: best weight when vertex `u` is not selected.

Transitions:

`take[u] = weight[u] + sum(skip[child])`

`skip[u] = sum(max(take[child], skip[child]))`

The tree is traversed iteratively. Processing vertices in reverse traversal order ensures that child values are calculated before their parent.

**Reconstruction**

The algorithm starts at the root. If the parent was selected, the current vertex must be skipped. Otherwise, it selects the current vertex only when `take[u]` is strictly greater than `skip[u]`. It then applies the same rule to its children.

An iterative traversal avoids Python recursion limits on deep trees.

**Correctness**

For a selected vertex, every child must be skipped. For a skipped vertex, each child can either be selected or skipped, whichever gives a larger value. These are all possible valid choices in a tree. Thus, the two states calculate the optimum for every subtree.

**Complexity**

- Time: O(n)
- Auxiliary memory: O(n)

## 4. Exact String Searching

All three algorithms return every zero-based starting position where the pattern occurs. Overlapping occurrences are included. An empty pattern matches every boundary from `0` to `n`.

### 4.1 Naive Search

**Idea**

The algorithm checks the pattern at every possible starting position in the text. It compares characters one by one and reports a position only if the complete pattern matches.

**Correctness**

Every valid starting position is checked. A position is reported only when all pattern characters match. Therefore, every reported position is valid, and no valid occurrence is missed.

**Complexity**

- Time: O(n × m + n + 1)
- Auxiliary memory: O(1), excluding output

### 4.2 Knuth-Morris-Pratt (KMP)

**Idea**

KMP uses a prefix function to avoid comparing characters that are already known to match.

`pi[i]` stores the length of the longest proper prefix of the pattern that is also a suffix ending at position `i`.

When a mismatch happens, the algorithm uses the prefix function to find the next possible matching prefix. After a full match, it also uses this fallback to preserve overlapping occurrences.

**Correctness**

The prefix function identifies the longest prefix that can still match after a mismatch. No possible occurrence is skipped because all shorter valid borders are considered through repeated fallback. After a complete match, the same rule preserves overlaps.

**Complexity**

- Time: O(n + m + z)
- Auxiliary memory: O(m), excluding output

### 4.3 Rabin-Karp (RK)

**Idea**

Rabin-Karp calculates polynomial hashes for the pattern and each text window. It uses base `31` and modulus `101`.

The next window hash is calculated from the previous hash by removing the outgoing character, multiplying by the base, and adding the incoming character.

Equal hashes are only candidates. The algorithm compares the actual characters before reporting a match because different strings can have the same hash.

**Correctness**

Every possible window is checked. Unequal hashes cannot represent equal strings under the same hash function. Equal hashes are verified character by character, so collisions never create false matches.

**Complexity**

- Expected practical performance: depends on the number of hash collisions.
- Worst-case time: O(n × m)
- Auxiliary memory: O(1), excluding output

## 5. Suffix Array and Kasai LCP

**Idea**

The suffix array stores the starting positions of all non-empty suffixes in lexicographical order.

**Prefix doubling**

Initially, suffixes are ranked by their first character. The algorithm repeatedly sorts suffixes using pairs of ranks representing prefixes of increasing lengths. It stops when every suffix has a unique rank.

**Kasai LCP**

The LCP array stores the common-prefix length of each suffix and the previous suffix in suffix-array order. Kasai's algorithm uses the previous comparison to avoid repeating character comparisons.

`lcp[0] = 0`.

**Longest repeated substring**

The longest repeated substring is found by taking the maximum LCP value. Its corresponding suffix provides the substring.

**Correctness**

Sorting by rank pairs progressively compares longer prefixes. Once all ranks are unique, their order is the lexicographical suffix order. Kasai computes the common prefix of every adjacent pair. Any repeated substring is a prefix shared by at least two suffixes, and the maximum such length is found between an adjacent pair in sorted order.

**Complexity**

- Prefix doubling: O(n log² n)
- Kasai LCP: O(n)
- Auxiliary memory: O(n)

## 6. Aho-Corasick

**Idea**

Aho-Corasick searches for many patterns in several texts using one trie and failure links.

**Construction**

All patterns are inserted into a trie. Each node represents a prefix. Failure links point to the longest suffix of the current prefix that is also a trie prefix.

Failure links are constructed using breadth-first search.

Duplicate patterns share the same terminal state but retain their separate dictionary positions.

**Searching and counting**

Each text is processed independently, starting from the root. The algorithm counts visits to automaton states while scanning the text.

After scanning, visit counts are propagated in reverse breadth-first order through failure links. This also counts patterns that end as suffixes of longer matched patterns.

The final row follows the original dictionary order.

**Correctness**

Every pattern match corresponds to a terminal state that is either the current state or a failure-link ancestor. Propagating visits from each state to its failure state counts all these matches. Shared terminal states correctly give equal counts to duplicate patterns.

**Complexity**

Let `L` be the total pattern length, `S` the number of trie states, `p` the number of patterns and `n` the text length.

- Construction: O(L + 95S + p)
- Each text: O(n + S + p)
- Auxiliary memory: O(95S + p), excluding output

## 7. Testing and Verification

The implementation was designed to cover:
- Empty strings and empty arrays.
- Overlapping string matches.
- Hash collisions in Rabin-Karp.
- Negative vertex weights.
- Trees with deep paths.
- Duplicate patterns in Aho-Corasick.
- Independent processing of multiple texts.
- Alternative optimal solutions where reconstruction is not unique.

The student test suite checks representative examples and important boundary cases.

Run the tests with:

```bash
python -m unittest discover -s tests/student -v
```

Run the official public checks with:

```bash
python tools/run.py --check
```

## 8. Search Algorithm Comparison

Naive search, KMP and Rabin-Karp solve the same exact matching problem but use different methods.

- Naive search is simple but may repeat many character comparisons.
- KMP uses prefix information and has linear search time.
- Rabin-Karp uses rolling hashes. It is efficient when few windows have matching hashes, but collisions require exact verification and can increase its running time.

The implementations can be compared on the same text and pattern. Their returned positions must be identical. The benchmark script uses a fixed input and reports elapsed time for each method.

## 9. Tools and Acknowledgements

Language: Python 3.12+.

The project uses the supplied JSON Lines launcher and public validation tools.

AI assistance was used to help develop and review algorithm implementations, tests and explanations. The student should review the code, run the tests locally, understand the algorithms and verify the final submitted commit.
