from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Private(unittest.TestCase):

    ###############################################################
    # Private
    ###############################################################

    def test_only_private_tag_only_value(self):

        description_entry = """@private"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["private"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_private_tag_own_line(self):

        description_entry = """
        @private
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["private"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_private_tag_extra_characters_after_not_marked_as_private(self):

        description_entry = """
        @private nope
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["private"] = False
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_only_private_tag_extra_characters_after_not_marked_as_private(self):

        description_entry = """
        This is also not @private
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is also not @private"
        expected_docstring_return["private"] = False
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_private_tag_extra_whitespace(self):

        description_entry = """      
              @private      
                
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["private"] = True
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    ###############################################################
    # Complex
    ###############################################################

    def test_private_tag_surrounded_by_other_tags(self):
        self.maxDiff = None

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @private
        @throws An error with no type 1
        @example Some caption text
        # This is a comment within the example
        myvar = 2
        if myvar == 2:
            print(myvar)
        @param SecondParamName This is another param description
        @returns This is the ultimate return text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."
        expected_docstring_return["private"] = True
        expected_docstring_return["examples"].append({"caption": "Some caption text", "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    