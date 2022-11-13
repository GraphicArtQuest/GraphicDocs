from copy import deepcopy
import unittest

from tests.__init__ import blank_parse_docstring_return
from src.parser import parse_docstring

class TestParseDocstring_Param(unittest.TestCase):

    ###############################################################
    # Parameters
    ###############################################################

    def test_only_single_parameter_no_desc(self):
        description_entry = """
            @param my_test_parameter This is a description of a test parameter
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"my_test_parameter": "This is a description of a test parameter"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_multiple_parameters_no_desc(self):
        description_entry = """
            @param my_test_parameter1 This is a description of a test parameter 1
            @param my_test_parameter2 This is a description of a test parameter 2
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_multiple_parameters_with_desc(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description of a test parameter 1
            @param my_test_parameter2 This is a description of a test parameter 2
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_single_multi_line_parameters_with_desc(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description
            of a test parameter 1
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_more_than_one_multi_line_parameters_with_desc(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description
            of a test parameter 1
            
            @param my_test_parameter2 This is a description
            of a test parameter 2
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_single_four_line_parameters_with_desc(self):
        description_entry = """
            This is a multiline description.
            It tells what this function does.

            @param my_test_parameter1 This is a description
            of a multi line test parameter 1
            with a third line
            and a fourth line.
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["description"] = "This is a multiline description. It tells what this function does."
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a multi line test parameter 1 with a third line and a fourth line."})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_multiple_parameters_with_same_name(self):
        description_entry = """
            @param my_test_parameter1 This is a description of a test parameter 1
            @param my_test_parameter1 This is a description of a test parameter 2 but misnamed so it overwrote
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 2 but misnamed so it overwrote"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_good_param_detected_after_bad(self):
        description_entry = """
            @parm my_test_parameter1 This should do nothing because it mispelled param
            @param my_test_parameter2 This is a description of a test parameter 2
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_good_param_detected_before_and_after_bad(self):
        description_entry = """
            @param my_test_parameter1 This is a description of a test parameter 1
            @parm my_test_parameter2 This should do nothing because it mispelled param
            @param my_test_parameter3 This is a description of a test parameter 3
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1"})
        expected_docstring_return["parameters"].append({"my_test_parameter3": "This is a description of a test parameter 3"})

        self.assertDictEqual(expected_docstring_return, returned_dict)

    def test_only_single_parameter_no_desc_extra_space_before_parameter_name(self):
        """The extra spaces between the @param tag and the parameter name and the name/description should not cause a problem"""
        description_entry = """
                 @param    my_test_parameter      This is a description of a test parameter   
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"my_test_parameter": "This is a description of a test parameter"})

        self.assertDictEqual(expected_docstring_return, returned_dict)
