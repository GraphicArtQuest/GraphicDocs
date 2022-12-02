from copy import deepcopy
import unittest

from .input_files.blank_defaults import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Namespace(unittest.TestCase):

    ###############################################################
    # Namespace
    ###############################################################

    def test_only_namespace_tag_with_good_name(self):

        description_entry = """@namespace ValidName"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "ValidName", "description": None})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    def test_only_namespace_tag_with_good_name_and_extra_whitespace(self):

        description_entry = """
        
            @namespace          ValidName       


                """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "ValidName", "description": None})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_namespace_tag_with_good_name_and_description_single_line(self):

        description_entry = """
        @namespace MyName
        This is a description.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName", "description": "This is a description."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_namespace_tag_with_good_name_and_description_multiple_lines(self):

        description_entry = """
        @namespace MyName


        This is a description.

        It has multiple paragraphs
        that span over more
        than one line.

        This is the end.
                    

        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName", "description": "This is a description.\nIt has multiple paragraphs that span over more than one line.\nThis is the end."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_namespace_tag_with_multiple_good_namespaces(self):

        description_entry = """
        @namespace MyName1
        This is a description.
        @namespace MyName2
        This is a description 2.
        @namespace MyName3
        This is a description 3.
        @namespace MyName4
        This is a description 4.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName1", "description": "This is a description."})
        expected_docstring_return["namespaces"].append({"name": "MyName2", "description": "This is a description 2."})
        expected_docstring_return["namespaces"].append({"name": "MyName3", "description": "This is a description 3."})
        expected_docstring_return["namespaces"].append({"name": "MyName4", "description": "This is a description 4."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_namespace_tag_with_identical_namespaces(self):
        """
            The parser only pulls out valid namespace information. Because namespaces can be defined in multiple places,
            there is no way to tell at this stage if one has already been defined. Therefore, the docstring parser
            just has to consolidate all valid namespace inputs.
        """

        description_entry = """
        @namespace MyName1
        This is a description.
        @namespace MyName1
        This is a different description of the same namespace name.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName1", "description": "This is a description."})
        expected_docstring_return["namespaces"].append({"name": "MyName1", "description": "This is a different description of the same namespace name."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        
    def test_only_namespace_tag_with_identical_namespaces(self):
        """
            Anything before the @namespace tag should not trigger the parser to pull out the namespace.
        """

        description_entry = """
        my @namespace MyName1
        This is a namespace and description that will not get found
        @namespace MyName2
        This is a different description of the same namespace name.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "my @namespace MyName1 This is a namespace and description that will not get found"
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName2", "description": "This is a different description of the same namespace name."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_namespace_tag_with_invalid_name_not_processed(self):
        """The namespace name must follow Python variable naming validation rules."""

        description_entry = """
        This is a description.

        @namespace 1InvalidName
        @namespace InvalidName With Extra Words
        @namespace Invalid-Name
        @namespace InvalidName#

        @namespace _ValidName
        This should be the only Namespace detected.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "_ValidName", "description": "This should be the only Namespace detected."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_namespace_tag_no_name_does_not_add_namespace(self):
        """
            The parser only pulls out valid namespace information. The namespace has to have a name, or else it should
            get ignored by the parser.
        """

        description_entry = """
        @namespace
        This is a description of a namespace without a name, and this namespace should not appear.
        @namespace MyName
        This is a valid namespace, and should be the only one returned.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName", "description": "This is a valid namespace, and should be the only one returned."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    # ###############################################################
    # # Complex
    # ###############################################################

    def test_only_namespace_tag_with_identical_namespaces(self):
        """
            Anything before the @namespace tag should not trigger the parser to pull out the namespace.
        """

        description_entry = """
        @author Charles Weller
        my @namespace MyName1
        This is a namespace and description between tags that will not get found or tracked
        @namespace MyName2
        This is a different description of the same namespace name.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName2", "description": "This is a different description of the same namespace name."})
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "Charles Weller", "email": None})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_namespace_tag_surrounded_by_other_tags(self):
        self.maxDiff = None

        description_entry = """This one also has a description in it.

        @namespace MyName
        This is a description.
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
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName", "description": "This is a description."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_example_tag_multiple_namespace_and_other_tags(self):

        description_entry = """
        This is a description.

        @namespace MyName1
        This is a description.
        @param the_var A variable of any type
        @returns It just prints to the console
        @example
        print(myvar1)
        @example
        print(myvar2)
        @namespace MyName2
        This is a description.
        @example This one has a caption
        print(myvar3)
        @example
        print(myvar4)
        @returns This is an overriding returns tag
        @namespace MyName3
        This is a description.
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
        expected_docstring_return["namespaces"] = []
        expected_docstring_return["namespaces"].append({"name": "MyName1", "description": "This is a description."})
        expected_docstring_return["namespaces"].append({"name": "MyName2", "description": "This is a description."})
        expected_docstring_return["namespaces"].append({"name": "MyName3", "description": "This is a description."})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
