from copy import deepcopy
import os
import unittest

from tests.__init__ import blank_parse_docstring_return
from tests.input_files.testmodule import test_func1
from src.parser import parse_function

class TestParseFunction(unittest.TestCase):

    ###############################################################
    # Functions
    ###############################################################

    def test_nonfunctions_return_nothing(self):
        self.maxDiff = None
        
        inputs = [
            2,
            3.14159,
            False,
            True,
            {"a": "Some String"},
            ["A", "B", "C"],
            ["Some String"],
            ("A", "B", "C"),
            None
        ]

        for input in inputs:
            self.assertIsNone(parse_function(input))

    def test_simple_function(self):
        self.maxDiff = None
        
        def test_func():
            pass

        expected_parsed_function_return = {
            "name": "test_func",
            "docstring": None,
            "arguments": None,
            "returns": None
        }

        parsed_return_dict = parse_function(test_func)

        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_function_return["lineno"] = parsed_return_dict["lineno"]
        expected_parsed_function_return["sourcefile"] = parsed_return_dict["sourcefile"]

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_function_parse_arguments_basics(self):
        self.maxDiff = None
        
        def test_func(arg1, arg2: str, arg2a, arg3: bool=False, arg4: bool=True, arg5: float=2.5, arg6: int=733,
                        arg7:list[str | None]=['Hello', 'World!'], arg8:dict={"key1": True}):
            pass

        expected_parsed_function_return = {
            "name": "test_func",
            "docstring": None,
            "arguments": [
                {"name": "arg1", "type": None, "required": True, "default": None},
                {"name": "arg2", "type": str, "required": True, "default": None},
                {"name": "arg2a", "type": None, "required": True, "default": None},
                {"name": "arg3", "type": bool, "required": False, "default": False},
                {"name": "arg4", "type": bool, "required": False, "default": True},
                {"name": "arg5", "type": float, "required": False, "default": 2.5},
                {"name": "arg6", "type": int, "required": False, "default": 733},
                {"name": "arg7", "type": list[str | None], "required": False, "default": ['Hello', 'World!']},
                {"name": "arg8", "type": dict, "required": False, "default": {"key1": True}}
            ],
            "returns": None
        }

        parsed_return_dict = parse_function(test_func)

        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_function_return["lineno"] = parsed_return_dict["lineno"]
        expected_parsed_function_return["sourcefile"] = parsed_return_dict["sourcefile"]

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_function_with_docstring(self):
        self.maxDiff = None
        
        def test_func(arg1, arg2: str):
            """This function does some things.
            @param arg1 This is a description of arg1
            @param arg101 This is a nonsense argument, but it parses
            @since v2.0
            """
            pass

        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_docstring_return["description"] = "This function does some things."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"arg1": "This is a description of arg1"})
        expected_docstring_return["parameters"].append({"arg101": "This is a nonsense argument, but it parses"})
        expected_docstring_return["since"] = "v2.0"

        expected_parsed_function_return = {
            "name": "test_func",
            "docstring": None,
            "arguments": [
                {"name": "arg1", "type": None, "required": True, "default": None},
                {"name": "arg2", "type": str, "required": True, "default": None}
            ],
            "returns": None
        }
        expected_parsed_function_return["docstring"] = expected_docstring_return

        parsed_return_dict = parse_function(test_func)

        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_function_return["lineno"] = parsed_return_dict["lineno"]
        expected_parsed_function_return["sourcefile"] = parsed_return_dict["sourcefile"]

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_function_with_returns_annotation_and_returns_tag(self):
        self.maxDiff = None
        
        def test_func(arg1, arg2: str="Hello") -> str | bool:
            """This function does some things.

            @param arg1 This is a description of arg1
            @param arg2 This is a description of arg2
            @returns A string or boolean value of some sort...
            """
            pass

        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_docstring_return["description"] = "This function does some things."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"arg1": "This is a description of arg1"})
        expected_docstring_return["parameters"].append({"arg2": "This is a description of arg2"})
        expected_docstring_return["returns"] = "A string or boolean value of some sort..."

        expected_parsed_function_return = {
            "name": "test_func",
            "docstring": None,
            "arguments": [
                {"name": "arg1", "type": None, "required": True, "default": None},
                {"name": "arg2", "type": str, "required": False, "default": "Hello"}
            ],
            "returns": str | bool
        }
        expected_parsed_function_return["docstring"] = expected_docstring_return

        parsed_return_dict = parse_function(test_func)

        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_function_return["lineno"] = parsed_return_dict["lineno"]
        expected_parsed_function_return["sourcefile"] = parsed_return_dict["sourcefile"]

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_function_with_returns_annotation_no_returns_tag(self):
        self.maxDiff = None
        
        def test_func(arg1, arg2: str="Hello") -> int | float:
            """This function does some things."""
            pass

        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_docstring_return["description"] = "This function does some things."

        expected_parsed_function_return = {
            "name": "test_func",
            "docstring": None,
            "arguments": [
                {"name": "arg1", "type": None, "required": True, "default": None},
                {"name": "arg2", "type": str, "required": False, "default": "Hello"}
            ],
            "returns": int | float
        }
        expected_parsed_function_return["docstring"] = expected_docstring_return

        parsed_return_dict = parse_function(test_func)

        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_function_return["lineno"] = parsed_return_dict["lineno"]
        expected_parsed_function_return["sourcefile"] = parsed_return_dict["sourcefile"]

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_function_beginning_with_underscore_flags_as_private(self):
        """Functions names that start with an underscore should flag as private regardless of whether the docstring
        `@private` tag."""
        self.maxDiff = None
        
        def _test_func(arg1):
            """This function does some things."""
            pass

        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_docstring_return["description"] = "This function does some things."
        expected_docstring_return["private"] = True

        expected_parsed_function_return = {
            "name": "_test_func",
            "docstring": None,
            "arguments": [
                {"name": "arg1", "type": None, "required": True, "default": None}
            ],
            "returns": None
        }
        expected_parsed_function_return["docstring"] = expected_docstring_return

        parsed_return_dict = parse_function(_test_func)

        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_function_return["lineno"] = parsed_return_dict["lineno"]
        expected_parsed_function_return["sourcefile"] = parsed_return_dict["sourcefile"]

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_function_beginning_with_underscore_flags_as_private_even_without_docstring(self):
        """Functions names that start with an underscore should flag as private regardless of whether the docstring
        `@private` tag. This is also true if there is no docstring at all."""
        self.maxDiff = None
        
        def _test_func():
            pass

        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_docstring_return["private"] = True

        expected_parsed_function_return = {
            "name": "_test_func",
            "docstring": None,
            "arguments": None,
            "returns": None
        }
        expected_parsed_function_return["docstring"] = expected_docstring_return

        parsed_return_dict = parse_function(_test_func)

        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_function_return["lineno"] = parsed_return_dict["lineno"]
        expected_parsed_function_return["sourcefile"] = parsed_return_dict["sourcefile"]

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_function_lineno_and_source(self):
        """The lineno and sourcefile attributes have been mocked until now to prevent brittleness in the other tests.
        This test looks explicitly at the 'testmodule' (which should rarely change), to verify it works right."""
        self.maxDiff = None

        expected_parsed_function_return = {
            "name": "test_func1",
            "docstring": None,
            "arguments": None,
            "returns": None,
            "lineno": (22, 23),
            "sourcefile": os.path.join(os.path.dirname(__file__), "input_files", "testmodule.py")
        }

        parsed_return_dict = parse_function(test_func1)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)
