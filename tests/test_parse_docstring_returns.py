from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Returns(unittest.TestCase):

    ###############################################################
    # Returns
    ###############################################################

    def test_only_returns_tag(self):
        description_entry = """@returns This is a description of the return value"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["returns"] = "This is a description of the return value"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_returns_tag_two_lines(self):
        description_entry = """
            @returns This is a description of the return value
            that spills onto a second line
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["returns"] = "This is a description of the return value that spills onto a second line"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_returns_tag_more_than_two_lines(self):
        description_entry = """
            @returns This is a description of the return value
            that spills onto a second line
            and then a third line
            and even a fourth
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["returns"] = "This is a description of the return value that spills onto a second line and then a third line and even a fourth"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_more_than_one_returns_tag_only_tracks_last_one(self):
        description_entry = """
            @returns This is a description of the return value
            @returns This is a different returns description
            @returns This is a second description that should show up instead
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["returns"] = "This is a second description that should show up instead"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_returns_tag_with_description_but_no_text_provided(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.
            
            @returns   """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["returns"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_empty_returns_tag(self):
        description_entry = """@returns"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["returns"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    ###############################################################
    # Complex
    ###############################################################

    def test_returns_value_after_parameters(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @param my_test_parameter2 This is a description of a test parameter 2
            @returns This is a description of the return value
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["returns"] = "This is a description of the return value"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_returns_value_between_parameters(self):
        self.maxDiff = None
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @returns This is a description of the return value
            @param my_test_parameter2 This is a description of a test parameter 2
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["returns"] = "This is a description of the return value"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_returns_value_between_parameters_with_final_returns_at_end(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @returns This is a description of the return value
            @param my_test_parameter2 This is a description of a test parameter 2
            @returns This is a my actual returns value
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["returns"] = "This is a my actual returns value"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
