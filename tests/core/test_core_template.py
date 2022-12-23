import json
import os
import shutil
import sys
import unittest
import uuid

from src.core import Core

class TestCoreTemplate(unittest.TestCase):

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

    def writeConfig(self, text: str):
        tempfile = open(self.config_file_path, "w+")
        tempfile.write(text)
        tempfile.close()


    ###############################################################
    # Load Valid Template
    ###############################################################

    def test_template_load_module_from_abs_path(self):
        """Installing a template from an absolute filepath name"""

        test_template = os.path.join(os.path.dirname(__file__), "input_files", "test_template.py")

        self.writeConfig(json.dumps(
            {"template": test_template}))

        core = Core(self.config_file_path)

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_package_from_abs_path(self):
        """Loading a template from an absolute filepath name"""

        test_template = os.path.join(os.path.dirname(__file__), "input_files", "test_template_package")

        self.writeConfig(json.dumps(
            {"template": test_template}))

        core = Core(self.config_file_path)

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)
        
    def test_template_load_from_sys_path(self):
        """ Installing a template from pip should be findable by loading through system path.

            e.g. `pip install my_template`, then in the template key: `"template": "my_template"`
        """

        test_template = os.path.join(os.path.dirname(__file__), "input_files")

        self.writeConfig(json.dumps(
            {"template": "test_template_package"}))

        # Simulate that the module was installed using pip, or the system path was manually added
        sys.path.append(test_template)

        core = Core(self.config_file_path)

        sys.path.pop()  # Cleanup by removing the path we just added

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_module_from_working_directory(self):
        """Try to load the template from the working directory"""

        temp_template_name = str(uuid.uuid1()) + ".py"
        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template.py")
        temp_template_path = os.path.join(os.getcwd(), temp_template_name)
        shutil.copy(test_template_path, temp_template_path)

        self.writeConfig(json.dumps(
            {"template": temp_template_name}))

        core = Core(self.config_file_path)

        os.remove(temp_template_path) # Cleanup

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_module_from_working_directory_with_relative_path_below(self):
        """Try to load the template from the working directory using a relative path below the working directory"""

        temp_template_name = str(uuid.uuid1()) + ".py"
        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template.py")
        temp_relative_path_name = str(uuid.uuid1())
        temp_template_path = os.path.join(os.getcwd(), temp_relative_path_name, temp_template_name)
        os.mkdir(os.path.join(os.getcwd(), temp_relative_path_name))
        shutil.copy(test_template_path, temp_template_path)

        self.writeConfig(json.dumps(
            {"template": os.path.join(temp_relative_path_name, temp_template_name)}))

        core = Core(self.config_file_path)

        shutil.rmtree(os.path.join(os.getcwd(), temp_relative_path_name)) # Cleanup

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_module_from_working_directory_with_relative_path_above(self):
        """Try to load the template from the working directory using a relative path above the working directory"""

        temp_template_name = str(uuid.uuid1()) + ".py"
        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template.py")
        temp_template_path = os.path.join(os.path.dirname(os.getcwd()), temp_template_name)
        shutil.copy(test_template_path, temp_template_path)

        self.writeConfig(json.dumps(
            {"template": os.path.join("..", temp_template_name)}))

        core = Core(self.config_file_path)

        os.remove(temp_template_path) # Cleanup

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_package_from_working_directory(self):
        """Try to load the template package from the working directory"""

        temp_template_name = str(uuid.uuid1())
        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template_package")
        temp_template_path = os.path.join(os.getcwd(), temp_template_name)
        shutil.copytree(test_template_path, temp_template_path)

        self.writeConfig(json.dumps(
            {"template": temp_template_name}))

        core = Core(self.config_file_path)

        shutil.rmtree(temp_template_path) # Cleanup

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_package_from_working_directory_with_relative_path_below(self):
        """Try to load the template package from the working dir using a relative path below the working directory"""

        temp_template_name = str(uuid.uuid1())
        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template_package")
        temp_template_path = os.path.join(os.getcwd(), temp_template_name, temp_template_name)
        shutil.copytree(test_template_path, temp_template_path)

        self.writeConfig(json.dumps(
            {"template": os.path.join(".", temp_template_name, temp_template_name)}))

        core = Core(self.config_file_path)

        shutil.rmtree(temp_template_path) # Cleanup all but top level directory
        shutil.rmtree(os.path.dirname(temp_template_path)) # Cleanup top level directory
    
        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_package_from_working_directory_with_relative_path_above(self):
        """Try to load the template package from the working dir using a relative path above the working directory"""

        temp_template_name = str(uuid.uuid1())
        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template_package")
        temp_template_path = os.path.join(os.path.dirname(os.getcwd()), temp_template_name)
        shutil.copytree(test_template_path, temp_template_path)

        self.writeConfig(json.dumps(
            {"template": os.path.join("..", temp_template_name)}))

        core = Core(self.config_file_path)

        shutil.rmtree(temp_template_path) # Cleanup
        try:
            shutil.rmtree(os.path.join(os.path.dirname(os.getcwd()), "__pycache__")) # Remove created pycache folder
        except:
            pass

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_from_config_directory_as_module(self):
        """If not found in the working directory, try loading a module from the place the config file was."""
        temp_template_name = str(uuid.uuid1()) + ".py"

        self.writeConfig(json.dumps(
            {"template": temp_template_name}))

        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template.py")
        temp_template_path = os.path.join(os.path.dirname(self.config_file_path), temp_template_name)
        shutil.copy(test_template_path, temp_template_path)

        core = Core(self.config_file_path)

        os.remove(temp_template_path) # Cleanup

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_load_from_config_directory_as_package(self):
        """If not found in the working directory, try loading a package from the place the config file was."""
        temp_template_name = str(uuid.uuid1())

        self.writeConfig(json.dumps(
            {"template": temp_template_name}))

        test_template_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_template_package")
        temp_template_path = os.path.join(os.path.dirname(self.config_file_path), temp_template_name)
        shutil.copytree(test_template_path, temp_template_path)

        core = Core(self.config_file_path)

        shutil.rmtree(temp_template_path) # Cleanup

        self.assertEqual("Test", core.template.test_value) # If loaded successfully, this value will be accessible
        self.assertTrue('error_loading_template' not in core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_loads_from_builtin_directory_explicit(self):
        """Make sure that the default Markdown template in the built in directory will load if explicitly requested"""

        self.writeConfig(json.dumps(
            {"template": "graphic_md"}))

        core = Core(self.config_file_path)

        self.assertTrue('error_loading_template' not in  core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_loads_from_builtin_directory_by_default(self):
        """Make sure that the default Markdown template in the built in directory will load if nothing is specified"""

        self.writeConfig("")

        core = Core(self.config_file_path)

        self.assertTrue('error_loading_template' not in  core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)


    ###############################################################
    # Invalid Templates Do Not Cause Errors
    ###############################################################

    def test_template_loads_from_builtin_directory_if_not_found(self):
        """Make sure that the default Markdown template in the built in directory will load if not otherwise found"""

        self.writeConfig(json.dumps(
            {"template": "some_random_template_that_does_not_exist"}))

        core = Core(self.config_file_path)

        self.assertTrue('error_loading_template' not in  core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)

    def test_template_that_have_no_build_function_loads_default_template(self):
        """Make sure that the core loads the default Markdown template if the specified one has no `build` function"""

        test_template = os.path.join(os.path.dirname(__file__), "input_files", "bad_test_template.py")

        self.writeConfig(json.dumps(
            {"template": test_template}))

        core = Core(self.config_file_path)

        self.assertTrue('error_loading_template' in  core.actions.done) # Check the appropriate hooks fired
        self.assertTrue('template_not_found' not in core.actions.done)
        self.assertTrue('no_template_specified' not in core.actions.done)
        self.assertTrue('get_template_path_from_config' in core.filters.done)
        self.assertTrue('finished_loading_template' in core.actions.done)
        self.assertTrue('core_loaded' in core.actions.done)
