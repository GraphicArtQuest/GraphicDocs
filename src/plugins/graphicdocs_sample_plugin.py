""" This plugin is used for both unit testing as well as demonstrating how to build your own plugins."""

def load(core = None):
    """ This is the only method REQUIRED for a plugin. The Core class will try to run this method after finding your
        plugin, and it will pass it a copy of itself as the argument. If the Core encounters an error while trying to
        load, then it will fire the `error_loading_plugin` action hook.
        @param core A reference to the Core() class object executing this plugin."""
        
    core.config["SomeTestKey"] = True