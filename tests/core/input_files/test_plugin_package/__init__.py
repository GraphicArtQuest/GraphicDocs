from tests.core.input_files.test_plugin_package.some_file import another_value

def load(core=None):
    """ The method that gets called by the Core() class when loading this plugin. It should always have a reference
    to the core object that is calling it. This particular plugin is presented as a package instead of a module."""

    core.config["SomeTestKey"] = True
    core.config["SomeTestKey2"] = another_value
