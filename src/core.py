"""This is the core class."""

from copy import deepcopy
import json
import os
import re

initial_default_settings = {
    "destination": os.getcwd(),         # Absolute or relative destination file path for generated files
    "destination_overwrite": False,     # If True, will overwrite any file of the same name that already exists there
    "plugins": [],                      # Ordered list of plugin names to use. Will resolve to absolute file paths.
    "source": [],                       # A list of modules, functions, classes, or absolute/relative paths to source files.
    "source_exclude_pattern": [],       # A regex pattern to exclude matching subfiles during parsing
    "template": os.path.join(os.getcwd(), "graphic_md"),  # Defaults to the Graphic Markdown template folder in the GraphicDocs source
    "verbose": False                    # If True, will output console status messages
}


class Core():
    def __init__(self, user_defined_config: str=""):
        """Initial class load

        @param user_defined_config An absolute or relative path to a configuration file. If this file path is invalid
            or does not exist, it will cause no errors. Default configs will load.
        """

        self.config = deepcopy(initial_default_settings)
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
            
            @example Path Resolution
            # Working directory is in 'C:\\users\\GAQ\\Working'
            self.validate_filepath("C:\\users\\GAQ\\Working\\output")
            # C:\\users\\GAQ\\Working\\output
            self.validate_filepath(".\\output")
            # C:\\users\\GAQ\\Working\\output
            self.validate_filepath("..\\..\\output")
            # C:\\users\\output
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