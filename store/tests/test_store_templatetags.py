import pytest

from store.templatetags.divide import divide_partition, divide_remainder


def test_divide_partition():
    assert divide_partition(10, 2) == 5
    assert not divide_partition(2, 0)
    assert not divide_partition("abc", 0)


def test_divide_remainder():
    assert divide_remainder(5, 2) == "Yes"
    assert divide_remainder(4, 2) == "No"
    assert not divide_remainder(2, 0)
    assert not divide_remainder("test", 3)
