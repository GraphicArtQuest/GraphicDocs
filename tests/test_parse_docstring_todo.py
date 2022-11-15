from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Todo(unittest.TestCase):

    ###############################################################
    # Todo
    ###############################################################

    def test_only_todo_tag_with_good_example(self):

        description_entry = """@todo I need to do some stuff still."""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("I need to do some stuff still.")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_todo_tag_with_extra_whitespace(self):

        description_entry = """
        
                @todo I need to do some stuff still.    

                     """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("I need to do some stuff still.")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)    

    def test_only_multiple_todos_plus_description(self):

        description_entry = """
        This is a function that does some stuff.

        @todo I need to do some stuff still.
        @todo I need to do some more stuff still.
        @todo How is the stuff not done.
        @todo I think this got away from me.
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("I need to do some stuff still.")
        expected_docstring_return["todo"].append("I need to do some more stuff still.")
        expected_docstring_return["todo"].append("How is the stuff not done.")
        expected_docstring_return["todo"].append("I think this got away from me.")
        expected_docstring_return["description"] = "This is a function that does some stuff."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_todo_tag_with_incorrect_syntax(self):

        description_entry = """marking something as @todo does nothing"""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "marking something as @todo does nothing"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_todo_tag_with_multiple_paragraphs(self):

        description_entry = """@todo I need to do some stuff still.
        This rolled over a line.

        This is a second paragraph.
        

        @todo This is a second todo.
        
        It also has two paragraphs."""

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("I need to do some stuff still. This rolled over a line.\nThis is a second paragraph.")
        expected_docstring_return["todo"].append("This is a second todo.\nIt also has two paragraphs.")
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    ###############################################################
    # Complex
    ###############################################################

    def test_todo_tag_surrounded_by_other_tags(self):

        description_entry = """This one also has a description in it.

        @param MyParam This is a param description
        @throws An error with no type 1
        @todo Some stuff
        @param SecondParamName This is another param description
        @returns This is the ultimate return text
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This one also has a description in it."
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("Some stuff")
        expected_docstring_return["throws"].append({"type": None, "description": "An error with no type 1"})
        expected_docstring_return["parameters"].append({"MyParam": "This is a param description"})
        expected_docstring_return["parameters"].append({"SecondParamName": "This is another param description"})
        expected_docstring_return["returns"] = "This is the ultimate return text"
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_example_tag_multiple_examples_and_other_tags(self):

        description_entry = """
        This is a description.

        @param the_var A variable of any type
        @returns It just prints to the console
        @todo Some stuff
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
        @todo Some final stuff
        """

        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a description."
        expected_docstring_return["parameters"].append({"the_var": "A variable of any type"})
        expected_docstring_return["returns"] = "This is an overriding returns tag"
        expected_docstring_return["todo"] = []
        expected_docstring_return["todo"].append("Some stuff")
        expected_docstring_return["todo"].append("Some more stuff and this @todo is part of it")
        expected_docstring_return["todo"].append("Some final stuff")
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar1)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar2)"})
        expected_docstring_return["examples"].append({"caption": "This one has a caption", "code": "print(myvar3)"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print(myvar4)"})
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
        