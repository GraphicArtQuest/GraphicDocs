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

                    if isinstance(user_config_data[key], str):
                        formated_data_output = f"'{self.config[key]}'"
                    else:
                        formated_data_output = self.config[key]

                    self.console(f"{action} key '{key}' in the core configuration.")
                    self.console(f"    {FormatForConsole('New key value:', ConsoleColorCodes.PYTHON)} {formated_data_output}")

                user_config_file.close()
        except:
            # Trying to open a config file that doesn't exist will throw an error. Just use the default config values.
            self.console("The configuration file was invalid. Continuing with default settings...")

    def _register_core_hooks(self) -> None:
        """ Registers a series of action hooks and filters that the core class uses.
        
            These are loaded with a dummy function as priority 0 so they are the first to execute when the core fires.
            This prevents the core from throwing a "not found" message for hooks that should exist.
        """
        self.console("Registering core hooks...")

        def core_action_hook():
            pass

        def core_filter_hook(input: any = None) -> any:
            return input

        self.actions.add("plugin_not_found", core_action_hook, 0)
        self.actions.add("error_loading_plugin", core_action_hook, 0)
        self.actions.add("plugin_loaded", core_action_hook, 0)
        self.actions.add("no_plugins_listed", core_action_hook, 0)
        self.actions.add("all_plugins_loaded", core_action_hook, 0)
        self.actions.add("init", core_action_hook, 0)

        self.filters.add("read_next_plugin", core_filter_hook, 0)

    def load_python_module(self, path_to_module: str) -> callable:
        """ Loads a python module into memory. If not provided an absolute file path, it will traverse through a
            series of possible directories to try to resolve it using the following priorities:

            1. In or relative to the working directory where the main script was run from
            2. The config file directory
            3. The system path (e.g. you build and install callable modules as packages using PIP)

            @param path_to_module An absolute or relative path to the module
            @returns A loaded reference to the module
        """

        loaded_module = None

        def load_by_spec(input_path: str) -> None:
            """ Helper function that tries to load a python module from spec based on the file location.
                @param input_path An absolute or relative path to the module
            """

            nonlocal loaded_module
            if os.path.isdir(input_path):
                # Convert a package path into the module that initializes it
                input_path = os.path.join(input_path, "__init__.py")
            elif os.path.exists(f"{input_path}.py"):
                # Allow providing plugin modules without the .py extension
                input_path = input_path + ".py"

            spec = importlib.util.spec_from_file_location("the_plugin", input_path)
            loaded_file = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(loaded_file)
            return loaded_file

        try:
            # Attempt to load from absolute path. If not an absolute path, it will try to load from a relative path
            #   to the current working directory using the "./" or "../" indicators.
            self.console(f"Attempting to load '{path_to_module}' from absolute path...")
            loaded_module = load_by_spec(path_to_module)
        except:
            try:
                # Attempts to load from working directory.
                formatted_path = os.path.join(os.getcwd(), path_to_module)
                self.console(f"Could not load '{path_to_module}'. Attempting to load from working directory...")
                loaded_module = load_by_spec(formatted_path)
            except:
                try:
                    # Attempt to load from the config file directory
                    formatted_path = os.path.join(os.path.dirname(self.user_defined_config_path), path_to_module)
                    self.console(f"Could not load '{path_to_module}'. Attempting to load from the config file's directory...")
                    loaded_module = load_by_spec(formatted_path)
                except:
                    try:
                        # Attempts to load from the system path.
                        self.console(f"Could not load '{path_to_module}'. Attempting to load from the system path...")
                        loaded_module = __import__(path_to_module)
                    except:
                        pass
        return loaded_module

    def _load_plugins(self) -> None:
        """ Loads all plugins from the config file. 
            
            This is the first location while initializing where actions/filters get executed because this is the first
            location a user can tap in their code to access them.
            
            If it can't find the plugin in the precedence hierarchy using the `load_python_module` function, then it
            searches in the GraphicDocs built-in plugin directory.
            @see Core.load_python_module
        """
        self.console("Loading plugins...")

        plugins_attempted = 0
        plugins_loaded = 0
        for plugin in self.config["plugins"]:
            plugins_attempted += 1
            plugin = self.apply_filter("read_next_plugin", plugin)
            loaded_plugin = self.load_python_module(plugin)

            # If the plugin wasn't found, try a last attempt at loading it from the built-in plugins directory
            if loaded_plugin is None:
                try:
                    # Attempt to load from the built in plugins directory
                    # Created with help from https://stackoverflow.com/a/6677505/6186333
                    self.console(f"Could not load '{plugin}'. Attempting to load from the GraphicDocs plugin directory...")
                    loaded_plugin = getattr(__import__(plugins.__package__, fromlist=[plugin]), plugin)
                except:
                    # Plugin didn't exist
                    self.console(f"Plugin '{plugin}' was not found.")
                    self.do_action('plugin_not_found', {'not_found_plugin': plugin})
                    break

            # Once the plugin was resolved try to load it
            try:
                self.console(f"Successfully loaded. Running the plugin's {FormatForConsole('load()', ConsoleColorCodes.PYTHON)} method...")
                loaded_plugin.load(self)
                plugins_loaded += 1
                self.do_action('plugin_loaded', {'loaded_plugin': plugin})
            except:
                self.do_action('error_loading_plugin', {'plugin_causing_error': plugin})

        else:
            self.do_action('no_plugins_listed')
        self.do_action('all_plugins_loaded', {'attempted': plugins_attempted, "succesful": plugins_loaded})

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
        if args:
            self.console(f"    {FormatForConsole('Hook Arguments:', ConsoleColorCodes.PYTHON)} {args}.")

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
        filter_output = deepcopy(filter_input)
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
                    filter_output = filter(filter_output)

        self.console(f"Applying filter {FormatForConsole(filter_name, ConsoleColorCodes.FILTER)}.")

        print_input = deepcopy(filter_input)
        print_output = deepcopy(filter_output)

        if isinstance(filter_input, str):
            print_input = f"'{print_input}'"
        if isinstance(filter_output, str):
            print_output = f"'{print_output}'"

        self.console(f"    {FormatForConsole('Input: ', ConsoleColorCodes.PYTHON)} {print_input}")
        self.console(f"    {FormatForConsole('Output:', ConsoleColorCodes.PYTHON)} {print_output}")
        return filter_output

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
