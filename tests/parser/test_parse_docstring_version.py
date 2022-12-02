from copy import deepcopy
import unittest

from .input_files.blank_defaults import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Version(unittest.TestCase):

    ###############################################################
    # Version
    ###############################################################
    def test_only_version_tag_no_value_returns_false(self):

        description_entry = """@version"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_version_tag_no_value_returns_false_own_line(self):

        description_entry = """
        @version
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_only_version_tag_no_value_extra_whitespace_returns_false(self):

        description_entry = """      
              @version      
                
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_multiple_version_tags_cause_no_errors(self):
        """
            It should not matter how many times a `@version` tag gets included. It should cause no errors.
            Only the latest one should get recorded.
        """
        description_entry = """
        @version
        @version version 2.0
        @version
        @version 3.0
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = "3.0"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_version_tag_with_description(self):
        description_entry = """@version This is a description of the version or other text."""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = "This is a description of the version or other text."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    def test_only_version_tag_with_description(self):
        description_entry = """This is a description.

        @version This is a description of the version or other text."""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["version"] = "This is a description of the version or other text."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_version_tag_two_lines(self):
        description_entry = """
            @version This is a description of the change
            that has spilled onto a second line.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = "This is a description of the change that has spilled onto a second line."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_version_tag_more_than_two_lines(self):
        description_entry = """
            @version This is a description of the change
            that has spilled onto a second line.
            And then a third line.
            And a fourth.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = "This is a description of the change that has spilled onto a second line. And then a third line. And a fourth."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_version_tag_more_than_two_lines_with_paragraph_breaks(self):
        description_entry = """
            @version This is a description of the change
            that has spilled onto a second line.

            This starts a new paragraph.
            And then a second line.
            And a third.

            This is a final paragraph.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = "This is a description of the change that has spilled onto a second line.\nThis starts a new paragraph. And then a second line. And a third.\nThis is a final paragraph."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_more_than_one_version_tag_only_tracks_last_one(self):
        description_entry = """
            @version This is a description of the change
            @version This is a different change description.
            It goes over two lines.
            @version This is a third change that should show up instead
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = "This is a third change that should show up instead"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_more_than_one_version_tag_last_one_is_empty_returns_false(self):
        """Only the last `@sense` tag gets recorded, and if it is a bad tag, then it will give `False`"""
        description_entry = """
            @version This is a description of the change
            @version This is a different change description.
            It goes over two lines.
            @version This is a third change that should show up instead
            @version
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["version"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_version_tag_with_description_but_no_text_provided(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.
            
            @version   """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["version"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

        
    # ###############################################################
    # # Complex
    # ###############################################################

    def test_version_value_after_parameters(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @param my_test_parameter2 This is a description of a test parameter 2
            @version This is a description of the change
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["version"] = "This is a description of the change"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_version_value_between_parameters(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @version This is a description of the change.
            @param my_test_parameter2 This is a description of a test parameter 2
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["version"] = "This is a description of the change."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_version_value_between_parameters_with_final_version_value_at_end(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @version This is a description of the chang
            @param my_test_parameter2 This is a description of a test parameter 2
            @version This is the actual change description
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["version"] = "This is the actual change description"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_version_value_after_parameters_with_multi_line_version(self):
        self.maxDiff = None
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @version This is a description of the change.
            It goes on to multiple lines.

            There is even a paragraph break.
            @param my_test_parameter1 This is a description of a test parameter 1.
            This parameter has two lines.
            @param my_test_parameter2 This is a description of a test parameter 2
            @returns Nothing to say
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1. This parameter has two lines."})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["version"] = "This is a description of the change. It goes on to multiple lines.\nThere is even a paragraph break."
        expected_docstring_return["returns"] = "Nothing to say"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_version_value_with_deprecated_and_since(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @since 7.19
            @deprecated in 7.55
            @version This is a description of the change
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["since"] = "7.19"
        expected_docstring_return["deprecated"] = "in 7.55"
        expected_docstring_return["version"] = "This is a description of the change"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)