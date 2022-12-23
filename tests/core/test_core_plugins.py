import json
import os
import shutil
import sys
import unittest
import uuid

from src.core import Core

class TestCorePlugins(unittest.TestCase):

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
    # Load Valid Plugins
    ###############################################################

    def test_plugins_load_module_from_abs_path(self):
        """Installing a plugin from an absolute filepath name"""

        self.writeConfig(json.dumps(
            {"plugins": [os.path.join(os.path.dirname(__file__), "input_files", "test_plugin.py")]}))

        core = Core(self.config_file_path)

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_package_from_abs_path(self):
        """Installing a plugin from an absolute filepath name"""

        self.writeConfig(json.dumps(
            {"plugins": [os.path.join(os.path.dirname(__file__), "input_files", "test_plugin_package")]}))

        core = Core(self.config_file_path)

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config
        self.assertEqual(12345, core.config["SomeTestKey2"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_from_sys_path(self):
        """ Installing a plugin from pip should be findable by loading through system path.

            e.g. `pip install my_plugin`, then in the plugin list: `"plugins": ["my_plugin"]`
        """

        self.writeConfig(json.dumps({"plugins": ["test_plugin"]}))

        # Simulate that the module was installed using pip, or the system path was manually added
        sys.path.append(os.path.join(os.path.dirname(__file__), "input_files"))

        core = Core(self.config_file_path)

        sys.path.pop()  # Cleanup by removing the path we just added

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_module_from_working_directory(self):
        """Try to load the plugin from the working directory"""

        tempplugin_name = str(uuid.uuid1()) + ".py"
        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin.py")
        temp_plugin_path = os.path.join(os.getcwd(), tempplugin_name)
        shutil.copy(test_plugin_path, temp_plugin_path)

        self.writeConfig(json.dumps({"plugins": [os.path.join(tempplugin_name)]}))

        core = Core(self.config_file_path)

        os.remove(temp_plugin_path) # Cleanup

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_module_from_working_directory_with_relative_path_below(self):
        """Try to load the plugin from the working directory using a relative path below the working directory"""

        tempplugin_name = str(uuid.uuid1()) + ".py"
        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin.py")
        temp_relative_path_name = str(uuid.uuid1())
        temp_plugin_path = os.path.join(os.getcwd(), temp_relative_path_name, tempplugin_name)
        os.mkdir(os.path.join(os.getcwd(), temp_relative_path_name))
        shutil.copy(test_plugin_path, temp_plugin_path)

        self.writeConfig(json.dumps({"plugins": [os.path.join(temp_relative_path_name, tempplugin_name)]}))

        core = Core(self.config_file_path)

        shutil.rmtree(os.path.join(os.getcwd(), temp_relative_path_name)) # Cleanup

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_module_from_working_directory_with_relative_path_above(self):
        """Try to load the plugin from the working directory using a relative path above the working directory"""

        tempplugin_name = str(uuid.uuid1()) + ".py"
        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin.py")
        temp_plugin_path = os.path.join(os.path.dirname(os.getcwd()), tempplugin_name)
        shutil.copy(test_plugin_path, temp_plugin_path)

        self.writeConfig(json.dumps({"plugins": [os.path.join("..", tempplugin_name)]}))

        core = Core(self.config_file_path)
        os.remove(temp_plugin_path) # Cleanup

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_package_from_working_directory(self):
        """Try to load the plugin package from the working directory"""

        tempplugin_name = str(uuid.uuid1())
        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin_package")
        temp_plugin_path = os.path.join(os.getcwd(), tempplugin_name)
        shutil.copytree(test_plugin_path, temp_plugin_path)

        self.writeConfig(json.dumps({"plugins": [os.path.join(tempplugin_name)]}))

        core = Core(self.config_file_path)

        shutil.rmtree(temp_plugin_path) # Cleanup

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config
        self.assertEqual(12345, core.config["SomeTestKey2"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_package_from_working_directory_with_relative_path_below(self):
        """Try to load the plugin package from the working dir using a relative path below the working directory"""

        tempplugin_name = str(uuid.uuid1())
        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin_package")
        temp_plugin_path = os.path.join(os.getcwd(), tempplugin_name, tempplugin_name)
        shutil.copytree(test_plugin_path, temp_plugin_path)

        self.writeConfig(json.dumps({"plugins": [os.path.join(".", tempplugin_name, tempplugin_name)]}))

        core = Core(self.config_file_path)

        shutil.rmtree(temp_plugin_path) # Cleanup all but top level directory
        shutil.rmtree(os.path.dirname(temp_plugin_path)) # Cleanup top level directory

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config
        self.assertEqual(12345, core.config["SomeTestKey2"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_package_from_working_directory_with_relative_path_above(self):
        """Try to load the plugin package from the working dir using a relative path above the working directory"""

        tempplugin_name = str(uuid.uuid1())
        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin_package")
        temp_plugin_path = os.path.join(os.path.dirname(os.getcwd()), tempplugin_name)
        shutil.copytree(test_plugin_path, temp_plugin_path)

        self.writeConfig(json.dumps({"plugins": [os.path.join("..", tempplugin_name)]}))

        core = Core(self.config_file_path)

        shutil.rmtree(temp_plugin_path) # Cleanup
        shutil.rmtree(os.path.join(os.path.dirname(os.getcwd()), "__pycache__")) # Remove created pycache folder

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config
        self.assertEqual(12345, core.config["SomeTestKey2"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_from_config_directory_as_module(self):
        """If not found in the working directory, try loading a module from the place the config file was."""
        tempplugin_name = str(uuid.uuid1()) + ".py"

        self.writeConfig(json.dumps({"plugins": [tempplugin_name]}))

        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin.py")
        temp_plugin_path = os.path.join(os.path.dirname(self.config_file_path), tempplugin_name)
        shutil.copy(test_plugin_path, temp_plugin_path)

        core = Core(self.config_file_path)

        os.remove(temp_plugin_path) # Cleanup

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_from_config_directory_as_package(self):
        """If not found in the working directory, try loading a package from the place the config file was."""
        tempplugin_name = str(uuid.uuid1())

        self.writeConfig(json.dumps({"plugins": [tempplugin_name]}))

        test_plugin_path = os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin_package")
        temp_plugin_path = os.path.join(os.path.dirname(self.config_file_path), tempplugin_name)
        shutil.copytree(test_plugin_path, temp_plugin_path)

        core = Core(self.config_file_path)

        shutil.rmtree(temp_plugin_path) # Cleanup

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config
        self.assertEqual(12345, core.config["SomeTestKey2"]) # Verify the plugin added the test key to the core config

    def test_plugins_load_from_builtin_directory(self):
        """Make sure that a sample plugin in the built in directory will load if not otherwise found"""

        self.writeConfig(json.dumps({"plugins": ["graphicdocs_sample_plugin"]}))

        core = Core(self.config_file_path)

        self.assertTrue(core.config["SomeTestKey"]) # Verify the plugin added the test key to the core config


    ###############################################################
    # Invalid Plugins Do Not Cause Errors
    ###############################################################
    
    def test_plugins_that_do_not_exist_cause_no_errors(self):
        """Make sure that the core still loads but executes the 'error_loading_plugin' hook if plugin doesn't exist"""

        self.writeConfig(json.dumps({"plugins": 
            [   
                os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin_not_found"),
                "i_am_a_plugin_that_does_not_exist"
            ]}))

        core = Core(self.config_file_path)

        self.assertFalse("SomeTestKey" in core.config) # Verify the config doesn't have the plugin test key
        self.assertFalse("error_loading_plugin_key" in core.config) # Verify no load error test key
        self.assertTrue(core.config["plugin_not_found_key"]) # Verify the plugin added the correct test key

    def test_plugins_that_with_no_load_function_executes_hook_with_no_errors(self):
        """ Make sure that the core still loads but executes the 'plugin_not_found' hook if the plugin exists but
            doesn't have a 'load' method"""

        self.writeConfig(json.dumps({"plugins": 
            [   
                os.path.join(os.getcwd(), "tests", "core", "input_files", "test_plugin_load_error"),
                os.path.join(os.getcwd(), "tests", "core", "input_files", "bad_test_plugin")
            ]}))

        core = Core(self.config_file_path)

        self.assertFalse("SomeTestKey" in core.config) # Verify the config doesn't have the typical plugin test key
        self.assertFalse("plugin_not_found_key" in core.config) # Verify no plugin not found test key
        self.assertTrue(core.config["error_loading_plugin_key"]) # Verify the plugin added the correct test key
