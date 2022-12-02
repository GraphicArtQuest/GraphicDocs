from copy import deepcopy
import unittest

from .input_files.blank_defaults import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Examples(unittest.TestCase):

    ###############################################################
    # Example
    ###############################################################

    def test_only_example_tag_with_good_example(self):

        description_entry = """
        @example
        # This is a comment within the example
        myvar = 2
        if myvar == 2:
            print(myvar)
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_example_tag_with_good_example_and_caption(self):

        description_entry = """
        @example This text is a caption for the example
        # This is a comment within the example
        myvar = 2
        if myvar == 2:
            print(myvar)
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": "This text is a caption for the example", "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_example_tag_multiple_examples(self):

        description_entry = """
        @example
        print(myvar1)
        @example
        print(myvar2)
        @example This one has a caption
        print(myvar3)
        @example
        print(myvar4)
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar1)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar2)"})
        expected_docstring_return["examples"].append({"caption": "This one has a caption", "code": "print(myvar3)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar4)"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_example_tag_characters_before_tagname_get_cut_off_in_formatting(self):
        """Any characters before the `@` symbol should get cut off as outside of the formatting scope."""

        description_entry = """
        @example
        # These two lines should completely appear.
        print(myvar2)
    # These two lines should get cut off
    print(myvar2)
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "# These two lines should completely appear.\nprint(myvar2)\nese two lines should get cut off\nt(myvar2)"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_example_tag_with_just_caption(self):

        description_entry = """
        @example This is an example with only a caption. It should return nothing.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    ###############################################################
    # Complex
    ###############################################################

    def test_example_tag_with_caption_surrounded_by_other_tags(self):
        self.maxDiff = None

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
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
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": "Some caption text", "code": "# This is a comment within the example\nmyvar = 2\nif myvar == 2:\n    print(myvar)"})
        expected_docstring_return["throws"] = []
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_example_tag_multiple_examples_and_other_tags(self):

        description_entry = """
        This is a description.

        @param the_var A variable of any type
        @returns It just prints to the console
        @example
        print(myvar1)
        @example
        print(myvar2)
        @example This one has a caption
        print(myvar3)
        @example
        print(myvar4)
        @returns This is an overriding returns tag
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"the_var": "A variable of any type"})
        expected_docstring_return["returns"] = "This is an overriding returns tag"
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar1)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar2)"})
        expected_docstring_return["examples"].append({"caption": "This one has a caption", "code": "print(myvar3)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar4)"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        