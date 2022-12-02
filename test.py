"""
Runs the unit tests JSDoc-For-Python.

The test classes are imported individually, but do not need additional references. Running unittest.main()
takes care of running all tests.
"""
import os
import unittest

from tests.test_parse_docstring_author import TestParseDocstring_Author
from tests.test_parse_docstring_copyright import TestParseDocstring_Copyright
from tests.test_parse_docstring_deprecated import TestParseDocstring_Deprecated
from tests.test_parse_docstring_example import TestParseDocstring_Examples
from tests.test_parse_docstring_global import TestParseDocstring_Global
from tests.test_parse_docstring_ignore import TestParseDocstring_Ignore
from tests.test_parse_docstring_license import TestParseDocstring_License
from tests.test_parse_docstring_memberof import TestParseDocstring_Memberof
from tests.test_parse_docstring_namespace import TestParseDocstring_Namespace
from tests.test_parse_docstring_param import TestParseDocstring_Param
from tests.test_parse_docstring_private import TestParseDocstring_Private
from tests.test_parse_docstring_public import TestParseDocstring_Public
from tests.test_parse_docstring_returns import TestParseDocstring_Returns
from tests.test_parse_docstring_throws import TestParseDocstring_Throws
from tests.test_parse_docstring_since import TestParseDocstring_Since
from tests.test_parse_docstring_todo import TestParseDocstring_Todo
from tests.test_parse_docstring_version import TestParseDocstring_Version
from tests.test_parse_docstring import TestParseDocstring

from tests.test_parse_function import TestParseFunction

from tests.test_parse_class import TestParseClass

from tests.test_parse_module import TestParseModule

from tests.core.test_core_config import TestCore

if __name__ == '__main__':
    unittest.main()