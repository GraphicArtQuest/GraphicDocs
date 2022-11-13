from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring(unittest.TestCase):

    ###############################################################
    # Validation Functions
    ###############################################################
    def test_non_string_inputs_return_none(self):
        inputs = [
            2,
            3.14159,
            False,
            True,
            {"a": "Some String"},
            ["A", "B", "C"],
            ["Some String"],
            ("A", "B", "C"),
            None
        ]

        for input in inputs:
            self.assertIsNone(parse_docstring(input))

    def test_empty_string_returns_blank_list(self):
        returned_dict = parse_docstring("""""")
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_empty_string_with_extra_whitespace_returns_blank_list(self):
        returned_dict = parse_docstring("""
        
        
        
        
        """)
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        self.assertDictEqual(expected_docstring_return, returned_dict)


    ###############################################################
    # Docstring Only - No tags
    ###############################################################
    
    def test_no_tags_single_line_string(self):
        description_entry = """This is a single line"""
        expected_docstring_return = deepcopy(blank_parse_docstring_return)

        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = description_entry
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_no_tags_multi_line_string(self):
        description_entry = """
            This is a multiple line description.    
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiple line description."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_no_tags_multi_line_paragraph(self):
        description_entry = """
            This is a multiple line description. It goes over many many lines. It has a very long description that will cause
            the sentence to run over 120 characters. But it still keeps going. This description only has a single entry in it,
            and is does not have more than one paragraph.
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiple line description. It goes over many many lines. It has a very long description that will cause the sentence to run over 120 characters. But it still keeps going. This description only has a single entry in it, and is does not have more than one paragraph."
        
        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_no_tags_multi_line_multi_paragraph_plus_extra_space_at_end(self):
        description_entry = """
            This is a multiple line description. It goes over many many lines. It has a very long description that will cause
            the sentence to run over 120 characters. But it still keeps going.
            
            This description has multiple paragraphs.

            The above paragraph only covered a single line.
            This paragraph covers multiple lines, but should still be treated as a single paragraph.



        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiple line description. It goes over many many lines. It has a very long description that will cause the sentence to run over 120 characters. But it still keeps going.\nThis description has multiple paragraphs.\nThe above paragraph only covered a single line. This paragraph covers multiple lines, but should still be treated as a single paragraph."

        self.assertDictEqual(expected_docstring_return, returned_dict)
    
    def test_no_tags_bulleted_list(self):
        description_entry = """
            This is a multiple line description. It goes over many many lines. It has a very long description that will cause
            the sentence to run over 120 characters. But it still keeps going.
            
            This description also has a bulleted list:
            - One
            - Two
            - Three
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiple line description. It goes over many many lines. It has a very long description that will cause the sentence to run over 120 characters. But it still keeps going.\nThis description also has a bulleted list:\n- One\n- Two\n- Three"

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_no_tags_bulleted_list_no_space(self):
        """Omitting the space after the '-' character will not treat it as an unordered list."""
        description_entry = """
            This is a multiple line description. It goes over many many lines. It has a very long description that will cause
            the sentence to run over 120 characters. But it still keeps going.
            
            This description also has a bulleted list:
            -One
            -Two
            -Three
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiple line description. It goes over many many lines. It has a very long description that will cause the sentence to run over 120 characters. But it still keeps going.\nThis description also has a bulleted list: -One -Two -Three"

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_no_tags_unordered_list(self):
        description_entry = """
            This is a multiple line description. It goes over many many lines. It has a very long description that will cause
            the sentence to run over 120 characters. But it still keeps going.
            
            This description also has a bulleted list:
            <ul>One
            <ul>Two
            <ul>Three
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiple line description. It goes over many many lines. It has a very long description that will cause the sentence to run over 120 characters. But it still keeps going.\nThis description also has a bulleted list:\n- One\n- Two\n- Three"

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_no_tags_numbered_list(self):
        description_entry = """
            This description also has a bulleted list:
                <ol>1. One
                <ol>2. Two
                <ol>3. Three
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This description also has a bulleted list:\n1. One\n2. Two\n3. Three"

        self.assertDictEqual(expected_docstring_return, returned_dict)
