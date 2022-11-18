import inspect

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
        "private": parse_docstring_functions.get_private(docstring), # If False, this implicitly makes this a public module
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
            
            `{
                "name",
                "docstring",
                "arguments",
                "returns"
            }`
    """
    if not inspect.isfunction(function_ref):
        return
    
    parsed_docstring = parse_docstring(function_ref.__doc__)
    if function_ref.__name__[0] == "_": # Beginning a function name with an underscore indicates it should be private
        parsed_docstring["private"] = True

    func_args = []

    # ARGUMENTS
    for arg in inspect.signature(function_ref).parameters:
        
        try:
            # If the argument type is specified, it will be found here
            arg_type = inspect.signature(function_ref).parameters[arg].annotation
            if arg_type == inspect._empty:
                arg_type = None

            arg_default = inspect.signature(function_ref).parameters[arg].default
            if arg_default == inspect._empty:
                arg_default = None
            
            arg_required = inspect.signature(function_ref).parameters[arg].default
            if arg_required == inspect._empty:
                arg_required = True
            else:
                arg_required = False
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

    return {
        "name": function_ref.__name__,
        "docstring": parsed_docstring,
        "arguments": func_args, # In order in which they appear in the function
        "returns": func_returns
    }
