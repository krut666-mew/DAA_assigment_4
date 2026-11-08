# Assignment 4 — Dynamic Programming and String Processing

## Overview

This project contains implementations of algorithms for Dynamic Programming and String Processing using Python.

The program supports multiple tasks through a JSON Lines (JSONL) interface. Each input line contains one task, and the program returns the corresponding result in JSON format.

## Implemented Algorithms

The project includes eight algorithms:

| Algorithm | Description |
|---|---|
| LCS | Finds the Longest Common Subsequence of two strings. |
| Merge | Finds the minimum cost of merging adjacent elements. |
| Tree | Solves the Maximum Weight Independent Set problem on a tree. |
| Naive Search | Finds all occurrences of a pattern using a basic search algorithm. |
| KMP | Uses the Knuth-Morris-Pratt algorithm for efficient pattern matching. |
| Rabin-Karp | Uses rolling hash to find pattern occurrences. |
| Suffix Array | Builds a suffix array and finds the longest repeated substring. |
| Aho-Corasick | Finds multiple patterns in texts using a trie and failure links. |

## Project Structure

```text
DAA_assignment_4/
│
├── Python/
│   └── source/
│       ├── algorithms.py
│       └── main.py
│
├── tests/
│   └── student/
│       ├── test_algorithms.py
│       └── benchmark_search.py
│
├── tools/
│   └── run.py
│
├── docs/
│   └── guide/
│       └── CONTRACTS.md
│
├── assignment.json
├── submission.json
└── README.md
```

## Technologies

- Python
- JSON
- Git and GitHub
- Python unittest

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/krut666-mew/DAA_assigment_4.git
```

### 2. Open the project directory

```bash
cd DAA_assigment_4
```

### 3. Run the program

Use the project runner:

```bash
python tools/run.py
```

### 4. Run Student Tests

```bash
python -m unittest discover -s tests/student -v
```

### 5. Run Public Tests

```bash
python tools/run.py --check
```

## Testing Results

The implementation was tested using student tests and the provided public test cases.

| Test Suite | Result |
|---|---:|
| Student Tests | 15/15 PASSED |
| Public Tests | 44/44 PASSED |
| State Reset Test | PASSED |

All tests passed successfully.

## Additional Features

- Supports multiple input requests.
- Handles empty strings and edge cases.
- Supports overlapping pattern matches.
- Handles duplicate patterns in Aho-Corasick.
- Uses iterative traversal for tree processing.
- Includes a benchmark script for search algorithms.

## Author

**Ansar Amantai**

Software Engineering

Astana IT University

---

## Conclusion

This assignment demonstrates the practical implementation of Dynamic Programming and String Processing algorithms in Python. The algorithms were tested with different input cases, including edge cases, and successfully passed all provided public tests.
