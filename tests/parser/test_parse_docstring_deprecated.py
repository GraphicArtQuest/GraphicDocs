from copy import deepcopy
import unittest

from tests.parser.input_files.blank_defaults import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Deprecated(unittest.TestCase):

    ###############################################################
    # Deprecated
    ###############################################################
    def test_only_deprecated_tag_only_value(self):

        description_entry = """@deprecated"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_deprecated_tag_own_line(self):

        description_entry = """
        @deprecated
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_only_private_tag_extra_whitespace(self):

        description_entry = """      
              @deprecated      
                
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_multiple_deprecated_tags_cause_no_errors(self):
        """It should not matter how many times a `@deprecated` tag gets included. It should cause no errors."""
        description_entry = """
        @deprecated
        @deprecated since 2.0
        @deprecated
        @deprecated
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_deprecated_tag_without_description(self):
        description_entry = """@deprecated This is a description of the deprecation"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = "This is a description of the deprecation"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    def test_only_deprecated_tag_with_description(self):
        description_entry = """This is a description.

        @deprecated This is a description of the deprecation"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["deprecated"] = "This is a description of the deprecation"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_deprecated_tag_two_lines(self):
        description_entry = """
            @deprecated This is a description of the deprecation
            that has spilled onto a second line.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = "This is a description of the deprecation that has spilled onto a second line."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_deprecated_tag_more_than_two_lines(self):
        description_entry = """
            @deprecated This is a description of the deprecation
            that has spilled onto a second line.
            And then a third line.
            And a fourth.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = "This is a description of the deprecation that has spilled onto a second line. And then a third line. And a fourth."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_deprecated_tag_more_than_two_lines_with_paragraph_breaks(self):
        description_entry = """
            @deprecated This is a description of the deprecation
            that has spilled onto a second line.

            This starts a new paragraph.
            And then a second line.
            And a third.

            This is a final paragraph.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = "This is a description of the deprecation that has spilled onto a second line.\nThis starts a new paragraph. And then a second line. And a third.\nThis is a final paragraph."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_more_than_one_deprecated_tag_only_tracks_last_one(self):
        description_entry = """
            @deprecated This is a description of the deprecation
            @deprecated This is a different deprecation description.
            It goes over two lines.
            @deprecated This is a third deprecation that should show up instead
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["deprecated"] = "This is a third deprecation that should show up instead"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_deprecated_tag_with_description_but_no_text_provided(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.
            
            @deprecated   """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["deprecated"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

        
    # ###############################################################
    # # Complex
    # ###############################################################

    def test_deprecated_value_after_parameters(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @param my_test_parameter2 This is a description of a test parameter 2
            @deprecated This is a description of the deprecation
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["deprecated"] = "This is a description of the deprecation"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_deprecated_value_between_parameters(self):
        self.maxDiff = None
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @deprecated This is a description of the deprecation.
            @param my_test_parameter2 This is a description of a test parameter 2
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["deprecated"] = "This is a description of the deprecation."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_deprecated_value_between_parameters_with_final_deprecated_value_at_end(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @deprecated This is a description of the deprecated value
            @param my_test_parameter2 This is a description of a test parameter 2
            @deprecated This is the actual deprecated description
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["deprecated"] = "This is the actual deprecated description"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_deprecated_value_after_parameters_with_multi_line_deprecated(self):
        self.maxDiff = None
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @deprecated This is a description of the deprecation.
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
        expected_docstring_return["deprecated"] = "This is a description of the deprecation. It goes on to multiple lines.\nThere is even a paragraph break."
        expected_docstring_return["returns"] = "Nothing to say"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
