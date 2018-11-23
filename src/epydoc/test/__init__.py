# epydoc -- Regression testing
#
# Copyright (C) 2005 Edward Loper
# Author: Edward Loper <edloper@loper.org>
# URL: <http://epydoc.sf.net>
#
# $Id: __init__.py 1502 2007-02-14 08:38:44Z edloper $

"""
Regression testing.
"""

from __future__ import absolute_import
from __future__ import print_function

__docformat__ = 'epytext en'

import unittest, doctest, epydoc, os, os.path, re, sys

# Python 2/3 compatibility
from epydoc.seven import six

def main():
    try:
        addflag = doctest.register_optionflag
    except:
        print("\n"
             "The regression test suite requires a more recent version of\n"
             "doctest (e.g., the version that ships with Python 2.4 or 2.5).\n"
             "Please place a new version of doctest on your path before \n"
             "running the test suite.\n")
        return

    py_versions = [
            (2, 4),
            (2, 5),
            (2, 7),
            (3, 0),
            (3, 4),
            (3, 5),
            (3, 6),
            (3, 7)
    ]

    # converts tuple to dotted version string
    def t2v(t): return '.'.join([str(x) for x in t])

    # Define PYTHON#.# and PYMIN#.# option flags
    py_min_flags = [
        (addflag('PYTHON%s' % t2v(x)), x) for x in py_versions
    ] + [
        (addflag('PYMIN%s' % t2v(x)), x) for x in py_versions
    ]

    # Define PYMAX#.# option flags
    py_max_flags = [
        (addflag('PYMAX%s' % t2v(x)), x) for x in py_versions
    ]

    class DocTestParser(doctest.DocTestParser):
        """
        Custom doctest parser that adds support for required-python flags
        +PYTHON2.4, +PYTHON2.4, +PYTHON2.7, +PYTHON3.0, etc...
        """
        def parse(self, string, name='<string>'):
            pieces = doctest.DocTestParser.parse(self, string, name)
            for i, val in enumerate(pieces):
                if (isinstance(val, doctest.Example) and
                        not self.py_version_suitable(val)):
                    pieces[i] = doctest.Example('1', '1')
            return pieces

        def py_version_suitable(self, example):
            for item in py_min_flags:
                if (example.options.get(item[0], False) and
                    sys.version_info < item[1]):
                    return False
            for item in py_max_flags:
                if (example.options.get(item[0], False) and
                    sys.version_info > item[1]):
                    return False
            return True



    # Turn on debugging.
    epydoc.DEBUG = True

    # Options for doctest:
    options = doctest.ELLIPSIS
    doctest.set_unittest_reportflags(doctest.REPORT_UDIFF)

    # Use a custom parser
    parser = DocTestParser()

    # Find all test cases.
    tests = []
    here = os.path.dirname(__file__)
    testdirs = [here, os.path.join(here, 'py2' if six.PY2 else 'py3')]
    for testdir in testdirs:
        for filename in os.listdir(testdir):
            filepath = os.path.join(testdir, filename)
            if (filename.endswith('.doctest') and
                check_requirements(filepath)):
                relpath = os.path.relpath(filepath, here)
                tests.append(doctest.DocFileSuite(relpath,
                                                  optionflags=options,
                                                  parser=parser))

    # Run all test cases.
    unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(tests))

def check_requirements(filename):
    """
    Search for strings of the form::

        [Require: <module>]

    If any are found, then try importing the module named <module>.
    If the import fails, then return False.  If all required modules
    are found, return True.  (This includes the case where no
    requirements are listed.)
    """
    s = open(filename).read()
    for m in re.finditer('(?mi)^[ ]*\:RequireModule:(.*)$', s):
        module = m.group(1).strip()
        try:
            __import__(module)
        except ImportError:
            print(('Skipping %r (required module %r not found)' %
                   (os.path.split(filename)[-1], module)))
            return False
    return True


if __name__=='__main__':
    main()
