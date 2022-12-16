def load(core=None):
    """ The method that gets called by the Core() class when loading this plugin. It should always have a reference
    to the core object that is calling it."""

    core.config["SomeTestKey"] = True
