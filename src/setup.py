#! /usr/bin/env python
#
# Edward Loper's API Documentation Generation Tool
#
# Created [05/27/01 09:04 PM]
# Edward Loper
#

from distutils.core import setup
import re, sys, epydoc

VERSION = str(epydoc.__version__)
(AUTHOR, EMAIL) = re.match('^(.*?)\s*<(.*)>$', epydoc.__author__).groups()
URL = epydoc.__url__
LICENSE = epydoc.__license__
KEYWORDS='docstring restructuredtext rst javadoc docformat pydoc epydoc'
LONG_DESCRIPTION = """\
Epydoc is a tool for generating API documentation documentation for
Python modules, based on their docstrings.  For an example of epydoc's
output, see the API documentation for epydoc itself (`html
<http://epydoc.sf.net/api/>`__\ , `pdf
<http://epydoc.sf.net/epydoc.pdf>`__\ ).  A lightweight markup
language called `epytext <http://epydoc.sf.net/epytextintro.html>`__
can be used to format docstrings, and to add information about
specific fields, such as parameters and instance variables.  Epydoc
also understands docstrings written in `reStructuredText
<http://docutils.sourceforge.net/rst.html>`__\ , Javadoc, and
plaintext. For a more extensive example of epydoc's output, see the
API documentation for `Python 2.5
<http://epydoc.sourceforge.net/stdlib/>`__\ ."""
CLASSIFIERS=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Topic :: Documentation',
    'Topic :: Software Development :: Documentation',
    ]

# Classifiers metadata only supported for Python 2.4+
if sys.version_info[:2] >= (2,4):
    other_metadata = dict(classifiers=CLASSIFIERS)
else:
    other_metadata = {}

if '--format=wininst' in sys.argv:
    SCRIPTS = ['scripts/epydoc.pyw', 'scripts/epydoc.py']
else:
    SCRIPTS = ['scripts/epydoc', 'scripts/epydocgui']

SCRIPTS.append('scripts/apirst2html.py')

setup(name="epydoc",
      description="Edward Loper's API Documentation Generation Tool",
      version=VERSION,
      author=AUTHOR,
      author_email=EMAIL,
      license=LICENSE,
      url=URL,
      scripts=SCRIPTS,
      keywords=KEYWORDS.split(),
      long_description=LONG_DESCRIPTION,
      packages=['epydoc', 'epydoc.markup', 'epydoc.test', 'epydoc.docwriter'],
      **other_metadata)

