# Copyright (c) 2018 Pawel Tomulik
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Epydoc extensions to six module"""

from __future__ import absolute_import

__author__ = "Pawel Tomulik <ptomulik@meil.pw.edu.pl>"
__version__ = "0.0.1"

from epydoc import six

import textwrap

if six.PY3:
    def get_method_class(method):
        self = six.get_method_self(method)
        if self is not None:
            return self.__class__
        return None

    def cmp(a, b):
        return (a > b) - (a < b)

    exceptions = six.moves.builtins
else:
    def get_method_class(method):
        return method.im_class
    import exceptions

if six.binary_type is not str:
    def xdedent(s, *args):
        if isinstance(s, six.binary_type):
            s = s.decode(*args)
            s = textwrap.dedent(s)
            s = s.encode(*args)
        else:
            s = textwrap.dedent(s)
        return s
else:

    def xdedent(s, *args):
        return textwrap.dedent(s)


six.get_method_class = get_method_class
six.xdedent = xdedent
six.cmp = cmp
six.moves.exceptions = exceptions
