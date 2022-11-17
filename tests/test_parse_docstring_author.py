from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Author(unittest.TestCase):

    ###############################################################
    # Author
    ###############################################################

    def test_only_author_tag_no_inputs(self):

        description_entry = """@author  """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_with_name_only(self):

        description_entry = """@author John Doe"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": None})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_with_name_and_email(self):

        description_entry = """@author John Doe [john.doe@somedomain.com]"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": "john.doe@somedomain.com"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_with_extra_whitespace_no_email(self):

        description_entry = """
        
                @author John Doe    

                     """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": None})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_with_extra_whitespace_with_email(self):

        description_entry = """
        
                @author John M.  Doe    [ some.email@myemaildomain.com  ] 

                     """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John M.  Doe", "email": "some.email@myemaildomain.com"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_with_description(self):

        description_entry = """
        This is a description.
        
        @author John Doe [john.doe@somedomain.com]"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": "john.doe@somedomain.com"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_with_description_and_multiple_authors(self):

        description_entry = """
        This is a description.
        
        @author John Doe [john.doe@somedomain.com]
        @author Frank Dorman [frank.dorman@somedomain.com]
        @author Jane M. Doe
        @author Hannah Marie Smith III [hannahsmith@somedomain.com]"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": "john.doe@somedomain.com"})
        expected_docstring_return["author"].append({"name": "Frank Dorman", "email": "frank.dorman@somedomain.com"})
        expected_docstring_return["author"].append({"name": "Jane M. Doe", "email": None})
        expected_docstring_return["author"].append({"name": "Hannah Marie Smith III", "email": "hannahsmith@somedomain.com"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_not_recognized_with_bad_syntax_leading_text(self):

        description_entry = """
        This is a description.
        
        this will not record an @author John Doe [john.doe@somedomain.com]"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description.\nthis will not record an @author John Doe [john.doe@somedomain.com]"

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_long_line_of_text_for_name(self):

        description_entry = """
        This is a description.
        
        @author John Doe john.doe@somedomain.com, Frank Dorman (frank.dorman@somedomain.com), Jane M. Doe, Hannah Marie Smith III hannahsmith@somedomain.com
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe john.doe@somedomain.com, Frank Dorman (frank.dorman@somedomain.com), Jane M. Doe, Hannah Marie Smith III hannahsmith@somedomain.com", "email": None})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_no_email_close_bracket(self):

        description_entry = """@author John Doe [john.doe@somedomain.com"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe [john.doe@somedomain.com", "email": None})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_no_email_open_bracket(self):

        description_entry = """@author John Doe john.doe@somedomain.com]"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe john.doe@somedomain.com]", "email": None})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_extra_text_after_email_ignored(self):

        description_entry = """
            @author John Doe [john.doe@somedomain.com]Sometext
            @author John Doe The Second [john.doe@somedomain.com] [john.doe@somedomain.com]
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": "john.doe@somedomain.com"})
        expected_docstring_return["author"].append({"name": "John Doe The Second", "email": "john.doe@somedomain.com"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_does_not_grab_info_from_next_line(self):

        description_entry = """
        This is a description.
        
        @author John Doe
        and Jane Doe
        @author Dr. Doak"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": None})
        expected_docstring_return["author"].append({"name": "Dr. Doak", "email": None})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_must_have_space_after_author(self):

        description_entry = """
        This is a description.
        
        @author John Doe
        @authorJane Doe
        @author Dr. Doak"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": None})
        expected_docstring_return["author"].append({"name": "Dr. Doak", "email": None})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_author_tag_name_just_email(self):

        description_entry = """@author [john.doe@somedomain.com]"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": None, "email": "john.doe@somedomain.com"})

    # ###############################################################
    # # Complex
    # ###############################################################

    def test_author_tag_surrounded_by_other_tags(self):

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @throws An error with no type 1
        @todo Some stuff
        @author John Doe [john.doe@somedomain.com]
        @param SecondParamName This is another param description
        @returns This is the ultimate return text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("Some stuff")
        expected_docstring_return["throws"] = []
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": "john.doe@somedomain.com"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_author_tag_multiple_authors_and_other_tags(self):

        description_entry = """
        This is a description.

        @author John Doe [john.doe@somedomain.com]
        @param the_var A variable of any type
        @returns It just prints to the console
        @todo Some stuff
        @author Frank Dorman [frank.dorman@somedomain.com]
        @example
        print(myvar1)
        @example
        print(myvar2)
        @example This one has a caption
        print(myvar3)
        @todo Some more stuff
        and this @todo is part of it
        @example
        print(myvar4)
        @returns This is an overriding returns tag
        @author Jane M. Doe
        @todo Some final stuff
        @author Hannah Marie Smith III [hannahsmith@somedomain.com]
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["parameters"] = []
        expected_docstring_return["parameters"].append({"the_var": "A variable of any type"})
        expected_docstring_return["returns"] = "This is an overriding returns tag"
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("Some stuff")
        expected_docstring_return["todo"].append("Some more stuff and this @todo is part of it")
        expected_docstring_return["todo"].append("Some final stuff")
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar1)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar2)"})
        expected_docstring_return["examples"].append({"caption": "This one has a caption", "code": "print(myvar3)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar4)"})
        expected_docstring_return["author"] = []
        expected_docstring_return["author"].append({"name": "John Doe", "email": "john.doe@somedomain.com"})
        expected_docstring_return["author"].append({"name": "Frank Dorman", "email": "frank.dorman@somedomain.com"})
        expected_docstring_return["author"].append({"name": "Jane M. Doe", "email": None})
        expected_docstring_return["author"].append({"name": "Hannah Marie Smith III", "email": "hannahsmith@somedomain.com"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
