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

    def test_only_single_parameter_description_spills_over_with_paragraph_breaks(self):
        self.maxDiff = None
        description_entry = """
            @param test_param This is a description of a test parameter.
            Its description goes onto a second line.

            Additionally, it has three paragraphs. This is the first.

            This is the second.
            @param test_param2 This is a second test parameter.
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"test_param": "This is a description of a test parameter. Its description goes onto a second line.\nAdditionally, it has three paragraphs. This is the first.\nThis is the second."})
        expected_docstring_return["parameters"].append({"test_param2": "This is a second test parameter."})
        self.assertDictEqual(expected_docstring_return, returned_dict)


    ###############################################################
    # Complex
    ###############################################################

    def test_good_param_detected_before_and_after_other_tags(self):
        self.maxDiff = None
        description_entry = """
            @example
            print('test1')
            @param my_test_parameter1 This is a description of a test parameter 1.

            It has a second paragraph.
            @example
            print('test2')
            @param my_test_parameter2 This is a description of a test parameter 2
            @returns This is a description of the return value
        """
        expected_docstring_return = deepcopy(blank_parse_docstring_return)
        
        returned_dict = parse_docstring(description_entry)
        expected_docstring_return["parameters"].append({"my_test_parameter1": "This is a description of a test parameter 1.\nIt has a second paragraph."})
        expected_docstring_return["parameters"].append({"my_test_parameter2": "This is a description of a test parameter 2"})
        expected_docstring_return["examples"] = []
        expected_docstring_return["examples"].append({"caption": None, "code": "print('test1')"})
        expected_docstring_return["examples"].append({"caption": None, "code": "print('test2')"})
        expected_docstring_return["returns"] = "This is a description of the return value"

        self.assertDictEqual(expected_docstring_return, returned_dict)