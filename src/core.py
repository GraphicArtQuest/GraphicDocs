"""This is the core class."""

from copy import deepcopy
from enum import Enum
import importlib.util
import inspect
import json
import os
import re
import typing

import src.plugins as plugins

initial_default_settings = {
    "console_colors": True,             # Set to False to remove colored output from
    "destination": os.getcwd(),         # Absolute or relative destination file path for generated files
    "destination_overwrite": False,     # If True, will overwrite any file of the same name that already exists there
    "plugins": [],                      # Ordered list of plugin names to use. Will resolve to absolute file paths.
    "source": [],                       # A list of modules, functions, classes, or absolute/relative paths to source files.
    "source_exclude_pattern": [],       # A regex pattern to exclude matching subfiles during parsing
    "template": os.path.join(os.getcwd(), "graphic_md"),  # Defaults to the Graphic Markdown template folder in the GraphicDocs source
    "verbose": True                     # If False, will not output console status messages
}

class ConsoleColorCodes(Enum):
    """Provides standardized console colors to use as escape codes for terminal debugging.

    This Enum provides standardized terminal escape sequences that correspond to colored text when printing to the
    terminal. This allows a debugging programmer to more easily separate the output and see what is going on.

    For accessibility for the color blind, users can disable this feature and print only black and white to the console.
    """
    CONTROL = '\033[35m'        # Purple
    PYTHON = '\033[33m'         # Yellow
    ACTION = '\033[91m'         # Red
    FILTER = '\033[94m'         # Blue
    QUOTE = '\033[92m'          # Green
    ENDC = NONE = '\033[0m'     # Required end code to tell the console to stop escaping

def FormatForConsole(message: str, type: ConsoleColorCodes = ConsoleColorCodes.NONE) -> str:
    """ 
        Applies color to a message that will output in the console.

        @param message The message to apply colored escape codes to
        @returns The same message wrapped in the appropriate formatting code
    """
    return type.value + str(message) + ConsoleColorCodes.ENDC.value

class HookException(Exception):
    """ Error to raise in the event a hook issue cannot be adequately resolved."""
    def __init__(self, message):
        super().__init__(message)

class Core():
    def __init__(self, user_defined_config: str=""):
        """Initial class load

        @param user_defined_config An absolute or relative path to a configuration file. If this file path is invalid
            or does not exist, it will cause no errors. Default configs will load.
        @see The Core flowchart.
        """

        self.actions = Hooks()
        self.config = deepcopy(initial_default_settings)
        self.filters = Hooks()
        self.user_defined_config_path = str(user_defined_config)
        self._process_user_defined_config()
        self._register_core_hooks()
        self._load_plugins()
        self.do_action("init")
        self.console(FormatForConsole("GraphicDocs Core object initialized successfully.", ConsoleColorCodes.CONTROL))

    @staticmethod
    def validate_filepath(input_filepath: str) -> str:
        """ Validate a file path by returning a valid absolute file path under any circumstance.

            For settings that involve file paths, either absolute or relative relative paths are allowed.
            Use a single dot '.' for the current directory, and a double dot '..' to go up a directory.
            Absolute paths resolve as themselves.

            @param input_filepath The generated output documentation base path. Can be relative or absolute.
            @returns Valid absolute path for generated files.
            
            @example Path Resolution (Working directory is in 'C:\\users\\GAQ\\Working')

            self.validate_filepath("output")                                    # C:\\users\\GAQ\\Working\\output
            self.validate_filepath("C:\\users\\GAQ\\Working\\output")           # C:\\users\\GAQ\\Working\\output
            self.validate_filepath(".\\output")                                 # C:\\users\\GAQ\\Working\\output
            self.validate_filepath("..\\output")                                # C:\\users\\GAQ\\output
            self.validate_filepath("..\\..\\output")                            # C:\\users\\output
            self.validate_filepath(["Bad Path In List Goes To Working Dir"])    # C:\\users\\GAQ\\Working\\output
        """

        bad_filename_pattern = "[:*?\"<>|]" # None of these characters may be in a file name on Windows systems
        try:
            validated_path = os.path.abspath(str(input_filepath))
            filename = validated_path.split("\\")[-1]
            # Now, check the file name for invalid characters. 
            if re.search(bad_filename_pattern, filename):
                return os.getcwd()  # If there are invalid chars, just send back working dir
            else:
                return os.path.abspath(str(input_filepath))  # Otherwise, send the formatted absolute path
        except:
            return os.getcwd()  # Trying to use .abspath() on memory references (e.g. function) will throw error.
                                #   In that case, just send back working dir
    
    def console(self, message: str, output_to_console: bool = True) -> str:
        """ Creates pretty formatted text and logs it to the console.

            @param message The message to log to the console
            @param output_to_console If True, this message will log to the console. Otherwise, it won't. It can be
                useful to set this to false to obtain the pretty formatted error message for use elsewhere. This allows
                'verbose' to be on while not outputting this particular text to the console.
            @returns A string representation of message
            @example
            console("I am a console message.")
            console("I am a 'console' message.")    # Will automatically wrap the quoted text in a green color.
        """
        # Automatically place quoted text in its own pattern
        quote_color_pattern = r"'" + ConsoleColorCodes.QUOTE.value + "\\1" + ConsoleColorCodes.ENDC.value + "'"
        formatted_msg = re.sub(r"'([^']*)'", quote_color_pattern, message)

        if not self.config["console_colors"]:
            # Remove any color codes if this config variable is not set
            for code in ConsoleColorCodes:
                formatted_msg = formatted_msg.replace(code.value, "")

        if self.config["verbose"] and output_to_console:
            print(formatted_msg)
        
        return formatted_msg
    
    def _process_user_defined_config(self) -> None:
        """ If the user didn't provide a config, look for one in the working directory called 'graphicdocs.config'.
            If it finds one there, use that. Otherwise, it will assume the defaults.

            - `destination`: An absolute or relative path for where the generated writes to.
            - `destination_overwrite`: If True, will overwrite any file of the same name that already exists there.
                Converts truthy or falsy inputs to booleans.
            - `plugins`: A list of plugins path to use. The inputs must be strings or coercible to strings. The values
                may be either a Python module name, or an absolute or relative path to the plugin script.
                If provided anything other than a list, it will use the default empty list.
                The initialization step will not resolve paths yet, just enforce strings.
            - `source_exclude_pattern`: A list of regex patterns that will get omitted from the source inclusions.
                If provided anything other than a list, it will use the default empty list. All values inside the list
                convert to strings if not already in string format.
            - `template`: Either a Python module name, or an absolute or relative path for where the template script
                is located. The initialization step will not resolve paths yet, just enforce strings.
            - `verbose`: If True, will output console status messages. Converts truthy or falsy inputs to booleans.
        """

        self.console(FormatForConsole("Setting initial GraphicDocs configuration.", ConsoleColorCodes.CONTROL))

        if not self.user_defined_config_path:
            # Nothing specified on initiation, check the working directory for the default config file name
            default_config_path = os.path.join(os.getcwd(), "graphicdocs.config")
            if os.path.exists(default_config_path):
                # Found a config file in the working directory, use that
                self.user_defined_config_path = default_config_path
                self.console("Found configuration file 'graphicdocs.config' in the working directory. Loading...")
            else:
                # There is no user defined config. Will use defaults. Do not try to proceed further.
                self.console("No user defined configuration specified. Continuing with default settings...")
                return

        # PROCESS CONFIG SETTINGS
        try:
            with open(self.user_defined_config_path) as user_config_file:
                user_config_data = json.loads(user_config_file.read())
                for key in user_config_data:
                    action = "Updated existing"

                    if key == "destination":
                        self.config[key] = self.validate_filepath(user_config_data[key])

                    elif key in ["console_colors", "destination_overwrite", "verbose"]:
                        self.config[key] = bool(user_config_data[key])

                    elif key in ["plugins", "source", "source_exclude_pattern"]:
                        if not isinstance(user_config_data[key], list):
                            return  # Default is empty list... leave it that way
                        processed_plugins = []
                        for entry in user_config_data[key]:
                            processed_plugins.append(str(entry))
                        self.config[key] = processed_plugins
                        
                    elif key == "template":
                        self.config[key] = str(user_config_data[key])

                    else:
                        self.config[key] = user_config_data[key]
                        action = "Added new"

                    self.console(f"{action} key '{key}' in the core configuration.")

                user_config_file.close()
        except:
            # Trying to open a config file that doesn't exist will throw an error. Just use the default config values.
            self.console("No valid configuration file found. Continuing with default settings...")

    def _register_core_hooks(self) -> None:
        """ Registers a series of action hooks and filters that the core class uses.
        
            These are loaded with a dummy function as priority 0 so they are the first to execute when the core fires.
        """
        self.console("Registering core hooks...")

        def core_action_hook():
            pass

        def core_filter_hook(input: any = None) -> any:
            return input

        self.actions.add("plugin_not_found", core_action_hook, 0)
        self.actions.add("error_loading_plugin", core_action_hook, 0)
        self.actions.add("plugin_loaded", core_action_hook, 0)
        self.actions.add("all_plugins_loaded", core_action_hook, 0)
        self.actions.add("init", core_action_hook, 0)

        self.filters.add("read_next_plugin", core_filter_hook, 0)
        self.filters.add("plugin_path_before_loading", core_filter_hook, 0)

    def _load_plugins(self) -> None:
        """ Loads all plugins from the config file. If not provided an absolute file path, it will traverse through a
            series of possible directories to try to resolve it using the following priorities:

            1. The working directory where the main script was run from
            2. The config file directory
            3. The system path (e.g. you build and install plugins as packages using PIP)
            4. The GraphicDocs built-in plugin directory
            
            This is the first location while initializing where actions/filters get executed because this is the first
            location a user can tap in their code to access them.
        """
        self.console("Loading plugins...")

        def load_by_spec(input_path: str) -> None:
            """ Tries to load a plugin from spec based on the file location.
                @param input_path An absolute or relative path to the plugin 
            """
            nonlocal loaded_plugin
            input_path = self.apply_filter("plugin_path_before_loading", input_path)
            if os.path.isdir(input_path):
                # Convert a package path into the module that initializes it
                input_path = os.path.join(formatted_path, "__init__.py")
            elif os.path.exists(input_path + ".py"):
                # Allow providing plugin modules without the .py extension
                input_path = input_path + ".py"

            spec = importlib.util.spec_from_file_location("the_plugin", input_path)
            loaded_plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(loaded_plugin)
        
        for plugin in self.config["plugins"]:
            plugin = self.apply_filter("read_next_plugin", plugin)
            loaded_plugin = None
            try:
                # Attempt to load from absolute path. If not an absolute path, it will try to load from a relative path
                #   to the current working directory using the "./" or "../" indicators.
                self.console(f"Attempting to load plugin '{plugin}' from absolute path...")
                load_by_spec(plugin)
            except:
                try:
                    # Attempts to load from working directory.
                    formatted_path = os.path.join(os.getcwd(), plugin)
                    self.console(f"Could not load plugin '{plugin}'. Attempting to load from working directory...")
                    load_by_spec(formatted_path)
                except:
                    try:
                        # Attempt to load from the config file directory
                        formatted_path = os.path.join(os.path.dirname(self.user_defined_config_path), plugin)
                        self.console(f"Could not load plugin '{plugin}'. Attempting to load from the config file's directory...")
                        load_by_spec(formatted_path)
                    except:
                        try:
                            # Attempts to load from the system path.
                            self.console(f"Could not load plugin '{plugin}'. Attempting to load from the system path...")
                            plugin = self.apply_filter("plugin_path_before_loading", plugin)
                            loaded_plugin = __import__(plugin)
                        except:
                            try:
                                # Attempt to load from the built in plugins directory
                                # Created with help from https://stackoverflow.com/a/6677505/6186333
                                self.console(f"Could not load plugin '{plugin}'. Attempting to load from the GraphicDocs plugin directory...")
                                plugin = self.apply_filter("plugin_path_before_loading", plugin)
                                loaded_plugin = getattr(__import__(plugins.__package__, fromlist=[plugin]), plugin)
                            except:
                                # Plugin didn't exist
                                self.console(f"Could not load plugin '{plugin}'.")
                                self.do_action('plugin_not_found')

            # Once the plugin was resolved try to load it
            try:
                self.console(f"Successfully loaded. Running the plugin's {FormatForConsole('load()', ConsoleColorCodes.PYTHON)} method...")
                loaded_plugin.load(self)
                self.do_action('plugin_loaded')
            except:
                self.do_action('error_loading_plugin')

        self.do_action('all_plugins_loaded')
        self.console("All plugins are loaded.")

    def do_action(self, action_name: str, args: dict = {}) -> None:
        """ Executes all actions with the provided name in order of priority.
        
            @param action_name The case sensitive name of the action hook to run
            @param args An optional dictionary of arguments to pass to the callback functions
            @example
            testval = 2
            def test_func(input: int)
                nonlocal testval
                testval *= 2
            
            core = Core()
            core.filters.add("test_actions", test_func, 5)
            core.filters.add("test_actions", test_func)
            core.filters.add("test_actions", test_func, 15)
            
            core.apply_filter("test_actions", 2) # testval = 16
        """
        if action_name not in self.actions._registered:
            if self.config["verbose"]:
                self.console(f"Action hook '{action_name}' not found.")
            return

        self.console(f"Executing action hook {FormatForConsole(action_name, ConsoleColorCodes.ACTION)}.")

        for priority in sorted(self.actions._registered[action_name]):
            # Actions must be carried out in priority order. Cannot rely on a dict structure to self-sort.
            for action in self.actions._registered[action_name][priority]:
                # Within the priority level though, actions should carry out in the order added.
                self.actions.doing["hook_name"] = action_name
                self.actions.doing["callback"] = action
                self.actions.doing["priority"] = priority
                if args and inspect.getfullargspec(action).args:
                    # Trying to execute with arguments will error if the callback doesn't expect or need them.
                    action(args)
                else:
                    action()

    def apply_filter(self, filter_name: str, filter_input: any) -> any:
        """ Applies all filters with the provided name to the provided input sequentially and in order of priority.
            In most cases, the filtered response should match input format, but this is not strictly necessary.
        
            @param filter_name The case sensitive name of the filter to apply
            @param filter_input An input argument to modify
            @example
            def test_func(input: int)
                return input * 2
            
            core = Core()
            core.filters.add("test_filters", test_func, 5)
            core.filters.add("test_filters", test_func)
            core.filters.add("test_filters", test_func, 15)
            
            final_val = core.apply_filter("test_filters", 2) # Returns 16
        """

        if filter_name not in self.filters._registered:
            if self.config["verbose"]:
                self.console(f"Filter hook '{filter_name}' not found.")
        else:
            for priority in sorted(self.filters._registered[filter_name]):
                for filter in self.filters._registered[filter_name][priority]:
                    # Apply filters to the input in sequential order until all have been applied
                    self.filters.doing["hook_name"] = filter_name
                    self.filters.doing["callback"] = filter
                    self.filters.doing["priority"] = priority
                    filter_input = filter(filter_input)

        self.console(f"Applying filter {FormatForConsole(filter_name, ConsoleColorCodes.FILTER)}.")
        self.console(f"    Input:  '{filter_input}'")
        self.console(f"    Output: '{filter_input}'")
        return filter_input

class Hooks():
    def __init__(self) -> None:
        self._registered: dict[dict[list[int]]] = {}
        self.doing: dict = {"hook_name": None, "callback": None, "priority": None}
        self.done: list|None = None

    def add(self, hook_name: str, callback: typing.Callable, priority: int = 10) -> True:
        """ Register a new hook.
            @param hook_name The identifying name for the hook
            @param callback A callable function to execute when this hook fires
            @param priority The priority level within this hook name. Hooks will execute in order of priority level
                followed by the order in which they were registered within that priority. This value must be coercible
                to an integer that is greater than or equal 0.
            @throws [HookException] If priority is less than 0 or is not coercible to an integer 
            @returns True if the hook was found and removed            
            @example
            Hooks.add("my_hook_name", my_callback_function, 10) 
            Hooks.add("my_hook_name", my_callback_function, 5) 
            Hooks.add("my_hook_name", my_callback_function) # Implicitly assumes priority 10
            Hooks.add("my_hook_name", my_callback_function, 755) 
        """

        try:
            priority = round(float(priority))
        except:
            try:
                priority = int(priority)
            except:
                raise HookException("Hook priority value must be type integer or float.")

        if int(priority) < 0:
            raise HookException("Hook priority value must be an integer greater than or equal to 0.")

        args = inspect.getfullargspec(callback).args
        if len(args) > 1:
            raise HookException("Hooks may only take a single argument. Use a list/tuple/dict for more args.")

        if hook_name in self._registered:
            if priority in self._registered[hook_name]:
                self._registered[hook_name][priority].append(callback) # Hook and priority already existed
            else:
                self._registered[hook_name][priority] = [callback] # Hook priority did not exist
        else:
            self._registered[hook_name] = {priority: [callback]} # Hook didn't exist

        return True

    def remove(self, hook_name: str, callback: typing.Callable, priority: int = 10) -> bool:
        """ Remove a callback from a hook. The hook to remove must exactly match the name, callable, and priority.

            If a hook matching these conditions is not met, it will do nothing and throw no errors.

            @param hook_name The identifying name for the hook to remove
            @param callback The callable function registered under this hook
            @param priority The priority level for the hook to be removed
            @returns True if the hook was found and removed, False otherwise
            @example
            Hooks.remove("my_hook_name", my_callback_function, 10)
            Hooks.remove("my_hook_name", my_callback_function, 5)
            Hooks.remove("my_hook_name", my_callback_function) # Implicitly assumes priority 10
        """

        try:
            hook_name = str(hook_name)
            priority = int(priority)

            # Try to remove callback
            self._registered[hook_name][priority].remove(callback)

            # Try to remove priority if there are no more under this dict
            if len(self._registered[hook_name][priority]) == 0:
                del self._registered[hook_name][priority]

            # Try to remove hook if there are no more under this dict
            if len(self._registered[hook_name]) == 0:
                del self._registered[hook_name]

            return True
        except:
            return False

    def remove_all(self, hook_name: str, priority: int|None = None) -> bool:
        """ Remove all callbacks from a specified hook and optional priority.

            If no hooks matching these conditions are found, it will do nothing and throw no errors.

            @param hook_name The identifying name for the hook to remove
            @param priority The optional priority level for the hook to be removed. If omitted, this function will
                remove all callbacks in a hook name of all priorities. If included, the function will delete only those
                with that priority level.
            @returns True if the hooks were found and removed, False otherwise
            @example
            Hooks.remove_all("my_hook_name")
            Hooks.remove_all("my_hook_name", 22)
        """

        try:
            hook_name = str(hook_name)
            
            # Try to remove priority if there are no more under this dict, otherwise remove whole dict
            if priority is not None:
                priority = int(priority)
                del self._registered[hook_name][priority]
            else:
                del self._registered[hook_name]

            return True
        except:
            return False
    
    def has(self, hook_name: str, priority: int|None = None, callback: typing.Callable|None = None) -> bool:
        """ Checks if this Hooks class instance has any hook registered meeting these criteria. 

            If no hooks matching these conditions are found, it will do nothing and throw no errors.

            @param hook_name The identifying name for the hook to check for
            @param callback The callback function to check for
            @param priority The priority level for the hook to check for
            @returns True if the hooks were found and removed, False otherwise
            @example
            Hooks.has("my_hook_name")
            Hooks.has("my_hook_name", 719)
            Hooks.has("my_hook_name", 719, my_callback_function)
        """
        try:
            # If not coercible to an integer, abort early
            if priority is not None:
                priority = int(float(priority))
        except:
            return False

        if hook_name in self._registered:
            if priority is None:
                return True
            elif priority in self._registered[hook_name]:
                if callback is None:
                    return True
                else:
                    if callback in self._registered[hook_name][priority]:
                        return True
                    return False
            else:
                return False
        else:
            return False
