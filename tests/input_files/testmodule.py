"""This is a test docstring."""

from copy import deepcopy
import copy
from os.path import abspath
import sys
import os.path

from tests import blank_parse_docstring_return, blank_parse_class_return

class _TestClass2():
    pass

class TestClass1():
    """This class does one classy thing."""
    def __init__(self, arg1):
        pass

def test_func3():   # Intentionally out of order to check how it gets pulled in
    pass

def test_func1():
    pass

def test_func2():
    pass

somevariable = 42

__someothervariable__ = "Hello world"