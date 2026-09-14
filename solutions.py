"""Runnable examples for Class 0; run with Python 3.11+ and no dependencies."""

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from math import isclose
from random import Random
from statistics import median


def sum_numbers(numbers: Iterable[int]) -> int:
    """Task 2: accumulate rather than overwrite."""
    total = 0
    for number in numbers:
        total += number
    return total


def linear_search(numbers: Iterable[int], target: int) -> int:
    """Task 6: return the first matching index, or -1 if absent."""
    for index, number in enumerate(numbers):
        if number == target:
            return index
    return -1


def binary_search(numbers: Sequence[int], target: int) -> int:
    """Task 6: input must be sorted ascending; return an index or -1."""
    left = 0
    right = len(numbers) - 1
    while left <= right:
        middle = (left + right) // 2
        if numbers[middle] == target:
            return middle
        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


def streaming_max(numbers: Iterable[int]) -> int:
    """Task 7: consume any iterable once using constant extra memory."""
    iterator = iter(numbers)
    try:
        largest = next(iterator)
    except StopIteration:
        raise ValueError("Cannot find a maximum of empty input") from None
    for number in iterator:
        if number > largest:
            largest = number
    return largest


def count_letters(letters: Iterable[str]) -> dict[str, int]:
    """Task 8: count occurrences with a dictionary."""
    counts: dict[str, int] = {}
    for letter in letters:
        counts[letter] = counts.get(letter, 0) + 1
    return counts


@dataclass(frozen=True)
class MarkStatistics:
    count: int
    minimum: int
    maximum: int
    total: int
    average: float
    median: float
    count_at_least_90: int
    count_below_40: int


def build_mark_histogram(marks: Iterable[int]) -> list[int]:
    """Task 16: read marks once; retain only 101 frequency counters."""
    frequency = [0] * 101
    for mark in marks:
        if type(mark) is not int or not 0 <= mark <= 100:
            raise ValueError("Each mark must be an integer from 0 to 100")
        frequency[mark] += 1
    return frequency


def validate_histogram(frequency: Sequence[int]) -> None:
    if len(frequency) != 101:
        raise ValueError("A mark histogram must have exactly 101 counters")
    if any(type(count) is not int or count < 0 for count in frequency):
        raise ValueError("Histogram counters must be nonnegative integers")


def summarize_histogram(frequency: Sequence[int]) -> MarkStatistics:
    """Find all statistics by scanning the small histogram, not the input."""
    validate_histogram(frequency)
    count = 0
    total = 0
    minimum = 101
    maximum = -1
    count_at_least_90 = 0
    count_below_40 = 0

    for mark, occurrences in enumerate(frequency):
        if occurrences == 0:
            continue
        count += occurrences
        total += mark * occurrences
        minimum = min(minimum, mark)
        maximum = mark
        if mark >= 90:
            count_at_least_90 += occurrences
        if mark < 40:
            count_below_40 += occurrences

    if count == 0:
        raise ValueError("Cannot summarize an empty dataset")

    lower_position = (count + 1) // 2
    upper_position = (count + 2) // 2
    cumulative = 0
    lower_value: int | None = None
    upper_value = 0
    for mark, occurrences in enumerate(frequency):
        cumulative += occurrences
        if lower_value is None and cumulative >= lower_position:
            lower_value = mark
        if cumulative >= upper_position:
            upper_value = mark
            break

    assert lower_value is not None
    return MarkStatistics(
        count=count,
        minimum=minimum,
        maximum=maximum,
        total=total,
        average=total / count,
        median=(lower_value + upper_value) / 2,
        count_at_least_90=count_at_least_90,
        count_below_40=count_below_40,
    )


def summarize_marks(marks: Iterable[int]) -> MarkStatistics:
    return summarize_histogram(build_mark_histogram(marks))


def merge_histograms(histograms: Iterable[Sequence[int]]) -> list[int]:
    """Merge independent chunks without retaining every chunk histogram."""
    combined = [0] * 101
    for frequency in histograms:
        validate_histogram(frequency)
        for mark, occurrences in enumerate(frequency):
            combined[mark] += occurrences
    return combined


def run_checks() -> None:
    """Check calculations and compare histogram results with a sorting oracle."""
    x = 5
    y = 2
    x = x + y
    y = x * 2
    x = y - x
    assert (x, y) == (7, 14)
    assert sum_numbers([10, 20, 30, 40, 50]) == 150
    assert sum_numbers([]) == 0
    assert sum(1 for _ in range(10) for _ in range(10)) == 100
    assert 1000 * 1000 == 1_000_000
    assert 10 * 1_000_000 == 10_000_000

    numbers = [3, 8, 12, 17, 24, 31, 45, 51, 63]
    for search in (linear_search, binary_search):
        for index, target in enumerate(numbers):
            assert search(numbers, target) == index
        for target in (-1, 13, 100):
            assert search(numbers, target) == -1
        assert search([], 45) == -1
    assert streaming_max(iter([-9, -2, -7])) == -2
    assert streaming_max([5]) == 5
    assert count_letters("A B A C B A D C A B".split()) == {
        "A": 4, "B": 3, "C": 2, "D": 1
    }

    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    addition = [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]
    product = [
        [sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)]
        for i in range(2)
    ]
    assert addition == [[6, 8], [10, 12]]
    assert product == [[19, 22], [43, 50]]
    new_time = 50 + (2 + 2 + 3 + 2) / 10
    assert isclose(new_time, 50.9)
    assert isclose(59 / new_time, 1.1591355599214146)

    samples = [
        [0], [100], [55] * 7, [0, 100], [39, 40, 89, 90],
        [0, 39, 40, 90, 100, 100], [0, 0, 0, 100],
    ]
    random = Random(0)
    samples.extend(
        [random.randrange(101) for _ in range(size)]
        for size in range(1, 201)
    )
    for marks in samples:
        # A one-shot iterator checks that the algorithm does not reread input.
        actual = summarize_marks(iter(marks))
        expected = MarkStatistics(
            count=len(marks), minimum=min(marks), maximum=max(marks),
            total=sum(marks), average=sum(marks) / len(marks),
            median=float(median(marks)),
            count_at_least_90=sum(mark >= 90 for mark in marks),
            count_below_40=sum(mark < 40 for mark in marks),
        )
        assert actual == expected
        chunk_histograms = (
            build_mark_histogram(marks[start:start + 7])
            for start in range(0, len(marks), 7)
        )
        assert summarize_histogram(merge_histograms(chunk_histograms)) == actual

    for invalid_marks in ([], [-1], [101], [2.5], [True], ["90"]):
        try:
            summarize_marks(invalid_marks)
        except ValueError:
            pass
        else:
            raise AssertionError(f"Accepted invalid marks: {invalid_marks}")
    try:
        streaming_max([])
    except ValueError:
        pass
    else:
        raise AssertionError("Accepted an empty maximum input")

    # Check the two middle ranks at the requested scale without storing marks.
    large_frequency = [0] * 101
    large_frequency[0] = 5_000_000
    large_frequency[100] = 5_000_000
    assert summarize_histogram(large_frequency) == MarkStatistics(
        count=10_000_000, minimum=0, maximum=100, total=500_000_000,
        average=50.0, median=50.0,
        count_at_least_90=5_000_000, count_below_40=5_000_000,
    )


if __name__ == "__main__":
    run_checks()
    print("All checks passed.")
    example_marks = [0, 39, 40, 90, 100, 100]
    print(f"Task 16 example marks: {example_marks}")
    print(summarize_marks(iter(example_marks)))
