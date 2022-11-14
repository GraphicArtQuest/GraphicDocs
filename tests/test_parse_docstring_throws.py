from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Throws(unittest.TestCase):

    ###############################################################
    # Throws
    ###############################################################

    def test_only_throws_tag_error_type_and_description_provided(self):
        description_entry = """@throws [CustomErrorType] This is a description of a thrown error with a specified error type"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": "This is a description of a thrown error with a specified error type"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_only_throws_tag_description_only(self):
        description_entry = """@throws This is a description of a thrown error with no specified error type"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": None, "description": "This is a description of a thrown error with no specified error type"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_throws_tag_error_type_only(self):
        description_entry = """@throws [CustomErrorType]"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": None})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_throws_tag_error_type_with_multi_line_description_provided(self):
        description_entry = """@throws [CustomErrorType] This is a description of a thrown error with a 
                                specified error type that spreads onto a second line."""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": "This is a description of a thrown error with a specified error type that spreads onto a second line."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_only_throws_tag_with_multi_linedescription_only(self):
        description_entry = """@throws This is a description of a thrown error with a 
            specified error type that spreads onto a second line.  """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": None, "description": "This is a description of a thrown error with a specified error type that spreads onto a second line."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_throws_multiple_throws_with_type_and_description(self):
        description_entry = """
            @throws [CustomErrorType] This is a description of a thrown error with a specified error type
            @throws [AnotherErrorType] This is a second error
            """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": "This is a description of a thrown error with a specified error type"})
        expected_docstring_return["throws"].append({"type": "AnotherErrorType", "description": "This is a second error"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_throws_multiple_throws_with_description_only(self):
        description_entry = """
            @throws This is a description of a thrown error with a specified error type
            @throws This is a second error
            """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": None, "description": "This is a description of a thrown error with a specified error type"})
        expected_docstring_return["throws"].append({"type": None, "description": "This is a second error"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_throws_multiple_throws_type_only(self):
        description_entry = """
            @throws [CustomErrorType]
            @throws [AnotherErrorType]
            @throws [YetAnotherError]
            """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": None})
        expected_docstring_return["throws"].append({"type": "AnotherErrorType", "description": None})
        expected_docstring_return["throws"].append({"type": "YetAnotherError", "description": None})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    
    def test_only_throws_tag_type_missing_closing_brackets(self):
        """Should raise an exception because the bracket was never closed"""
        description_entry = """@throws [CustomErrorType"""

        with self.assertRaises(AttributeError):
            parse_docstring(description_entry)

    def test_only_throws_tag_missing_open_bracket_for_type(self):
        """Missing the opening bracket, so it treats the whole thing like a description"""
        description_entry = """@throws CustomErrorType] This is a description of a thrown error with a specified error type"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": None, "description": "CustomErrorType] This is a description of a thrown error with a specified error type"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_throws_tag_extra_space_before_open_bracket_for_type(self):
        """Extra space before type bracket treats the entire thing as a description string"""
        description_entry = """@throws  [CustomErrorType] This is a description of a thrown error with a specified error type"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": None, "description": "[CustomErrorType] This is a description of a thrown error with a specified error type"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_only_throws_should_recognize_paragraph_breaks_in_description(self):
        self.maxDiff = None
        description_entry = """
            @throws [CustomErrorType] This is a description of a thrown error with a specified error type.

            The description has two paragraphs.
            @throws This is an error description that has no type.

            It also has two paragraphs.
            @throws [AnotherErrorType] This is a third error with only one line.
            """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": "This is a description of a thrown error with a specified error type.\nThe description has two paragraphs."})
        expected_docstring_return["throws"].append({"type": None, "description": "This is an error description that has no type.\nIt also has two paragraphs."})
        expected_docstring_return["throws"].append({"type": "AnotherErrorType", "description": "This is a third error with only one line."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    ###############################################################
    # Complex
    ###############################################################

    def test_throws_mixed_type_and_desc_provided_plus_params_and_return(self):
        description_entry = """
            This one also has a description in it.

            @param MyParam This is a param description
            @throws An error with no type 1
            @throws [CustomErrorType]
            @throws [AnotherErrorType]
            @throws [YetAnotherError]
            @throws [CustomErrorType] A Repeat of Before 1
            @throws [AnotherErrorType] A Repeat of Before 2
            @throws [YetAnotherError] A Repeat of Before 3
            @throws An error with no type 2
            @returns This should get ignored
            @param MyParam2 This is another param description
            @returns This is the ultimate return text
            """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."

        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": None})
        expected_docstring_return["throws"].append({"type": "AnotherErrorType", "description": None})
        expected_docstring_return["throws"].append({"type": "YetAnotherError", "description": None})
        expected_docstring_return["throws"].append({"type": "CustomErrorType", "description": "A Repeat of Before 1"})
        expected_docstring_return["throws"].append({"type": "AnotherErrorType", "description": "A Repeat of Before 2"})
        expected_docstring_return["throws"].append({"type": "YetAnotherError", "description": "A Repeat of Before 3"})
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 2"})

        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"MyParam2": "This is another param description"})
        
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

