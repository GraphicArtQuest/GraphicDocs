from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Copyright(unittest.TestCase):

    ###############################################################
    # Copyright
    ###############################################################

    def test_only_copyright_tag_no_inputs(self):

        description_entry = """@copyright  """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_copyright_tag_with_good_example(self):

        description_entry = """@copyright All rights reserved."""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["copyright"] = []
        expected_docstring_return["copyright"].append("All rights reserved.")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_copyright_tag_with_extra_whitespace(self):

        description_entry = """
        
                @copyright All rights reserved.    

                     """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["copyright"] = []
        expected_docstring_return["copyright"].append("All rights reserved.")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)    

    def test_only_multiple_copyrights_plus_description(self):

        description_entry = """
        This is a function that does some stuff.

        @copyright All rights reserved.
        @copyright All rights still reserved.
        @copyright All rights reserved again.
        @copyright All rights forever reserved.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["copyright"] = []
        expected_docstring_return["copyright"].append("All rights reserved.")
        expected_docstring_return["copyright"].append("All rights still reserved.")
        expected_docstring_return["copyright"].append("All rights reserved again.")
        expected_docstring_return["copyright"].append("All rights forever reserved.")
        expected_docstring_return["description"] = "This is a function that does some stuff."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_copyright_tag_with_incorrect_syntax(self):

        description_entry = """marking something as @copyright does nothing"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "marking something as @copyright does nothing"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_copyright_tag_with_multiple_paragraphs(self):

        description_entry = """@copyright All rights reserved.
        This rolled over a line.

        This is a second paragraph.
        

        @copyright This is a second copyright.
        
        It also has two paragraphs."""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["copyright"] = []
        expected_docstring_return["copyright"].append("All rights reserved. This rolled over a line.\nThis is a second paragraph.")
        expected_docstring_return["copyright"].append("This is a second copyright.\nIt also has two paragraphs.")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    ###############################################################
    # Complex
    ###############################################################

    def test_copyright_tag_surrounded_by_other_tags(self):

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @throws An error with no type 1
        @copyright Some stuff
        @param SecondParamName This is another param description
        @returns This is the ultimate return text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."
        expected_docstring_return["copyright"] = []
        expected_docstring_return["copyright"].append("Some stuff")
        expected_docstring_return["throws"] = []
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_example_tag_multiple_copyright_and_other_tags(self):

        description_entry = """
        This is a description.

        @param the_var A variable of any type
        @returns It just prints to the console
        @copyright Some stuff
        @example
        print(myvar1)
        @example
        print(myvar2)
        @example This one has a caption
        print(myvar3)
        @copyright Some more stuff
        and this @copyright is part of it
        @example
        print(myvar4)
        @returns This is an overriding returns tag
        @copyright Some final stuff
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["parameters"].append({"the_var": "A variable of any type"})
        expected_docstring_return["returns"] = "This is an overriding returns tag"
        expected_docstring_return["copyright"] = []
        expected_docstring_return["copyright"].append("Some stuff")
        expected_docstring_return["copyright"].append("Some more stuff and this @copyright is part of it")
        expected_docstring_return["copyright"].append("Some final stuff")
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar1)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar2)"})
        expected_docstring_return["examples"].append({"caption": "This one has a caption", "code": "print(myvar3)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar4)"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        