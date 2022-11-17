from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Memberof(unittest.TestCase):

    ###############################################################
    # Memberof
    ###############################################################

    def test_only_memberof_tag_with_good_name(self):

        description_entry = """@memberof ValidName"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    def test_only_memberof_tag_with_good_name_and_extra_whitespace(self):

        description_entry = """
        
            @memberof          ValidName       


                """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_memberof_tag_with_good_name_and_func_description(self):

        description_entry = """
        This is a description.
        @memberof ValidName
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_memberof_tag_with_good_name_subsequent_lines_not_tracked(self):

        description_entry = """
        This is a description.
        @memberof ValidName
        This line should not be tracked.

        Nor this one.
        Or this one.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_memberof_tag_with_multiple_memberof_with_good_names(self):

        description_entry = """
        This is a description.
        @memberof ValidName1
        @memberof ValidName2
        This text is not tracked
        @memberof ValidName3
        @memberof ValidName4
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName1")
        expected_docstring_return["memberof"].append("ValidName2")
        expected_docstring_return["memberof"].append("ValidName3")
        expected_docstring_return["memberof"].append("ValidName4")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_memberof_tag_with_identical_tags_only_unique_marked(self):
        """The parser should only pull out valid unique `memberof` tags."""

        description_entry = """
        This is a description.
        @memberof ValidName1
        @memberof ValidName2
        @memberof ValidName3
        @memberof ValidName3
        @memberof ValidName3
        @memberof ValidName4
        @memberof ValidName4
        @memberof ValidName1
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName1")
        expected_docstring_return["memberof"].append("ValidName2")
        expected_docstring_return["memberof"].append("ValidName3")
        expected_docstring_return["memberof"].append("ValidName4")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_memberof_tag_with_invalid_syntax_not_tracked(self):
        """The parser should ignore @memberof tags with invalid syntax"""

        description_entry = """
        This is a description.
        @memberof ValidName1
        This is not a @memberof ValidName2
        @membersof ValidName3
        @memberofValidName4
        @memberof ValidName5
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName1")
        expected_docstring_return["memberof"].append("ValidName5")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_namespace_tag_invalid_names_not_processed(self):
        """The parser should only pull out valid unique `memberof` tags."""

        description_entry = """
        @memberof 1InvalidName
        @memberof InvalidName With Extra Words
        @memberof Invalid-Name
        @memberof InvalidName#
        @memberof InvalidName@
        @memberof ValidName
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    # # ###############################################################
    # # # Complex
    # # ###############################################################

    def test_memberof_tag_surrounded_by_other_tags(self):
        self.maxDiff = None

        description_entry = """This one also has a description in it.

        @namespace MyName
        This is a description.
        @memberof ValidName
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
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName", "description": "This is a description."})
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_example_tag_multiple_memberof_and_other_tags(self):

        description_entry = """
        This is a description.
        @memberof ValidName1

        @namespace MyName1
        This is a description.
        @param the_var A variable of any type
        @returns It just prints to the console
        @example
        print(myvar1)
        @example
        print(myvar2)
        @memberof ValidName2
        @namespace MyName2
        This is a description.
        @memberof ValidName3
        @example This one has a caption
        print(myvar3)
        @example
        print(myvar4)
        @returns This is an overriding returns tag
        @namespace MyName3
        This is a description.
        @memberof ValidName4
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
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName1", "description": "This is a description."})
        expected_docstring_return["namespaces"].append({"name": "MyName2", "description": "This is a description."})
        expected_docstring_return["namespaces"].append({"name": "MyName3", "description": "This is a description."})
        expected_docstring_return["memberof"] = []
        expected_docstring_return["memberof"].append("ValidName1")
        expected_docstring_return["memberof"].append("ValidName2")
        expected_docstring_return["memberof"].append("ValidName3")
        expected_docstring_return["memberof"].append("ValidName4")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
