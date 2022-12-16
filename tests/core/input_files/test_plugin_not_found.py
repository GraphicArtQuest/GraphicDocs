def load(core=None):
    """ Used while verifying that the plugin_not_found action fires"""

    core.config["plugin_not_found_key"] = True
