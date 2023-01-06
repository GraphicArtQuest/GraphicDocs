import os
import re
import unittest
import uuid

from src.core import Core

class TestCoreParser(unittest.TestCase):

    ###############################################################
    # Parse Build - Cause Errors
    ###############################################################

    def test_parse_no_targets(self):
        """Should fire appropriate hook if no parsing targets"""

        config = {
            "source": [],
        }
        core = Core(config)

        self.assertTrue('no_parsing_targets_specified' in core.actions.done)
        self.assertTrue('parsed_module' not in core.actions.done)
        self.assertTrue('unable_to_load_module' not in core.actions.done)
        self.assertTrue('unable_to_parse' not in core.actions.done)
        self.assertTrue('parsing_complete' not in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_build_cannot_load_module(self):
        """Should fail to parse when trying to load a nonsense file that doesn't exist"""

        config = {"source": [os.path.join(".", str(uuid.uuid1()) + ".py")]}    # Guarantee file doesn't exist

        core = Core(config)

        self.assertTrue('no_parsing_targets_specified' not in core.actions.done)
        self.assertTrue('parsed_module' not in core.actions.done)
        self.assertTrue('unable_to_load_module' in core.actions.done)
        self.assertTrue('unable_to_parse' not in core.actions.done)
        self.assertTrue('parsing_complete' not in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_build_unable_to_parse(self):
        """ Return no results when the file could not be parsed.

            This test has been temporarily omitted because I cannot figure out a way to reliably test it. In the event
            the parser encounters an error, it will return `None`. The build function detects this and prevents moving
            forward. Unfortunately, I have patched all the error inducing issues in the parser so far, so I have not
            found a way to come back and introduce other errors to test this from here.

            I am leaving this test here as a placeholder.
        """
        pass
        # config = {"source": [os.path.join(".", "tests")]}

        # core = Core(config)

        # self.assertTrue('no_parsing_targets_specified' not in core.actions.done)
        # self.assertTrue('parsed_module' in core.actions.done)
        # self.assertTrue('unable_to_load_module' not in core.actions.done)
        # self.assertTrue('unable_to_parse' in core.actions.done)
        # self.assertTrue('parsing_complete' not in core.actions.done)
        # self.assertTrue('core_loaded' in core.actions.done)

    def test_build_individual_files_no_exclude(self):
        """Should parse four out of four from the provided source list"""

        config = {
            "source": [
                os.path.join(".", "tests", "core", "test_core_config.py"),  # Guaranteed these files exist
                os.path.join(".", "tests", "core", "test_core_hooks.py"),
                os.path.join(".", "tests", "core", "test_core_plugins.py"),
                os.path.join(".", "tests", "core", "test_core_template.py")
            ]
        }

        core = Core(config)

        self.assertTrue('no_parsing_targets_specified' not in core.actions.done)
        self.assertTrue('parsed_module' in core.actions.done)
        self.assertTrue('unable_to_load_module' not in core.actions.done)
        self.assertTrue('unable_to_parse' not in core.actions.done)
        self.assertTrue('parsing_complete' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_build_individual_files_with_exclude(self):
        """Should parse 3 out of 10 files due to matches against the exclude pattern."""

        config = {
            "source": [
                os.path.join(".", "tests", "core", "test_core_config.py"),  # Guaranteed these files exist
                os.path.join(".", "tests", "core", "test_core_hooks.py"),
                os.path.join(".", "tests", "core", "test_core_plugins.py"),
                os.path.join(".", "tests", "core", "test_core_template.py"),
                os.path.join(".", "tests", "parser", "test_parse_class.py"),
                os.path.join(".", "tests", "parser", "test_parse_docstring.py"),
                os.path.join(".", "tests", "parser", "test_parse_function.py"),
                os.path.join(".", "tests", "parser", "test_parse_module.py"),
                os.path.join(".", "tests", "parser", "__init__.py"),
                os.path.join(".", "tests", "templates", "test_graphic_md.py"),
            ],
            "source_exclude_pattern": ['parse.*(.py)', 'template']
        }

        core = Core(config)

        self.assertTrue('no_parsing_targets_specified' not in core.actions.done)
        self.assertTrue('parsed_module' in core.actions.done)
        self.assertTrue('unable_to_load_module' not in core.actions.done)
        self.assertTrue('unable_to_parse' not in core.actions.done)
        self.assertTrue('parsing_complete' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

        self.assertEqual(3, core.actions.done.count('parsed_module'))

    def test_build_folders_no_depth_limit(self):
        """ Should parse all the .py files in the provided folder.
            Note: This also tests excluding folders as the built in `__pycache__` exclusions are validated."""

        config = {
            "source": [
                os.path.join(".", "tests", "core"),  # Guaranteed the files in this folder exist
            ],
        }

        core = Core(config)

        self.assertTrue('no_parsing_targets_specified' not in core.actions.done)
        self.assertTrue('parsed_module' in core.actions.done)
        self.assertTrue('unable_to_load_module' not in core.actions.done)
        self.assertTrue('unable_to_parse' not in core.actions.done)
        self.assertTrue('parsing_complete' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_build_folders_with_depth_limit(self):
        """Should parse everything up to the config `source_depth` limit and no further."""

        config = {
            "source": [
                os.path.join(".", "tests"),  # Guaranteed the files in this folder exist
            ],
            "source_depth": 2
        }

        core = Core(config)

        self.assertTrue('no_parsing_targets_specified' not in core.actions.done)
        self.assertTrue('parsed_module' in core.actions.done)
        self.assertTrue('unable_to_load_module' not in core.actions.done)
        self.assertTrue('unable_to_parse' not in core.actions.done)
        self.assertTrue('parsing_complete' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

        # By starting at the tests folder and limiting to 2 folders deep, the input files should never get searched.
        #   Therefore, if one of these does get parsed, it did not succeed.
        unreachable_file_was_reached = False
        nonreachable_filename = r"tests\\parser\\input_files\\testmodule_only_docstring.py"

        reachable_filename_was_reached = False
        reachable_filename = r"tests\\parser\\test_parse_class.py"
        for module in core.parsed_results:
            if re.search(nonreachable_filename, module["sourcefile"]):
                unreachable_file_was_reached = True
            if re.search(reachable_filename, module["sourcefile"]):
                reachable_filename_was_reached = True

        self.assertTrue(reachable_filename_was_reached)
        self.assertFalse(unreachable_file_was_reached)
