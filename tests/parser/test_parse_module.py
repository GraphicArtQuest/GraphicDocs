from copy import deepcopy
import os
import unittest

from src.parser import parse_module
from tests.parser.input_files.blank_defaults import blank_parse_docstring_return, blank_parse_class_return, blank_parse_module_return, blank_parsed_function_return
from tests.parser.input_files import testmodule
from tests.parser.input_files import testmodule_only_docstring
from tests.parser.input_files import testmodule_with_imports

class TestParseModule(unittest.TestCase):

    ###############################################################
    # Modules
    ###############################################################

    def test_nonmodule_returns_nothing(self):
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
            None,
            parse_module
        ]

        for input in inputs:
            self.assertIsNone(parse_module(input))
        # self.assertIsNotNone(parse_module(os))  # Check with a built in module

    def test_module(self):
        self.maxDiff = None

        expected_parsed_module_return = deepcopy(blank_parse_module_return)
        expected_parsed_module_return["name"] = "tests.parser.input_files.testmodule"

        # Classes will always show up in alphabetical order, not the order they appear in the file
        expected_parsed_module_return["classes"] = {}
        expected_parsed_module_return["classes"]["TestClass1"] = deepcopy(blank_parse_class_return)
        expected_parsed_module_return["classes"]["TestClass1"]["name"] = "TestClass1"
        expected_parsed_module_return["classes"]["TestClass1"]["docstring"] = deepcopy(blank_parse_docstring_return)
        expected_parsed_module_return["classes"]["TestClass1"]["docstring"]["description"] = "This class does one classy thing."
        expected_parsed_module_return["classes"]["TestClass1"]["arguments"] = [{"default": None, "name": "arg1", "required": True, "type": any}]

        expected_parsed_module_return["classes"]["_TestClass2"] = deepcopy(blank_parse_class_return)
        expected_parsed_module_return["classes"]["_TestClass2"]["name"] = "_TestClass2"
        expected_parsed_module_return["classes"]["_TestClass2"]["docstring"] = deepcopy(blank_parse_docstring_return)
        expected_parsed_module_return["classes"]["_TestClass2"]["docstring"]["private"] = True

        # Functions will always show up in alphabetical order, not the order they appear in the file
        expected_parsed_module_return["functions"] = {}
        expected_parsed_module_return["functions"]["test_func1"] = deepcopy(blank_parsed_function_return)
        expected_parsed_module_return["functions"]["test_func1"]["name"] = "test_func1"
        expected_parsed_module_return["functions"]["test_func2"] = deepcopy(blank_parsed_function_return)
        expected_parsed_module_return["functions"]["test_func2"]["name"] = "test_func2"
        expected_parsed_module_return["functions"]["test_func3"] = deepcopy(blank_parsed_function_return)
        expected_parsed_module_return["functions"]["test_func3"]["name"] = "test_func3"
        
        expected_parsed_module_return["imported"] = {
            "classes": None,
            "functions": [('ntpath', 'abspath'), ('copy', 'deepcopy')],
            "modules": ['copy', 'os', 'sys']
        }

        expected_parsed_module_return["sourcefile"] = os.path.abspath(testmodule.__file__)

        parsed_return_dict = parse_module(testmodule)
        
        # Line numbers and sources are verified elsewhere. Mocking them as correct prevents more brittle tests. 
        expected_parsed_module_return["classes"]["TestClass1"]["lineno"] = parsed_return_dict["classes"]["TestClass1"]["lineno"]
        expected_parsed_module_return["classes"]["TestClass1"]["sourcefile"] = parsed_return_dict["classes"]["TestClass1"]["sourcefile"]
        expected_parsed_module_return["classes"]["_TestClass2"]["lineno"] = parsed_return_dict["classes"]["_TestClass2"]["lineno"]
        expected_parsed_module_return["classes"]["_TestClass2"]["sourcefile"] = parsed_return_dict["classes"]["_TestClass2"]["sourcefile"]
        
        expected_parsed_module_return["functions"]["test_func1"]["lineno"] = parsed_return_dict["functions"]["test_func1"]["lineno"]
        expected_parsed_module_return["functions"]["test_func1"]["sourcefile"] = parsed_return_dict["functions"]["test_func1"]["sourcefile"]
        expected_parsed_module_return["functions"]["test_func2"]["lineno"] = parsed_return_dict["functions"]["test_func2"]["lineno"]
        expected_parsed_module_return["functions"]["test_func2"]["sourcefile"] = parsed_return_dict["functions"]["test_func2"]["sourcefile"]
        expected_parsed_module_return["functions"]["test_func3"]["lineno"] = parsed_return_dict["functions"]["test_func3"]["lineno"]
        expected_parsed_module_return["functions"]["test_func3"]["sourcefile"] = parsed_return_dict["functions"]["test_func3"]["sourcefile"]

        self.assertDictEqual(expected_parsed_module_return, parsed_return_dict)
    
    def test_module_only_docstring(self):
        """This test only covers the module with a docstring. It verifies the proper `None` return result for the
        other properties when they do not have any object in that category."""
        self.maxDiff = None

        expected_parsed_module_return = deepcopy(blank_parse_module_return)
        expected_parsed_module_return["name"] = "tests.parser.input_files.testmodule_only_docstring"
        expected_parsed_module_return["sourcefile"] = os.path.abspath(testmodule_only_docstring.__file__)
        expected_parsed_module_return["imported"] = {'classes': None, 'functions': None, 'modules': None}

        parsed_return_dict = parse_module(testmodule_only_docstring)

        self.assertDictEqual(expected_parsed_module_return, parsed_return_dict)
        
    def test_module_only_imports(self):
        """This test verifies the imported objects are correctly recorded."""
        self.maxDiff = None

        expected_parsed_module_return = deepcopy(blank_parse_module_return)
        expected_parsed_module_return["name"] = "tests.parser.input_files.testmodule_with_imports"
        expected_parsed_module_return["sourcefile"] = os.path.abspath(testmodule_with_imports.__file__)
        expected_parsed_module_return["imported"] = {
            "classes": [('tests.parser.input_files.testmodule', 'TestClass1')],
            "functions": [('tests.parser.input_files.testmodule', 'test_func1')],
            "modules": ["testmodule_only_docstring"]
        }

        parsed_return_dict = parse_module(testmodule_with_imports)

        self.assertDictEqual(expected_parsed_module_return, parsed_return_dict)
