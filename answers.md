# Parallel Computing - Class 0 Diagnostic

Solutions to Tasks 1-16. Python examples and executable checks are in
`solutions.py`. Run them with `python solutions.py` (Python 3.11+, standard
library only). The examples use small inputs; no actual dataset of 10 million
marks was supplied.

## Task 1 - Trace the Code

Assignments use the current values of the variables, including earlier updates.

| Statement | x afterward | y afterward |
| --- | ---: | ---: |
| `x = 5` | 5 | Not assigned yet |
| `y = 2` | 5 | 2 |
| `x = x + y` | 7 | 2 |
| `y = x * 2` | 7 | 14 |
| `x = y - x` | 7 | 14 |
| `print(x, y)` | 7 | 14 |

Final output: `7 14`.

## Task 2 - Find the Bug

`total = numbers[i]` replaces the previous value on every iteration. Therefore,
the program prints the last element, `50`, rather than a sum. It was probably
intended to calculate `10 + 20 + 30 + 40 + 50 = 150`.

Fix: accumulate instead of replacing the total.

```python
numbers = [10, 20, 30, 40, 50]
total = 0
for number in numbers:
    total += number
print(total)  # 150
```

This takes O(n) time and O(1) extra memory. `sum(numbers)` is a shorter alternative.

## Task 3 - Nested Loops

For each outer iteration, the entire inner loop runs. Multiply the iteration
counts to obtain the number of calls to `print`.

| Case | Calculation | Print executions |
| --- | --- | ---: |
| a: Both loops run 10 times | 10 * 10 | 100 |
| b: Both run from 0 through 999 | 1,000 * 1,000 | 1,000,000 |
| c: Outer 10, inner 1,000,000 | 10 * 1,000,000 | 10,000,000 |

For general loop lengths a and b, the work is O(a * b), or O(n^2) when both
lengths are n. Printing this much output may dominate execution time.

## Task 4 - Which Is Faster?

Algorithm A visits n elements: O(n) time. Algorithm B compares n elements against
n elements: n^2 comparisons and O(n^2) time, assuming all ordered pairs are
checked, including each element against itself. If only distinct unordered
pairs are compared, there are n(n - 1)/2 comparisons, still O(n^2).

At n = 1,000,000, A makes about 1,000,000 visits and B makes 1,000,000,000,000
comparisons under the all-pairs interpretation. B has about one million times
as many basic operations. Actual elapsed time also depends on each operation's
cost, the implementation, and the hardware. B's work grows much faster.

## Task 5 - Complexity Ranking

From fastest-growing to slowest-growing, for sufficiently large n:

```text
2^n > n^2 > n log2(n) > n > log2(n) > 1
```

These correspond to exponential, quadratic, linearithmic, linear, logarithmic,
and constant growth. Exponential work quickly becomes impractical: adding one
to n doubles it. Quadratic work is also problematic for large inputs: doubling
n quadruples the work. O(n log n) and O(n) are much more scalable, although even
a linear scan can be costly on an enormous dataset. O(log n) and O(1) grow
slowly or do not grow with n; these rankings describe growth, not exact timings
for small inputs.

## Task 6 - Searching

The list is `[3, 8, 12, 17, 24, 31, 45, 51, 63]`.

1. **Order unknown: linear search.** Compare with 3, 8, 12, 17, 24, 31, then 45.
   Find 45 after 7 element checks, at zero-based index 6 (the seventh position).
   Worst-case time is O(n), best-case time O(1), and extra memory O(1).
2. **Known sorted: binary search.** Start with indices 0-8. The middle index is
   `(0 + 8) // 2 = 4`, containing 24. Since 45 > 24, keep indices 5-8. Their
   middle index is `(5 + 8) // 2 = 6`, containing 45. Find it in 2 middle-element
   checks. Each unsuccessful step discards about half the remaining candidates.
   Worst-case time is O(log n), best-case time O(1), and an iterative
   implementation uses O(1) extra memory.

Binary search requires sorted data and efficient access by index. Sorting an
unknown list first usually costs O(n log n), so it is not worthwhile just for
one search; it can be useful when many searches follow.

## Task 7 - Large Dataset

Read the first integer and store it as `largest`. For each subsequent integer,
replace `largest` if the new integer is larger. Initializing from the first
value, rather than zero, also works when all numbers are negative.

Every integer is examined once, with 499,999,999 comparisons for 500 million
values. Only the current maximum needs to be retained; the full dataset need
not be stored in memory. A file or other stream can supply the numbers one at
a time or in chunks. Keep the running maximum between chunks, or take the
maximum of all chunk maxima.

Time is O(n), with one pass over the original data. Extra working memory is
O(1) when streaming, or O(b) including an input buffer holding b values. An
empty input has no maximum; the code raises `ValueError` for it. Without extra
information about the data, skipping any value could miss the largest one.

## Task 8 - Counting

Use a dictionary mapping each letter to its count. Start with an empty
dictionary; for each letter, add 1 to its existing count, treating a missing
entry as zero.

```text
A -> 4
B -> 3
C -> 2
D -> 1
```

The counts add up to `4 + 3 + 2 + 1 = 10`, matching the input length. Dictionary
lookup and update take expected O(1) time, giving expected O(n) total time and
O(k) memory for k distinct letters. Here k = 4. If the alphabet is fixed in
advance, a small frequency array also works.

## Task 9 - Matrix Operations

Matrix addition adds corresponding entries:

```text
A + B = [[1 + 5, 2 + 6],
         [3 + 7, 4 + 8]]
      = [[6, 8],
         [10, 12]]
```

For matrix multiplication, each output entry is a row of A dotted with a
column of B:

```text
C[0][0] = 1*5 + 2*7 = 5 + 14  = 19
C[0][1] = 1*6 + 2*8 = 6 + 16  = 22
C[1][0] = 3*5 + 4*7 = 15 + 28 = 43
C[1][1] = 3*6 + 4*8 = 18 + 32 = 50

A * B = [[19, 22],
         [43, 50]]
```

The standard row-by-column method uses 4 output entries * 2 multiplications
each = **8 individual multiplications**, and 4 additions. For n-by-n matrices,
standard addition is O(n^2) and standard multiplication is O(n^3).

## Task 10 - CPU vs Memory

A fast CPU does not guarantee a fast scan of a huge array. Possible causes are:

- **Memory bandwidth:** RAM can deliver only a limited amount of data per
  second, so the CPU may consume values faster than memory supplies them.
- **Cache misses and memory latency:** a huge array does not fit in CPU caches.
  Fetching new cache lines takes time, especially when layout or access patterns
  prevent effective prefetching.
- **Insufficient RAM:** if the working set does not fit, paging data between RAM
  and storage can be far slower than reading RAM.
- **Interpreter and object overhead:** a Python loop performs interpreter work
  for each element; a Python list of integers holds references to objects, which
  is less compact than a packed numeric array.
- **Resource sharing:** other processes can compete for CPU time and memory
  bandwidth. A serial loop also cannot automatically use every available core.

The loop is still O(n); complexity alone does not determine its elapsed time.

## Task 11 - What Happens When You Run a Program?

For a typical Unix-like system, `./program` means run the file called `program`
in the current directory.

1. The **shell** reads the command and asks the operating system to start it,
   commonly by creating a child process and executing the file within it.
2. The **operating system** checks access permissions and the executable format.
   It creates or replaces the process's program image. A **process** is a running
   instance of a program, with its own execution state and virtual address space.
3. The executable's code and data are mapped into **memory**. The system sets up
   the stack, arguments, and environment. Required shared libraries are loaded
   or mapped too. Pages may be brought into RAM only when they are first used.
4. The scheduler gives the process CPU time. The **CPU** executes its
   instructions, reading and writing memory as needed.
5. The program makes **system calls** to request operating-system services such
   as reading a file or writing output. It may wait while an I/O request finishes.
6. Output is written to standard output, usually connected to the terminal, and
   becomes visible. Library buffering may delay it; redirection may send it to
   a file instead.
7. On normal completion, the program returns or calls an exit function. The
   operating system releases process resources and records an exit status.
   The shell collects the status and displays its prompt again for a foreground
   command.

If the file is a script, an interpreter may execute it instead of the file
containing native machine instructions directly.

## Task 12 - Four Programs

| Program | Likely limiting resource |
| --- | --- |
| A: lots of CPU work | CPU execution speed and available CPU time |
| B: lots of memory | RAM capacity; memory bandwidth or latency if it accesses that memory heavily |
| C: reads a large file | Storage throughput or latency, unless the data is already cached in RAM |
| D: waits for user input | Arrival of user input; it usually needs little CPU while waiting |

All four can be active **concurrently**. With multiple cores, several runnable
threads can execute at the same instant. A process blocked on input or disk I/O
usually sleeps, allowing another to use the CPU. Merely allocating lots of
memory does not prove that B is memory-bound; its actual access pattern matters.

CPU time is the time actually spent executing a process's instructions. It
depends on the amount of computation, scheduling priority, runnable competitors,
and available cores. Time waiting for I/O or user input contributes to elapsed
time but generally not to that process's CPU time.

With one CPU core, only one thread executes instructions at an instant under
the usual single-hardware-thread model. The operating system switches between
ready threads, so the four programs still make concurrent progress. CPU-heavy
jobs share the core and may take longer. Storage operations can still overlap
CPU work, and waiting processes need not occupy the core. Context switches also
have some overhead.

## Task 13 - The Slow Program

The claim is **not necessarily true**. "Twice as fast" must refer to the part
of the computer that limits this particular program. A CPU improvement does not
automatically double disk, network, database, or memory performance. Twice as
many cores does not halve a serial program's time either.

Let p be the fraction of the original time spent in work that becomes twice
as fast, with everything else unchanged and no new overhead. Then:

```text
new time = 10 * ((1 - p) + p/2) hours
```

If p = 1, the result is 5 hours. If only half the time benefits, p = 0.5 and
the result is `10 * (0.5 + 0.25) = 7.5 hours`. This is the idea behind Amdahl's
law: unchanged work limits the overall speedup. Measure the bottleneck before
predicting the effect of a hardware upgrade.

## Task 14 - Make It Faster

These are possibilities to evaluate, not changes that always help:

- **Profile first:** time each phase and inspect CPU use, memory use, I/O waits,
  and database query plans. Focus on the part consuming most of the 60 seconds.
- **Choose a better algorithm:** replace unnecessary all-pairs work with a
  linear scan, hashing, an index, or binary search where its assumptions hold.
- **Use suitable data structures:** use sets for repeated membership checks,
  dictionaries for lookup, and compact arrays for dense numeric data.
- **Avoid repeated work:** move invariant calculations outside loops, reuse
  computed results, and eliminate redundant scans or conversions.
- **Reduce allocation:** reuse buffers, avoid unnecessary copies and temporary
  objects, and process data in chunks when full materialization is unnecessary.
- **Improve memory access:** use contiguous layouts and sequential access, keep
  frequently used data compact, and avoid paging. Add RAM if capacity is limiting.
- **Reduce CPU overhead:** use efficient built-in operations or optimized
  compiled libraries; vectorize suitable numeric operations or compile measured
  hot loops. Use appropriate compiler optimizations for compiled code.
- **Improve I/O:** buffer and batch small reads/writes, avoid redundant file
  access, and reduce unnecessary network round trips. Use faster storage when
  storage is the limiting resource.
- **Improve database access:** add useful indexes, inspect query plans, fetch
  only necessary rows and columns, remove repeated per-row queries, batch work,
  and reuse connections. Account for index maintenance costs on writes.
- **Parallelize independent work:** split suitable tasks among cores or machines
  and combine results. Keep chunks large enough to amortize setup and transfer
  costs, balance the work, and minimize synchronization.
- **Overlap waiting and computation:** use asynchronous I/O, threads, or a
  pipeline when there is useful independent work during an I/O wait.
- **Cache repeated results:** memoize expensive pure calculations or cache
  unchanged data, with correct invalidation when inputs change.
- **Reduce contention:** shorten critical sections, avoid shared writable state
  when possible, and reduce competition from unrelated workloads.
- **Match hardware to the bottleneck:** a faster CPU, more cores, a GPU, faster
  RAM, or better storage helps only if the workload can use it effectively.

Retest with representative inputs and verify the result after each change.
Preserve required output, precision, ordering, and error behavior. For example,
reordering floating-point arithmetic can change a result even when the formula
looks equivalent. Faster execution must not depend on dropping required work.

## Task 15 - Bottleneck Identification

Assume the stages execute sequentially, so their times add.

```text
original total = 2 + 2 + 50 + 3 + 2 = 59 s
improved A    = 2 / 10 = 0.2 s
improved B    = 2 / 10 = 0.2 s
unchanged C   = 50 s
improved D    = 3 / 10 = 0.3 s
improved E    = 2 / 10 = 0.2 s
new total    = 0.2 + 0.2 + 50 + 0.3 + 0.2 = 50.9 s
speedup      = old time / new time = 59 / 50.9 = 1.1591...
```

The whole program is about **1.16 times as fast**, with elapsed time reduced by
`(59 - 50.9) / 59 * 100 = 13.73%`. Focus on C: it originally accounts for
`50 / 59 * 100 = 84.75%` of the runtime. Even eliminating A, B, D, and E
entirely would leave 50 seconds and cap the speedup at `59 / 50 = 1.18`.

## Task 16 - 10 Million Student Marks

### Algorithm and data structures

Marks are **integers from 0 through 100 inclusive**. Use a frequency array
`frequency` with 101 counters. Entry `frequency[v]` holds the number of marks
equal to v. There is no need to sort or retain the original marks.

1. Initialize all 101 counters to zero.
2. Read each mark once, validate its range and type, and increment its counter.
3. Scan the small frequency array to obtain:
   - Count: `n = sum(frequency)`.
   - Minimum: the first index whose counter is positive.
   - Maximum: the last index whose counter is positive.
   - Total: `sum(v * frequency[v] for v in range(101))`.
   - Average: `total / n`.
   - Number >= 90: `sum(frequency[90:101])`.
   - Number < 40: `sum(frequency[0:40])`.
4. Use cumulative counts to locate the median as described below.

The code calculates totals and threshold counts while scanning the frequency
array, then performs one further small scan for the median. This keeps the
per-input update simple. No numerical answers for the real cohort can be given
without the actual marks; this algorithm computes them when supplied.

### Median without sorting

Use one-based positions in the conceptual sorted sequence:

```text
lower position = (n + 1) // 2
upper position = (n + 2) // 2
```

Walk through marks 0 to 100, adding their frequencies to a cumulative count.
The first mark where the cumulative count reaches the lower position is the
lower middle value; do the same for the upper position. The median is their
average. For odd n the positions coincide, so the middle value is returned.

For n = 10,000,000 the middle positions are **5,000,000 and 5,000,001**. If they
contain different values, both values must be included. For example:

```text
marks:                    [0, 39, 40, 90, 100, 100]
nonzero frequencies:      0:1, 39:1, 40:1, 90:1, 100:2
cumulative counts:        1,   2,    3,    4,     6
middle positions:         3 and 4
middle values:            40 and 90
median:                   (40 + 90) / 2 = 65
total:                    0 + 39 + 40 + 90 + 100 + 100 = 369
average:                  369 / 6 = 61.5
minimum / maximum:        0 / 100
count >= 90 / count < 40:  3 / 2
```

### Passes, complexity, and memory

- **Original-data passes:** exactly one. Each mark is consumed once. Subsequent
  scans visit only the 101 counters and never reread the input.
- **Time:** O(n + k), where k = 101, hence O(n) for this fixed range.
- **Extra working memory:** O(k), hence O(1) relative to n. An input chunk of b
  marks adds O(b) buffer memory if chunks are materialized.
- **Storage estimate:** 101 packed unsigned 64-bit counters occupy
  `101 * 8 = 808 bytes`, plus a few scalar values. A Python list and Python
  integers have object overhead, so the supplied implementation uses more than
  808 bytes, but its histogram is still small and fixed in length.
- **Numeric limits:** the total is at most `10,000,000 * 100 = 1,000,000,000`.
  Python integers accumulate this exactly; the reported average uses floating
  point and may be rounded. Keep `(total, n)` if an exact rational average is
  needed. In fixed-width implementations, 64-bit counters and totals leave room
  for larger datasets.

The implementation raises `ValueError` for an empty dataset because minimum,
maximum, average, and median are undefined. It also rejects invalid marks.

### Likely bottleneck and optimizations

The histogram fits easily in cache. For a text file, reading and parsing marks
may dominate; in a Python loop, validation and interpreter overhead may
dominate if data is already in RAM. An optimized compiled version can become
limited by input or memory bandwidth. Profile to identify the actual limit.

Use buffered sequential reads, sensible chunk sizes, and avoid printing per
mark. Avoid unnecessary conversions or copies. When the input format permits,
store marks compactly (one unsigned byte can represent 0-100). A compiled or
vectorized histogram operation can reduce Python loop overhead; validate input
at the boundary and retain exactly the same accepted values and results. No
external numeric package is required for the supplied solution.

### Independent chunks and later parallelization

Give each worker a separate chunk and its own 101-counter array. After all
workers finish, merge by adding corresponding entries:

```text
global_frequency[v] = sum(worker_frequency[v] for each worker)
```

Calculate the final statistics from this merged array using the same algorithm.
Do **not** average chunk medians; medians cannot generally be combined that way.
For example, chunks `[0, 0, 0]` and `[100]` have medians 0 and 100: their median
average is 50, but the combined median is 0. Similarly, chunk averages must be
weighted by their counts; the merged histogram handles unequal chunks directly.

For p workers, input work is ideally about O(n/p) per worker; a serial merge
costs O(101 * p), and worker histograms use O(101 * p) total extra memory,
excluding input buffers. Actual speedup is limited by storage and memory
bandwidth, worker startup, data transfer, load imbalance, and the final merge.
Private arrays avoid contention on shared counters. For CPU-heavy Python loops
on a conventional GIL-enabled CPython build, processes or compiled operations
are preferable to expecting threads to provide CPU parallelism. The code
demonstrates chunk merging sequentially; a parallel runtime is a later option.
