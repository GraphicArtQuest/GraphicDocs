"""This is the core class."""

from copy import deepcopy
import inspect
import json
import os
import re
import typing

initial_default_settings = {
    "destination": os.getcwd(),         # Absolute or relative destination file path for generated files
    "destination_overwrite": False,     # If True, will overwrite any file of the same name that already exists there
    "plugins": [],                      # Ordered list of plugin names to use. Will resolve to absolute file paths.
    "source": [],                       # A list of modules, functions, classes, or absolute/relative paths to source files.
    "source_exclude_pattern": [],       # A regex pattern to exclude matching subfiles during parsing
    "template": os.path.join(os.getcwd(), "graphic_md"),  # Defaults to the Graphic Markdown template folder in the GraphicDocs source
    "verbose": False                    # If True, will output console status messages
}

class HookException(Exception):
    """ Error to raise in the event a hook issue cannot be adequately resolved."""
    def __init__(self, message):
        super().__init__(message)

class Core():
    def __init__(self, user_defined_config: str=""):
        """Initial class load

        @param user_defined_config An absolute or relative path to a configuration file. If this file path is invalid
            or does not exist, it will cause no errors. Default configs will load.
        """

        self.actions = Hooks()
        self.config = deepcopy(initial_default_settings)
        self.filters = Hooks()
        self.user_defined_config_path = str(user_defined_config)
        self._process_user_defined_config()
    
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

        if not self.user_defined_config_path:
            # Nothing specified on initiation, check the working directory for the default config file name
            default_config_path = os.path.join(os.getcwd(), "graphicdocs.config")
            if os.path.exists(default_config_path):
                # Found a config file in the working directory, use that
                self.user_defined_config_path = default_config_path
            else:
                # There is no user defined config. Will use defaults. Do not try to proceed further.
                return

        # PROCESS CONFIG SETTINGS
        try:
            with open(self.user_defined_config_path) as user_config_file:
                user_config_data = json.loads(user_config_file.read())
                for key in user_config_data:

                    if key == "destination":
                        self.config[key] = self.validate_filepath(user_config_data[key])

                    elif key in ["destination_overwrite", "verbose"]:
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

                user_config_file.close()
        except:
            # Trying to open a config file that doesn't exist will throw an error. Just use the default config values.
            pass

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
                print(f"Action hook '{action_name}' not found.")
            return

        for priority in sorted(self.actions._registered[action_name]):
            # Actions must be carried out in priority order. Cannot rely on a dict structure to self-sort.
            for action in self.actions._registered[action_name][priority]:
                # Within the priority level though, actions should carry out in the order added.
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
                print(f"Filter hook '{filter_name}' not found.")
            return

        for priority in sorted(self.filters._registered[filter_name]):
            for filter in self.filters._registered[filter_name][priority]:
                # Apply filters to the input in sequential order until all have been applied
                filter_input = filter(filter_input)

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
