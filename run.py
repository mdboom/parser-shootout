# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import test_pyparsing
import test_ply

from numpy.testing import assert_allclose


def get_inputs():
    return [
        ('34d23m15s', ((34, 23, 15), 'degree')),
        ('34d23m', ((34, 23, 0), 'degree')),
        ('54.12412', (54.12412, None)),
        ('-54:07:26.832', ((-54, 7, 26.832), None)),
        ('54.12412 deg', (54.12412, 'degree')),
        ('54.12412 degrees', (54.12412, 'degree')),
        ("54.12412°", (54.12412, 'degree')),
        ("54°07'26.832\"", ((54, 7, 26.832), 'degree')),
        ('3h36m29.7888s', ((3, 36, 29.7888), 'hourangle')),
        ('54:07', ((54, 7, 0), None)),
        ('54 07 32', ((54, 7, 32), None)),]



inputs = get_inputs()

def get_test(func):
    def test():
        for s, expect in inputs:
            try:
                result = func(s)
                assert_allclose(result[0], expect[0])
                assert result[1] == expect[1]
            except:
                print("{0} failed.".format(s))
                raise

    return test

if __name__ == "__main__":
    test_modules = [
        test_pyparsing,
        test_ply]

    import timeit
    for module in test_modules:
        test = get_test(module.test)
        t = timeit.timeit(test, number=1000)
        print("{0}: {1}s".format(module.__name__, t))
