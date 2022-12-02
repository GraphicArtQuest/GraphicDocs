import json
import os
import unittest
import uuid

from src.core import Core
from src.core import initial_default_settings

def get_random_config_name():
    return "testing_" + uuid.uuid1()

def create_default_config_file():
    config_file_path = os.getcwd()
    return config_file_path

class TestCoreConfig(unittest.TestCase):

    def new_temp_config_path(self, base_directory: str=os.path.dirname(__file__)) -> str:
        """Creates an empty config file in the same directory as this test script"""
        return os.path.join(base_directory, "test_config_" + str(uuid.uuid1()) + ".config")
    
    def createFile(self, path: str):
        self.file = open(path, "w+")

    def deleteFile(self, path: str):
        self.file.close()
        os.remove(path)

    def setUp(self):
        self.config_file_path = self.new_temp_config_path()
        self.createFile(self.config_file_path)

    def tearDown(self):
        self.file.close()
        self.deleteFile(self.config_file_path)
        self.config_file_path = ""


    ###############################################################
    # Basic Config Inputs
    ###############################################################

    def test_default_core_instance(self):
        """Calling with no arguments yields a successful Core object."""
        core = Core()
        self.assertIsInstance(core, Core)
        self.assertEqual(core.config, initial_default_settings)

    def test_will_convert_all_config_inputs_to_string(self):
        """If provided with an input for the user_defined_config, it should convert it to a string without regard
        to if it will be a valid config file path or not."""
        self.maxDiff = None

        inputs = [
            2,
            3.14159,
            False,
            True,
            {"a": "Some String"},
            ["A", "B", "C"],
            ["Some String"],
            ("A", "B", "C"),
            None,
            str,    # Class references
            unittest,   # Module references
            Core._process_user_defined_config   # Function references
        ]

        for input in inputs:
            self.assertIsInstance(Core(input), Core)
            self.assertEqual(Core(input).user_defined_config_path, str(input))
    
    def test_config_file_not_specified_but_found_in_working_directory(self):
        """If a config file is not specified, look for a default one ('graphicdocs.config') in the working directory."""
        
        # First, check to make sure there isn't already a default file here by this name. If there is, we can use that.
        #   Otherwise, we need to create a new one.
        test_config_path = os.path.join(os.getcwd(), "graphicdocs.config")
        test_config_already_exists = os.path.exists(test_config_path)
        if not test_config_already_exists:
            self.working_dir_file = open(test_config_path, "w")
        
        self.assertEqual(Core().user_defined_config_path, test_config_path)

        if not test_config_already_exists:
            # Only delete our created mock testing config, not any other config that was already provided.
            self.working_dir_file.close()
            self.deleteFile(test_config_path)
    
    def test_config_file_not_specified_and_not_found(self):
        """No config file specified, no config in working directory. Use default configs."""

        # First, check to see if a config already exists here. If so, we need to rename it so we don't destroy settings.
        test_config_path = os.path.join(os.getcwd(), "graphicdocs.config")
        test_config_already_exists = os.path.exists(test_config_path)
        if test_config_already_exists:
            temp_path = self.new_temp_config_path()
            os.rename(test_config_path, temp_path)
        
        self.assertEqual(Core().user_defined_config_path, "")

        if test_config_already_exists:
            # Restore the original file
            os.rename(temp_path, test_config_path)
    
    def test_config_file_specified_but_absolute_path_bad(self):
        """Test a valid filepath that COULD exist, but doesn't. The user_defined_config_path variable should be
        set, but no default configs should change."""
        bad_config_file_path = self.new_temp_config_path()

        core = Core(bad_config_file_path)
        self.assertEqual(core.user_defined_config_path, bad_config_file_path)
        self.assertEqual(core.config, initial_default_settings)
    
    def test_empty_config_file(self):
        """Test a valid config filepath that exists, but has nothing in it."""

        core = Core(self.config_file_path)
        self.assertEqual(core.config, initial_default_settings)

    ###############################################################
    # Changing Config Default Values
    ###############################################################

    def test_config_file_changes_default_value_destination(self):
        """Test the config file accepts valid input for the 'destination' variable."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [1] = Variable to JSON stringify, [2] = Expected absolute path string it gets back
            ('', os.getcwd()),
            ('2', os.path.join(os.getcwd(), "2")),
            (2, os.path.join(os.getcwd(), "2")),
            (3.14159, os.path.join(os.getcwd(), "3.14159")),
            ("abc", os.path.join(os.getcwd(), "abc")),
            (False, os.path.join(os.getcwd(), "False")),
            (True, os.path.join(os.getcwd(), "True")),
            ({"a": "Some String"}, os.getcwd()),    # Yields an invalid filename character (the colon ':')
            (["A", "B", "C"], os.path.join(os.getcwd(), "['A', 'B', 'C']")),
            (["Some String"], os.path.join(os.getcwd(), "['Some String']")),
            (("A", "B", "C"), os.path.join(os.getcwd(), "['A', 'B', 'C']")),
            (None, os.path.join(os.getcwd(), "None")),
            ([], os.path.join(os.getcwd(), "[]")),
            ((), os.path.join(os.getcwd(), "[]")),
            (0, os.path.join(os.getcwd(), "0")),

            (str, os.getcwd()),    # Class references
            (unittest, os.getcwd()),   # Module references
            (Core._process_user_defined_config, os.getcwd()),   # Function references,
            (os.getcwd(), os.getcwd()),
            (os.path.join(os.getcwd(), "abc"), os.path.join(os.getcwd(), "abc")),
            
            (".abc", os.path.join(os.getcwd(), ".abc")),
            ("./abc", os.path.join(os.getcwd(), "abc")),
            ("../abc", os.path.join(os.path.dirname(os.getcwd()), "abc")),  # .. should go up one level
            ("../../abc", os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), "abc")),  # .. Go up two levels
        ]

        for input in inputs:
            try:
                config_text = json.dumps({"destination": input[0]})
            except:
                config_text = json.dumps({"destination": ""}) # Object refs can't serialize, so just use empty string

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(config_text)
            tempfile.close()

            core = Core(self.config_file_path)

            expected = os.path.join(os.getcwd(), input[1])
            received = core.config["destination"]

            self.assertEqual(expected, received)

    def test_config_file_changes_default_value_destination_overwrite(self):
        """Test the config file accepts valid input for the 'destination_overwrite' variable."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [1] = Variable to JSON stringify, [2] = Expected processed response back
            ('', False),
            ('2', True),
            (2, True),
            (3.14159, True),
            ("abc", True),
            (False, False),
            (True, True),
            ({"a": "Some String"}, True),
            (["A", "B", "C"], True),
            (["Some String"], True),
            (("A", "B", "C"), True),
            (None, False),
            ([], False),
            ((), False),
            (0, False),

            (str, False),    # Class references
            (unittest, False),   # Module references
            (Core._process_user_defined_config, False),   # Function references,
            (os.getcwd(), True),
        ]

        for input in inputs:
            try:
                config_text = json.dumps({"destination_overwrite": input[0]})
            except:
                config_text = json.dumps({"destination_overwrite": ""}) # Object refs can't serialize, so just use empty string

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(config_text)
            tempfile.close()

            core = Core(self.config_file_path)

            expected = input[1]
            received = core.config["destination_overwrite"]

            self.assertEqual(expected, received)

    def test_config_file_changes_default_value_plugins(self):
        """Test the config file accepts valid input for the 'plugins' variable."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [1] = Variable to JSON stringify, [2] = Expected processed response back
            ('', []),
            ('2', []),
            (2, []),
            (3.14159, []),
            ("abc", []),
            (False, []),
            (True, []),
            ({"a": "Some String"}, []),
            (["A", "B", "C"], ["A", "B", "C"]),
            ([1, 2, 3], ["1", "2", "3"]),
            ([1, 2, "A"], ["1", "2", "A"]),
            (["Some String"], ["Some String"]),
            (["../Some Plugin"], ["../Some Plugin"]),
            (("A", "B", "C"), ["A", "B", "C"]),

            ((os.path.join(os.getcwd(), "A"), os.path.join(os.getcwd(), "B"), os.path.join(os.getcwd(), "C")), [
                os.path.join(os.getcwd(), "A"),
                os.path.join(os.getcwd(), "B"),
                os.path.join(os.getcwd(), "C")
            ]),
            (None, []),
            ([], []),
            ((), []),
            (0, []),

            (str, []),    # Class references
            (unittest, []),   # Module references
            (Core._process_user_defined_config, []),   # Function references,
            (os.getcwd(), []),
        ]

        for input in inputs:
            try:
                config_text = json.dumps({"plugins": input[0]})
            except:
                config_text = json.dumps({"plugins": ""}) # Object refs can't serialize, so just use empty string

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(config_text)
            tempfile.close()

            core = Core(self.config_file_path)

            expected = input[1]
            received = core.config["plugins"]

            self.assertEqual(expected, received)

    def test_config_file_changes_default_value_plugins(self):
        """Test the config file accepts valid input for the 'source' variable."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [1] = Variable to JSON stringify, [2] = Expected processed response back
            ('', []),
            ('2', []),
            (2, []),
            (3.14159, []),
            ("abc", []),
            (False, []),
            (True, []),
            ({"a": "Some String"}, []),
            (["A", "B", "C"], ["A", "B", "C"]),
            ([1, 2, 3], ["1", "2", "3"]),
            ([1, 2, "A"], ["1", "2", "A"]),
            (["Some String"], ["Some String"]),
            (["../Some Plugin"], ["../Some Plugin"]),
            (("A", "B", "C"), ["A", "B", "C"]),
            ((os.path.join(os.getcwd(), "A"), os.path.join(os.getcwd(), "B"), os.path.join(os.getcwd(), "C")), [
                os.path.join(os.getcwd(), "A"),
                os.path.join(os.getcwd(), "B"),
                os.path.join(os.getcwd(), "C")
            ]),
            (None, []),
            ([], []),
            ((), []),
            (0, []),

            (str, []),    # Class references
            (unittest, []),   # Module references
            (Core._process_user_defined_config, []),   # Function references,
            (os.getcwd(), []),
        ]

        for input in inputs:
            try:
                config_text = json.dumps({"source": input[0]})
            except:
                config_text = json.dumps({"source": ""}) # Object refs can't serialize, so just use empty string

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(config_text)
            tempfile.close()

            core = Core(self.config_file_path)

            expected = input[1]
            received = core.config["source"]

            self.assertEqual(expected, received)

    def test_config_file_changes_default_value_source_exclude_pattern(self):
        """Test the config file accepts valid input for the 'source_exclude_pattern' variable."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [1] = Variable to JSON stringify, [2] = Expected processed response back
            ('', []),
            ('2', []),
            (2, []),
            (3.14159, []),
            ("abc", []),
            (False, []),
            (True, []),
            ({"a": "Some String"}, []),
            (["A", "B", "C"], ["A", "B", "C"]),
            ([1, 2, 3], ["1", "2", "3"]),
            ([1, 2, "^[\w]"], ["1", "2", "^[\w]"]),
            (["Some String"], ["Some String"]),
            (("A", "B", "C"), ["A", "B", "C"]),
            (None, []),
            ([], []),
            ((), []),
            (0, []),

            (str, []),    # Class references
            (unittest, []),   # Module references
            (Core._process_user_defined_config, []),   # Function references,
            (os.getcwd(), []),
        ]

        for input in inputs:
            try:
                config_text = json.dumps({"source_exclude_pattern": input[0]})
            except:
                config_text = json.dumps({"source_exclude_pattern": ""}) # Object refs can't serialize, so just use empty string

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(config_text)
            tempfile.close()

            core = Core(self.config_file_path)

            expected = input[1]
            received = core.config["source_exclude_pattern"]

            self.assertEqual(expected, received)

    def test_config_file_changes_default_value_template(self):
        """Test the config file accepts valid input for the 'template' variable."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [1] = Variable to JSON stringify, [2] = Expected absolute path string it gets back
            ('', ''),
            ('2', '2'),
            (2, '2'),
            (3.14159, "3.14159"),
            ("abc", "abc"),
            ("graphic_md", "graphic_md"),
            (False, "False"),
            (True, "True"),
            ({'a': 'Some String'}, "{'a': 'Some String'}"),
            (["A", "B", "C"], "['A', 'B', 'C']"),
            (['Some String'], "['Some String']"),
            (("A", "B", "C"), "['A', 'B', 'C']"),
            (None, "None"),
            ([], "[]"),
            ((), "[]"),
            (0, "0"),

            (str, ""),    # Class references
            (unittest, ""),   # Module references
            (Core._process_user_defined_config, ""),   # Function references,
            (os.getcwd(), os.getcwd()),
            (os.path.join(os.getcwd(), "abc"), os.path.join(os.getcwd(), "abc")),
            
            (".abc", ".abc"),
            ("./abc", "./abc"),
            ("../abc", "../abc"),  # .. should go up one level
            ("../../abc", "../../abc"),  # .. Go up two levels
        ]

        for input in inputs:
            try:
                config_text = json.dumps({"template": input[0]})
            except:
                config_text = json.dumps({"template": ""}) # Object refs can't serialize, so just use empty string

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(config_text)
            tempfile.close()

            core = Core(self.config_file_path)

            expected = input[1]
            received = core.config["template"]

            self.assertEqual(expected, received)

    def test_config_file_changes_default_value_verbose(self):
        """Test the config file accepts valid input for the 'verbose' variable."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [1] = Variable to JSON stringify, [2] = Expected processed response back
            ('', False),
            ('2', True),
            (2, True),
            (3.14159, True),
            ("abc", True),
            (False, False),
            (True, True),
            ({"a": "Some String"}, True),
            (["A", "B", "C"], True),
            (["Some String"], True),
            (("A", "B", "C"), True),
            (None, False),
            ([], False),
            ((), False),
            (0, False),

            (str, False),    # Class references
            (unittest, False),   # Module references
            (Core._process_user_defined_config, False),   # Function references,
            (os.getcwd(), True),
            
        ]

        for input in inputs:
            try:
                config_text = json.dumps({"verbose": input[0]})
            except:
                config_text = json.dumps({"verbose": ""}) # Object refs can't serialize, so just use empty string

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(config_text)
            tempfile.close()

            core = Core(self.config_file_path)

            expected = input[1]
            received = core.config["verbose"]

            self.assertEqual(expected, received)


    ###############################################################
    # Unrecognized Settings
    ###############################################################

    def test_config_file_add_new_unrecognized_key(self):
        """Test the config file accepts unrecognized setting keys exactly as they are."""
        self.maxDiff = None

        inputs = [
            # Tuple of: [0] = Key to JSON stringify (must be strings), [1] = Value of entry
            ('2', True),
            ("abc", True),
            ("False", True),
            ("True", True),
            ("None", None),           
            ("MyCustomKey", [1, 2, 3]),
            ("MyCustomKey", ['1', '2', '3']),
            ("MyCustomKey", [True, False, None]),
            ("MyCustomKey", {"1": True, "2": False, "3": None}),
            ("MyCustomKey", [{"1": True, "2": False, "3": None}, {"1": True, "2": False, "3": None}]),
            ("MyCustomKey", {"A": {"1": True, "2": False, "3": None}, "B": {"1": True, "2": False, "3": None}})
        ]

        for input in inputs:

            tempfile = open(self.config_file_path, "w+")
            tempfile.write(json.dumps({input[0]: input[1]}))
            tempfile.close()

            core = Core(self.config_file_path)

            expected = input[1]
            received = core.config[input[0]]
            # print("\n" +str(input[0]) + "\nExpected: ", expected, "\nReceived: ", received)

            self.assertEqual(expected, received)