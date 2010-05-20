import os
import re
import unittest
from zope.testing import doctest, renormalizing

checker = renormalizing.RENormalizing([
    # str(Exception) has changed from Python 2.4 to 2.5 (due to
    # Exception now being a new-style class).  This changes the way
    # exceptions appear in traceback printouts.
    (re.compile(r"ConfigurationExecutionError: <class '([\w.]+)'>:"),
                r'ConfigurationExecutionError: \1:'),
    ])

optionflags=(doctest.ELLIPSIS+
            doctest.NORMALIZE_WHITESPACE)

main_doctests = ['README.txt']

def test_suite():
    suite = unittest.TestSuite()

    for testfile in main_doctests:
        suite.addTest(
            doctest.DocFileSuite(
                os.path.join('..', testfile),
                optionflags=optionflags,
                globs=globals(),
                checker=checker))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
