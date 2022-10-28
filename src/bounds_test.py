"""Testing bounds."""

from bounds import lower_bound, upper_bound
from random import randint


def test_bounds() -> None:
    """
    Test lower_bound and upper_bound.

    Test that if we extract the range from lower to upper bound,
    we get the block we are searching for.
    """
    x = [randint(0, 5) for _ in range(10)]
    x.sort()
    for i in range(10):
        query = x[lower_bound(x, i):upper_bound(x, i)]
        for q in query:
            assert i == q
