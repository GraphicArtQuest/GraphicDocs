import inspect
import os

import src.parse_docstring_functions as parse_docstring_functions

def parse_docstring(docstring: str) -> dict:
    """
        Parses a docstring and returns a dict of the string formatted into component parts.
        
        The description must be at the top. Everything before the first tag gets treated as description.

        The parser treats consecutive lines as part of a single paragraph. To make a new paragraph, add an additional
        blank line to separate it from the previous one.

        You can use ordered lists by putting them on their own line using either a "-" or "<ul>" character.
        Omitting the space after the '-' character will not treat it as an unordered list.

        Ordered lists can be created with the "<ol>" character before it.

        Available Tags:

        - @author
        - @copyright
        - @deprecated
        - @example
        - @global
        - @ignore
        - @license
        - @memberof
        - @namespace
        - @param
        - @private
        - @public
        - @returns
        - @since
        - @throws
        - @todo
        - @version
    """

    # Guard clause
    if not isinstance(docstring, str):
        return

    return {
        "description": parse_docstring_functions.get_description(docstring),

        # Tags (Alphabetical Order)
        "author": parse_docstring_functions.get_authors(docstring),
        "copyright": parse_docstring_functions.get_copyright(docstring),
        "deprecated": parse_docstring_functions.get_deprecated(docstring),
        "examples": parse_docstring_functions.get_examples(docstring),
        "global": parse_docstring_functions.get_global(docstring),
        "ignore": parse_docstring_functions.get_ignore(docstring),
        "license": parse_docstring_functions.get_license(docstring),
        "memberof": parse_docstring_functions.get_memberof(docstring),
        "namespaces": parse_docstring_functions.get_namespaces(docstring),
        "parameters": parse_docstring_functions.get_parameters(docstring),
        "private": parse_docstring_functions.get_private(docstring), # If False, implicitly makes this a public module
        "returns": parse_docstring_functions.get_returns(docstring),
        "since": parse_docstring_functions.get_since(docstring),
        "throws": parse_docstring_functions.get_throws(docstring),
        "todo": parse_docstring_functions.get_todo(docstring),
        "version": parse_docstring_functions.get_version(docstring)
    }

def parse_function(function_ref: object) -> dict:
    """
        Inpsect a function and return a dictionary of documentation values.

        @returns If not passed a function, returns `None`. Otherwise, it returns a dictionary of documentation values
            for that function:
                
        {
            arguments: List of dictionaries as [default: `any`, name: `str`, required: bool, type: any] (or `None`),
            docstring: Parsed docstring object (or `None`)
            lineno: Lines in the source code where this occers: tuple(startingline: int, endingline: int)
            name: String of the function name
            returns: Whatever the return value type is
            sourcefile: A string filepath for where this sourcefile is located
        }
    """
    if not inspect.isfunction(function_ref):
        return
    
    parsed_docstring = parse_docstring(function_ref.__doc__)
    if function_ref.__name__[0] == "_":
        # Starting the function name with an underscore indicates it is private.
        if parsed_docstring is not None:
            parsed_docstring["private"] = True
        else:
            # If there was no docstring provided, we need to make our own docstring
            parsed_docstring = parse_docstring("@private")

    func_args = []

    # ARGUMENTS
    for arg in inspect.signature(function_ref).parameters:

        try:
            # If the argument type is specified, it will be found here
            class_arguments = inspect.signature(function_ref).parameters[arg]
            arg_type = class_arguments.annotation
            if arg_type == inspect._empty:
                arg_type = None

            arg_required = False
            arg_default = class_arguments.default
            if arg_default == inspect._empty:
                arg_required = True
                arg_default = None

        except:
            arg_type = None
            arg_default = None

        func_args.append({"name": arg, "type": arg_type, "required": arg_required, "default": arg_default})
    if len(func_args) == 0:
        func_args = None

    # RETURNS
    try:
        # If no return value explicitly defined, trying to access this way will throw an error
        func_returns = function_ref.__annotations__['return']
    except:
        func_returns = None

    # LINE NUMBERS
    linestart = inspect.findsource(function_ref)[1] + 1, # This is zero indexed, but we read line numbers starting at 1
    num_code_lines = inspect.getsource(function_ref).count("\n")  # total number of code as separated by a new line

    return {
        "arguments": func_args, # In order in which they appear in the function
        "docstring": parsed_docstring,
        "lineno": (linestart[0], linestart[0] + num_code_lines - 1), # Tuple of (linestart: int, lineend: int)
        "name": function_ref.__name__,
        "returns": func_returns,
        "sourcefile": inspect.getsourcefile(function_ref),
    }

def parse_class(class_ref) -> dict:
    """
        Inspect a class and return a dictionary of documentation values.

        @returns a dictionary of documentation values:
        {
            annotations: List of tuples as (name: `str`, type: `object`) (or `None`),
            arguments: Excluding `self`, list of dictionaries as [default: `any`, name: `str`, required: bool, type: any] (or `None`),
            docstring: Parsed docstring object (or `None`)
            methods: List of parsed functions (or `None`)
            name: String of the function name
            parent: Name of the parent class this class inherited from (or `None`)
            properties: List of dictionaries for all class properties as [docstring: `dict`, name: `str`, readable: `bool`, writeable: `bool`]
        }
    """
    if not inspect.isclass(class_ref):
        return

    # DOCSTRING
    class_docstring = parse_docstring(class_ref.__doc__)
    if class_ref.__name__[0] == "_":
        # Starting the class name with an underscore indicates it is private.
        if class_docstring is not None:
            class_docstring["private"] = True
        else:
            # If there was no docstring provided, we need to make our own docstring
            class_docstring = parse_docstring("@private")

    # CLASS ARGUMENTS
    class_arguments = inspect.getfullargspec(class_ref).args # This will always return an array from args in __init__
    args_list = []  # A working list to hold the formatted dictionary objects from each argument
    
    if len(class_arguments) > 0:
        for i in range(1, len(class_arguments)):
            # Start at 1 instead of 0. First argument is ALWAYS a reference to "self", even if named something else.
            #   As far as generated documentation purposes go, this has little value to the end user. Discard it.
            arg_name = class_arguments[i]
            class_parameters = inspect.signature(class_ref.__init__).parameters[arg_name]

            arg_type = class_parameters.annotation
            if arg_type == inspect._empty:
                arg_type = any

            arg_required = False
            arg_default = class_parameters.default
            if arg_default == inspect._empty:   # If no default was found, then this is one of the required params
                arg_required = True
                arg_default = None

            args_list.append({"name": arg_name, "type": arg_type, "required": arg_required, "default": arg_default})
    if len(args_list) == 0:
        args_list = None

    # CLASS PROPERTIES AND METHODS
    class_properties = {}
    class_methods = {}
    class_subclasses = {}

    for item in class_ref.__dict__.keys():

        if item[0:2] == "__":
            # Eliminate built in Python properties and functions (double __) and go on to the next one
            continue

        attribute = getattr(class_ref, item)

        if inspect.isdatadescriptor(attribute): # i.e. Properties
            class_properties[item] = {
                "docstring": parse_docstring(attribute.__doc__), 
                "readable": inspect.isfunction(attribute.fget), 
                "writable": inspect.isfunction(attribute.fset)
            }

        if inspect.isfunction(attribute):
            parsed_function = parse_function(attribute)
            # if parsed_function["arguments"] is not None:
            if parsed_function["arguments"] == None:
                # There was no self argument provided. This is likely a static method.
                class_methods[parsed_function["name"]] = parsed_function
                continue

            # Remove the existing first argument, which is always a reference to self in class functions
            del parsed_function["arguments"][0]    

            if len(parsed_function["arguments"]) == 0:
                parsed_function["arguments"] = None

            class_methods[parsed_function["name"]] = parsed_function
        
        if inspect.isclass(attribute):
            subclass = parse_class(attribute)
            class_subclasses[subclass["name"]] = subclass # Recursively parse this subclass using this parsing func

    if len(class_properties) == 0:
        class_properties = None
    if len(class_methods) == 0:
        class_methods = None
    if len(class_subclasses) == 0:
        class_subclasses = None

    # CLASS ANNOTATIONS
    class_annotations = {}
    for key in class_ref.__annotations__.keys():
        class_annotations[key] = class_ref.__annotations__[key]

    if len(class_annotations) == 0:
        class_annotations = None

    # PARENT CLASS
    parent_tuple = inspect.getmro(class_ref)
    if len(parent_tuple) == 2:
        # If there was no inherited class, this tuple only has two values.
        parent_class = None
    else:
        # If there IS an inherited class, the tuple has three values, the second index of which is the parent
        parent_class = inspect.getmro(class_ref)[1].__name__

    # LINE NUMBERS
    linestart = inspect.findsource(class_ref)[1] + 1, # This is zero indexed, but we read line numbers starting at 1
    num_code_lines = inspect.getsource(class_ref).count("\n")  # total number of code as separated by a new line

    return {
        "annotations": class_annotations,
        "arguments": args_list,
        "docstring": class_docstring,
        "lineno": (linestart[0], linestart[0] + num_code_lines - 1), # Tuple of (linestart: int, lineend: int)
        "methods": class_methods,
        "name": class_ref.__name__,
        "parent": parent_class,
        "properties": class_properties,
        "sourcefile": inspect.getsourcefile(class_ref),
        "subclasses": class_subclasses
        }

def parse_module(module_ref) -> dict:
    """
        This function parses Python module files (i.e. `*.py`).

        Functions and classes will always show up in alphabetical order, NOT the order they appear in the file.
    """

    if not inspect.ismodule(module_ref):
        return
    
    # CLASSES
    class_list = {}
    imported_classes = []
    for class_ref in inspect.getmembers(module_ref, inspect.isclass):
        # Check if the class module is the same as the module name we're parsing. Without this check, the parser would
        #   get all of the imported functions as well, which is unexpected behavior.
        if class_ref[1].__module__ == module_ref.__name__:
            class_list[class_ref[1].__name__] = (parse_class(class_ref[1]))
        else:
            imported_classes.append((class_ref[1].__module__, class_ref[1].__name__))
    if len(class_list) == 0:
        class_list = None
    if len(imported_classes) == 0:
        imported_classes = None

    # FUNCTIONS
    functions_list = {}
    imported_functions = []
    for function_name in inspect.getmembers(module_ref, inspect.isfunction):
        if function_name[1].__module__ == module_ref.__name__:
            # Check if the function module (from the second index of the tuple returned by inspect.getmembers) is the
            #   same as the module name we're parsing. Without this check, the parser would get all of the imported
            #   functions as well, which is unexpected behavior.
            functions_list[function_name[1].__name__] = parse_function(function_name[1])
        else:
            # Return a tuple of the function's module and the function's name
            imported_functions.append((function_name[1].__module__, function_name[1].__name__))
    if len(functions_list) == 0:
        functions_list = None
    if len(imported_functions) == 0:
        imported_functions = None
    
    # MODULES
    imported_modules = []

    for module in inspect.getmembers(module_ref, inspect.ismodule):
        imported_modules.append(module[0])
            # NOTE: Only does the highest level. For example, if imported "tests.input_files.testmodule_only_docstring",
            #   then it will return "tests".
    if len(imported_modules) == 0:
        imported_modules = None

    return {
        "classes": class_list,
        "functions": functions_list,
        "imported": {
            "classes": imported_classes,
            "functions": imported_functions,
            "modules": imported_modules
        },
        "name": module_ref.__name__,
        "sourcefile": os.path.abspath(module_ref.__file__)
    }
