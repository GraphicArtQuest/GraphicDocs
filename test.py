"""
Runs the unit tests JSDoc-For-Python.

The test classes are imported individually, but do not need additional references. Running unittest.main()
takes care of running all tests.
"""
import os
import unittest

from tests.test_parse_docstring_example import TestParseDocstring_Examples
from tests.test_parse_docstring_global import TestParseDocstring_Global
from tests.test_parse_docstring_ignore import TestParseDocstring_Ignore
from tests.test_parse_docstring_param import TestParseDocstring_Param
from tests.test_parse_docstring_private import TestParseDocstring_Private
from tests.test_parse_docstring_public import TestParseDocstring_Public
from tests.test_parse_docstring_returns import TestParseDocstring_Returns
from tests.test_parse_docstring_throws import TestParseDocstring_Throws
from tests.test_parse_docstring import TestParseDocstring

if __name__ == '__main__':
    unittest.main()