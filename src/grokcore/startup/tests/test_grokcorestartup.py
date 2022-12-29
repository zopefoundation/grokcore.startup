import doctest
import os
import unittest


optionflags = doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE

main_doctests = ['README.txt']


def test_suite():
    suite = unittest.TestSuite()

    for testfile in main_doctests:
        suite.addTest(
            doctest.DocFileSuite(
                os.path.join('..', testfile),
                optionflags=optionflags,
                globs=globals()))
    return suite
