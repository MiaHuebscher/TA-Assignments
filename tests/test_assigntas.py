import pytest
import assign_tas as ata
import pandas as pd
import numpy as np


@pytest.fixture
def cases():
    """Load data from csv files and return as tuple"""
    t1 = np.array(pd.read_csv('test1.csv', header=None))
    t2 = np.array(pd.read_csv('test2.csv', header=None))
    t3 = np.array(pd.read_csv('test3.csv', header=None))
    return t1, t2, t3


def test_overallocation(cases):
    test1, test2, test3 = cases

    assert ata.overallocation(test1) == 37, "Incorrect overallocation score for test 1"
    assert ata.overallocation(test2) == 41, "Incorrect overallocation score for test 2"
    assert ata.overallocation(test3) == 23, "Incorrect overallocation score for test 3"


def test_conflicts(cases):
    test1, test2, test3 = cases

    assert ata.conflicts(test1) == 8, "Incorrect conflicts score for test 1"
    assert ata.conflicts(test2) == 5, "Incorrect conflicts score for test 2"
    assert ata.conflicts(test3) == 2, "Incorrect conflicts score for test 3"


def test_undersupport(cases):
    test1, test2, test3 = cases

    assert ata.undersupport(test1) == 1, "Incorrect undersupport score for test 1"
    assert ata.undersupport(test2) == 0, "Incorrect undersupport score for test 2"
    assert ata.undersupport(test3) == 7, "Incorrect undersupport score for test 3"


def test_unwilling(cases):
    test1, test2, test3 = cases

    assert ata.unwilling(test1) == 53, "Incorrect unwilling score for test 1"
    assert ata.unwilling(test2) == 58, "Incorrect unwilling score for test 2"
    assert ata.unwilling(test3) == 43, "Incorrect unwilling score for test 3"


def test_unpreferred(cases):
    test1, test2, test3 = cases

    assert ata.unpreferred(test1) == 15, "Incorrect unpreferred score for test 1"
    assert ata.unpreferred(test2) == 19, "Incorrect unpreferred score for test 2"
    assert ata.unpreferred(test3) == 10, "Incorrect unpreferred score for test 3"

