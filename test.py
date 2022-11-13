"""
Runs the unit tests JSDoc-For-Python.

The test classes are imported individually, but do not need additional references. Running unittest.main()
takes care of running all tests.
"""
import os
import unittest

from tests.test_parse_docstring_param import TestParseDocstring_Param
from tests.test_parse_docstring import TestParseDocstring

if __name__ == '__main__':
    unittest.main()