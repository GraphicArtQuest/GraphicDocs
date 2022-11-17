from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_License(unittest.TestCase):

    ###############################################################
    # License
    ###############################################################

    def test_only_license_tag_no_name_or_text_returns_none(self):

        description_entry = """
        @license
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    def test_only_license_tag_with_license_text_only(self):

        description_entry = """
        @license
        This is the license text.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": None, "text": "This is the license text."}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_license_tag_with_license_name_only(self):

        description_entry = """
        @license MIT
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": "MIT", "text": None}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_license_tag_with_license_name_and_text(self):

        description_entry = """
        @license MIT
        Some license text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": "MIT", "text": "Some license text"}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_license_tag_with_license_name_and_text_multi_line(self):

        description_entry = """
        @license MIT
        Some license text.
        It goes on to another line.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": "MIT", "text": "Some license text. It goes on to another line."}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_license_tag_with_license_name_and_text_multi_line_multiple_paragraphs(self):

        description_entry = """
        @license MIT
        Some license text.
        It goes on to another line.

        Then another paragraph.

        And another.
        With a second line.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": "MIT", "text": "Some license text. It goes on to another line.\nThen another paragraph.\nAnd another. With a second line."}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_license_tag_no_license_name_and_text_multi_line_multiple_paragraphs(self):

        description_entry = """
        @license
        Some license text.
        It goes on to another line.

        Then another paragraph.

        And another.
        With a second line.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": None, "text": "Some license text. It goes on to another line.\nThen another paragraph.\nAnd another. With a second line."}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_multiple_license_returns_only_last_one_1(self):

        description_entry = """
        @license MIT
        Some license text
        @license
        Some other license text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": None, "text": "Some other license text"}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_multiple_license_returns_only_last_one_2(self):

        description_entry = """
        @license MIT
        Some license text
        @license Apache
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = {"name": "Apache", "text": None}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_multiple_license_returns_only_last_one_3(self):

        description_entry = """
        @license MIT
        Some license text
        @license
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["license"] = None
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    # ###############################################################
    # # Complex
    # ###############################################################

    def test_license_tag_with_caption_surrounded_by_other_tags(self):
        self.maxDiff = None

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @throws An error with no type 1
        @license MIT
        Some license text
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
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": "Some caption text", "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        expected_docstring_return["throws"] = []
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        expected_docstring_return["license"] = {"name": "MIT", "text": "Some license text"}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_license_tag_multiple_licenses_and_other_tags(self):

        description_entry = """
        This is a description.

        @param the_var A variable of any type
        @returns It just prints to the console
        @example
        print(myvar1)
        @license Apache
        Some Apache license text
        @example
        print(myvar2)
        @example This one has a caption
        print(myvar3)
        @example
        print(myvar4)
        @returns This is an overriding returns tag
        @license MIT
        Some license text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["parameters"].append({"the_var": "A variable of any type"})
        expected_docstring_return["returns"] = "This is an overriding returns tag"
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar1)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar2)"})
        expected_docstring_return["examples"].append({"caption": "This one has a caption", "code": "print(myvar3)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar4)"})
        expected_docstring_return["license"] = {"name": "MIT", "text": "Some license text"}
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        