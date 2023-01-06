"""This is the core class."""

from copy import deepcopy
from enum import Enum
import importlib.util
import inspect
import json
import os
import re

from src.hooks import Hooks
from src.parser import parse_module
import src.plugins as plugins
import src.templates as templates

initial_default_settings = {
    "console_colors": True,             # Set to False to remove colored output from
    "destination": os.getcwd(),         # Absolute or relative destination file path for generated files
    "destination_overwrite": False,     # If True, will overwrite any file of the same name that already exists there
    "plugins": [],                      # Ordered list of plugin names to use. Will resolve to absolute file paths.
    "source": [],                       # A list of modules, functions, classes, or absolute/relative paths to source files.
    "source_depth": 0,                  # How many folders to traverse down. Set to 0 for no limit. Truncates to lowest integer.
    "source_exclude_pattern": [],       # A regex pattern to exclude matching subfiles during parsing
    "template": "",                     # Defaults to the Graphic Markdown template folder in the GraphicDocs source
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

        if isinstance(user_defined_config, dict):
            # If provided with a config dictionary object instead of a filepath, try to use that instead
            self.user_defined_config = user_defined_config
            self.user_defined_config_path = ""
        else:
            self.user_defined_config = None
            self.user_defined_config_path = str(user_defined_config)

        self._process_user_defined_config()
        self._register_core_hooks()
        self._load_plugins()
        self.do_action("init")
        self.template = None
        self._load_template()
        self.do_action('finished_loading_template', {'template': self.template})
        self.parsed_results = self.parse_source_targets(self.config["source"])
        self.do_action("core_loaded")
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

        def process_config(user_config_data: dict) -> None:
            """ Takes a config dictionary object and processes the values into `self.config`. These can come directly
                from a dictionary object, or can be loaded into one from a JSON file first."""

            for key in user_config_data:
                    action = "Updated existing" # A flag to describe in the console what specifically the core is doing

                    if key == "destination":
                        self.config[key] = self.validate_filepath(user_config_data[key])

                    elif key in ["console_colors", "destination_overwrite", "verbose"]:
                        self.config[key] = bool(user_config_data[key])

                    elif key in ["plugins", "source", "source_exclude_pattern"]:
                        if not isinstance(user_config_data[key], list):
                            return  # Default is empty list... leave it that way
                        processed_list = []
                        for entry in user_config_data[key]:
                            processed_list.append(str(entry))
                        self.config[key] = processed_list
                        
                    elif key == "template":
                        self.config[key] = str(user_config_data[key])

                    elif key == "source_depth": # Force to integers
                        try:
                            self.config["source_depth"] = int(user_config_data[key])
                        except:
                            self.config["source_depth"] = 0

                    else:
                        self.config[key] = user_config_data[key]
                        action = "Added new"

                    if isinstance(user_config_data[key], str):
                        data_output = f"'{self.config[key]}'"
                    else:
                        data_output = self.config[key]

                    self.console(f"{action} key '{key}' in the core configuration.")
                    self.console(f"    {FormatForConsole('New key value:', ConsoleColorCodes.PYTHON)} {data_output}")

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
            # Try to load directly from a provided config file first.
            #   If not provided, iterating over `None` raises exception
            process_config(self.user_defined_config)    
        except:
            # Try to load from a file system based config file
            try:
                with open(self.user_defined_config_path) as user_config_file:
                    user_config_data = json.loads(user_config_file.read())
                    process_config(user_config_data)
                    user_config_file.close()
            except:
                # Trying to open a config file that doesn't exist raises exceptions. Just use the default config values.
                self.console("The configuration file was invalid. Continuing with default settings...")

    def _register_core_hooks(self) -> None:
        """ Registers a series of action hooks and filters that the core class uses.
        
            These are loaded with a dummy function as priority 0 so they are the first to execute when the core fires.
            This prevents the core from throwing a "not found" message for hooks that should exist.
        """
        self.console("Registering Core hooks...")

        def core_action_hook():
            pass

        def core_filter_hook(input: any = None) -> any:
            return input

        # CORE FILTERS AND ACTIONS
        #   Plugins
        self.filters.add("read_next_plugin", core_filter_hook, 0)

        self.actions.add("plugin_not_found", core_action_hook, 0)
        self.actions.add("error_loading_plugin", core_action_hook, 0)
        self.actions.add("plugin_loaded", core_action_hook, 0)
        self.actions.add("no_plugins_listed", core_action_hook, 0)
        self.actions.add("all_plugins_loaded", core_action_hook, 0)

        #   Templates
        self.filters.add("get_template_path_from_config", core_filter_hook, 0)

        self.actions.add("error_loading_template", core_action_hook, 0)
        self.actions.add("template_not_found", core_action_hook, 0)
        self.actions.add("no_template_specified", core_action_hook, 0)
        self.actions.add("finished_loading_template", core_action_hook, 0)

        #   Parsing
        self.filters.add("next_parsing_target", core_filter_hook, 0)

        self.actions.add("no_parsing_targets_specified", core_action_hook, 0)
        self.actions.add("unable_to_load_module", core_action_hook, 0)
        self.actions.add("unable_to_parse", core_action_hook, 0)
        self.actions.add("parsed_module", core_action_hook, 0)
        self.actions.add("parsing_complete", core_action_hook, 0)

        #   Core Initialization
        self.actions.add("init", core_action_hook, 0)
        self.actions.add("core_loaded", core_action_hook, 0)

        # Building
        self.actions.add("build_with_template", core_action_hook, 0)
        self.actions.add("all_doc_generation_complete", core_action_hook, 0)
        self.actions.add("error_building_documentation", core_action_hook, 0)

        # BUILT-IN TEMPLATE HOOKS - By registering these here, other end users can tap in to these hooks through plugins.
        # templates.graphic_md.register_hooks(self) #TODO: Reserved for future implementation

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

            spec = importlib.util.spec_from_file_location(os.path.basename(input_path), input_path)
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

            # Once the plugin is resolved try to load it
            try:
                self.console(f"Successfully loaded. Running the plugin's {FormatForConsole('load()', ConsoleColorCodes.PYTHON)} method...")
                loaded_plugin.load(self)
                plugins_loaded += 1
                self.do_action('plugin_loaded', {'loaded_plugin': loaded_plugin})
            except:
                self.do_action('error_loading_plugin', {'plugin_causing_error': loaded_plugin})

        else:
            self.do_action('no_plugins_listed')
        self.do_action('all_plugins_loaded', {'attempted': plugins_attempted, "succesful": plugins_loaded})

    def _load_template(self) -> None:
        """ Loads a reference to the template from the path specified in the config file.
            
            If it can't find the template in the precedence hierarchy using the `load_python_module` function, then it
            searches in the GraphicDocs built-in template directory. If it doesn't find a valid template there, it will
            use the default Markdown template.
            @see Core.load_python_module
        """
        def verify_template_validity(template_reference: callable) -> bool:
            """ A helper function to check that the template has a `build` method.
                @param template_reference A reference to the template in memory
                @returns True if the template has the `build` method. Otherwise, runs the `error_loading_template`
                action hook and Returns False.
            """
            self.console(f"Successfully loaded. Checking for the template's {FormatForConsole('build()', ConsoleColorCodes.PYTHON)} method...")
            try:
                getattr(template_reference, "build")
                return True
            except Exception as err:
                self.do_action('error_loading_template', {'template_causing_error': template_reference, "exception": err})
                return False

        self.console("Loading template...")

        template = self.apply_filter("get_template_path_from_config", self.config["template"])
        loaded_template = None
        use_default_template = False
        if template:
            # User specified a template, try to load it
            loaded_template = self.load_python_module(template)

            # If the template wasn't found, try a last attempt at loading it from the built-in template directory
            if loaded_template is None:
                try:
                    # Attempt to load from the built in template directory
                    # Created with help from https://stackoverflow.com/a/6677505/6186333
                    self.console(f"Could not load '{template}'. Attempting to load from the GraphicDocs template directory...")
                    loaded_template = getattr(__import__(templates.__package__, fromlist=[template]), template)
                except:
                    # Template didn't exist
                    self.console(f"Template '{template}' was not found.")
                    self.do_action('template_not_found', {'not_found_template': template})
                    use_default_template = True
        else:
            # If the user did not specify a template, then default to the Markdown template in the templates directory
            self.do_action('no_template_specified')
            use_default_template = True

        # Once the template is resolved, make sure it has an appropriate build method
        if loaded_template and verify_template_validity(loaded_template):
            self.template = loaded_template
        else:
            use_default_template = True

        if use_default_template:
            self.console("Using the default Markdown template...")
            default_template = os.path.join(os.path.dirname(__file__), "templates", "graphic_md")
            loaded_template = self.load_python_module(default_template)
            if verify_template_validity(loaded_template):
                self.template = loaded_template

    def parse_source_targets(self, target_path: str) -> list[dict]:
        """ Parses source files into a list target path.
            It will search using the exclusion patterns and source folder depth limit.

            This method runs during initialization, but is designed so that it can be used again later for other
            purposes. It does not update any core instance settings directly.
            
            @param target_path A filesystem path to search and parse. Can be a file or folder.
            @returns A list of parsed dictionaries for each file in the source list.
        """

        def should_exclude(input: str, exclusion_list: list[str]) -> bool:
            """ Determines if the input should be excluded or not.
                @param input The text to check
                @param exclusion_list A series of regex patterns to evaluate
                @returns True if the input matches any of the regex patterns from the exclusion list, False otherwise
            """
            if re.search("pycache", input) or re.search(".pyc", input):
                # Guarantee that the pycache files will always get ignored. These will never be useful for parsing.
                return False
            for exclusion_pattern in exclusion_list:
                excludeRegex = re.compile(rf"{exclusion_pattern}")
                if excludeRegex.search(input):
                    return True
            return False

        formatted_source_list = []
        def traverse_folders(src: str, current_level: int) -> None:
            """ Check provided entries to handle either files or folders. Appends results to `formatted_source_list`.

                @param src An absolute or relative source path
                @param current_level Tracks the folder depth that we have progressed down so far
            """

            def add_path(src_path):
                """Check the input file against the exclusion list and add it to the formatted_source_list if good."""
                if not should_exclude(src_path, self.config["source_exclude_pattern"]):
                    formatted_source_list.append(src_path)

            if os.path.isdir(src):
                for sublevel in os.listdir(src):
                    if os.path.isdir(os.path.join(src, sublevel)):
                        # We are about to recursively parse a subfolder. If after incrementing, we find that
                        #   current_level is still less than the config source_depth (assuming it exists), then we
                        #   should continue on and parse that subfolder. Otherwise, nothing happens and we move on. 
                        current_level += 1
                        if self.config["source_depth"] and current_level < self.config["source_depth"]:
                            traverse_folders(os.path.join(src, sublevel), current_level)  # Recursively call again
                        current_level -= 1
                    add_path(os.path.join(src, sublevel))   # It's a file in the sublevel, add it
                return
            add_path(os.path.join(src)) # It's a file in the provided source list, add it

        def process_module(src_path):
            # Attempt to load the module, and raise an exception if it can't.
            src_module = self.load_python_module(src_path)
            if not src_module:
                self.do_action("unable_to_load_module", {"bad_source_target": src_path})
                raise(Exception)

            parsed_mod = parse_module(src_module)
            if not parsed_mod:
                self.do_action("unable_to_parse", {"bad_source_target": src_path})
                raise(Exception)
            return parsed_mod

        if not target_path:
            self.do_action("no_parsing_targets_specified")
            return

        self.console("Parsing source targets...")

        for src in target_path:
            traverse_folders(src, 0)

        parsed_results = []
        for target in formatted_source_list:

            if target[-3:] != ".py":
                continue    # Trying to process non-python files will cause errors

            # Check each provided source file against the exclusion criteria using regexp and core config. Skip matches.
            src_path = self.apply_filter("next_parsing_target", target)

            try:
                parsed_results.append(process_module(src_path))
                self.do_action("parsed_module")
            except:
                return

        self.do_action("parsing_complete")
        return parsed_results

    def build(self) -> None:
        """ Runs the template's build function while passing the core object to it."""
        # TODO: This is just a placeholder for now. Testing is not implemented.

        self.console(FormatForConsole("\nBuilding documentation...", ConsoleColorCodes.CONTROL))
        self.do_action("build_with_template")

        try:
            self.template.build(self)
            self.do_action("all_doc_generation_complete")
            self.console(FormatForConsole("Documentation built successfully.", ConsoleColorCodes.CONTROL))
        except:
            self.do_action("error_building_documentation")
            self.console(FormatForConsole("Documentation failed to build.", ConsoleColorCodes.CONTROL))

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

        self.actions.done.append(action_name)
        self.actions.doing["hook_name"] = None
        self.actions.doing["callback"] = None
        self.actions.doing["priority"] = None

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

        if print_input == print_output:
            self.console(f"    {FormatForConsole('Input/Output: ', ConsoleColorCodes.PYTHON)} {print_input}")
        else:
            self.console(f"    {FormatForConsole('Input: ', ConsoleColorCodes.PYTHON)} {print_input}")
            self.console(f"    {FormatForConsole('Output:', ConsoleColorCodes.PYTHON)} {print_output}")

        self.filters.done.append(filter_name)
        self.filters.doing["hook_name"] = None
        self.filters.doing["callback"] = None
        self.filters.doing["priority"] = None

        return filter_output
