from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_class

class TestParseClass(unittest.TestCase):

    ###############################################################
    # Classes
    ###############################################################

    def test_nonclasses_return_nothing(self):
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
            self.assertIsNone(parse_class(input))

    def test_simple_class(self):
        self.maxDiff = None
        
        class TestClass():
            def __init__():
                pass

        expected_parsed_function_return = {
            "name": "TestClass",
            "docstring": None,
            "annotations": None,
            "arguments": None,
            "methods": None,
            "properties": None,
            "parent": None,
            "subclasses": None
        }

        parsed_return_dict = parse_class(TestClass)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_function_parse_arguments_basics(self):
        self.maxDiff = None
        
        class TestClass():
            def __init__(self, arg1, arg2: str, arg2a, arg3: bool=False, arg4: bool=True, arg5: float=2.5, arg6: int=733,
                        arg7:list[str | None]=['Hello', 'World!'], arg8:dict={"key1": True}):
                pass

        expected_parsed_function_return = {
            "name": "TestClass",
            "docstring": None,
            "annotations": None,
            "arguments": [
                {"name": "arg1", "type": any, "required": True, "default": None},
                {"name": "arg2", "type": str, "required": True, "default": None},
                {"name": "arg2a", "type": any, "required": True, "default": None},
                {"name": "arg3", "type": bool, "required": False, "default": False},
                {"name": "arg4", "type": bool, "required": False, "default": True},
                {"name": "arg5", "type": float, "required": False, "default": 2.5},
                {"name": "arg6", "type": int, "required": False, "default": 733},
                {"name": "arg7", "type": list[str | None], "required": False, "default": ['Hello', 'World!']},
                {"name": "arg8", "type": dict, "required": False, "default": {"key1": True}}
            ],
            "methods": None,
            "properties": None,
            "parent": None,
            "subclasses": None
        }

        parsed_return_dict = parse_class(TestClass)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_class_with_docstring(self):
        self.maxDiff = None
        
        class TestClass():
            """This class does some things."""
            def __init__(self, arg1):
                pass
        
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_docstring_return["description"] = "This class does some things."

        expected_parsed_function_return = {
            "name": "TestClass",
            "docstring": expected_docstring_return,
            "annotations": None,
            "arguments": [
                {"name": "arg1", "type": any, "required": True, "default": None}
            ],
            "methods": None,
            "properties": None,
            "parent": None,
            "subclasses": None
        }

        parsed_return_dict = parse_class(TestClass)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)
    
    def test_simple_class_with_functions(self):
        self.maxDiff = None
        
        class TestClass():
            def my_function():
                pass
            def my_function2(self) -> int:
                pass
            def my_function3(self, myvar: str) -> int:
                pass
        

        expected_parsed_function_return = {
            "name": "TestClass",
            "docstring": None,
            "annotations": None,
            "arguments": None,
            "methods": {
                "my_function": {
                    "arguments": None,
                    "docstring": None,
                    "name": "my_function",
                    "returns": None
                },
                "my_function2": {
                    "arguments": None,
                    "docstring": None,
                    "name": "my_function2",
                    "returns": int
                },
                "my_function3": {
                    "arguments": [{"name": "myvar", "type": str, "required": True, "default": None}],
                    "docstring": None,
                    "name": "my_function3",
                    "returns": int
                }
            },
            "properties": None,
            "parent": None,
            "subclasses": None
        }

        parsed_return_dict = parse_class(TestClass)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_class_starting_with_underscore_treated_as_private(self):
        self.maxDiff = None
        
        class _TestClass():
            pass


        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_docstring_return["private"] = True

        expected_parsed_function_return = {
            "name": "_TestClass",
            "docstring": expected_docstring_return,
            "annotations": None,
            "arguments": None,
            "methods": None,
            "properties": None,
            "parent": None,
            "subclasses": None
        }

        parsed_return_dict = parse_class(_TestClass)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_class_has_properties(self):
        self.maxDiff = None
        
        class TestClass():
            def _get_myprop(self):
                return 1

            def _set_myprop(self, arg1: int):
                pass

            @property
            def MyProp8(self):
                """This is a property description in a prop function header."""
                pass
            
            MyProp2 = property(_get_myprop, _set_myprop)  # 2 intentionally before 1 to check array ordering
            MyProp1 = property(_get_myprop, _set_myprop)
            MyProp3 = property(_get_myprop)
            MyProp4 = property(fget=_get_myprop)
            MyProp5 = property(fset=_set_myprop)
            MyProp6 = property()    # Not sure why you would want an empty property, but... it's available
            MyProp7 = property(fget=_get_myprop, doc="This is a property description.")


        expected_prop7_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_prop7_docstring_return["description"] = "This is a property description."
        
        expected_prop8_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_prop8_docstring_return["description"] = "This is a property description in a prop function header."

        
        expected_gettersetter_docstring_return = deepcopy(blank_parse_docstring_return)
        expected_gettersetter_docstring_return["private"] = True

        expected_parsed_function_return = {
            "name": "TestClass",
            "docstring": None,
            "annotations": None,
            "arguments": None,
            "methods": {
                "_get_myprop": {
                    "arguments": None,
                    "docstring": expected_gettersetter_docstring_return,
                    "name": "_get_myprop",
                    "returns": None
                },
                "_set_myprop": {
                    "arguments": [{"name": "arg1", "type": int, "required": True, "default": None}],
                    "docstring": expected_gettersetter_docstring_return,
                    "name": "_set_myprop",
                    "returns": None
                }
            },
            "properties": {
                "MyProp8": {"docstring": expected_prop8_docstring_return, "readable": True, "writable": False},
                "MyProp2": {"docstring": None, "readable": True, "writable": True},
                "MyProp1": {"docstring": None, "readable": True, "writable": True},
                "MyProp3": {"docstring": None, "readable": True, "writable": False},
                "MyProp4": {"docstring": None, "readable": True, "writable": False},
                "MyProp5": {"docstring": None, "readable": False, "writable": True},
                "MyProp6": {"docstring": None, "readable": False, "writable": False},
                "MyProp7": {"docstring": expected_prop7_docstring_return, "readable": True, "writable": False}
            },
            "parent": None,
            "subclasses": None
        }

        parsed_return_dict = parse_class(TestClass)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_class_with_annotations(self):
        self.maxDiff = None
        
        class TestClass():
            myvar1: str = "Hi there"
            myvar1: int = 1 # Overwrites previous annotation
            myvar2: any=2

        expected_parsed_function_return = {
            "name": "TestClass",
            "docstring": None,
            "annotations": {"myvar1": int, "myvar2": any},
            "arguments": None,
            "methods": None,
            "properties": None,
            "parent": None,
            "subclasses": None
        }

        parsed_return_dict = parse_class(TestClass)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)

    def test_simple_class_with_nested_subclasses_and_inheritence(self):
        self.maxDiff = None

        class SubClass1():
                    pass
        
        class TestClass2(SubClass1):
            class SubClass3():
                pass
        
            class SubClass4(SubClass3):
                class SubClass5():
                    pass

        expected_parsed_function_return = {
            "name": "TestClass2",
            "docstring": None,
            "annotations": None,
            "arguments": None,
            "methods": None,
            "properties": None,
            "parent": "SubClass1",
            "subclasses": {
                "SubClass3": {
                    "name": "SubClass3",
                    "docstring": None,
                    "annotations": None,
                    "arguments": None,
                    "methods": None,
                    "properties": None,
                    "parent": None,
                    "subclasses": None
                },
                "SubClass4": {
                    "name": "SubClass4",
                    "docstring": None,
                    "annotations": None,
                    "arguments": None,
                    "methods": None,
                    "properties": None,
                    "parent": "SubClass3",
                    "subclasses": {
                        "SubClass5": {
                            "name": "SubClass5",
                            "docstring": None,
                            "annotations": None,
                            "arguments": None,
                            "methods": None,
                            "properties": None,
                            "parent": None,
                            "subclasses": None
                        }
                    }
                },
            }
        }
        parsed_return_dict = parse_class(TestClass2)

        self.assertDictEqual(expected_parsed_function_return, parsed_return_dict)
