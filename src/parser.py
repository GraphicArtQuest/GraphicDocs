import re

import src.parse_docstring_functions as parse_docstring_functions

def parse_docstring(docstring: str) -> dict:
    """
        Parses a doc string and returns a dict of the string formatted into component parts.
        
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

    parameters = []
    throws = []

    parsed = docstring.splitlines()
    
    def get_parameters() -> None:
        """Goes through the doc string and looks for parameters annotated by the @param tag"""
        parameter_name = ""
        parameter_description = ""

        def add_parameter(name:str, desc: str) -> None:
            """
                Adds the parameter and description to the parameters list.
                If the parameter was already added, it was overwrites it.
            """
            nonlocal parameter_name
            nonlocal parameter_description

            for param in parameters:
                if name in param:
                    param[name] = parameter_description.strip()
                    return

            parameters.append({name.strip(): desc.strip()})
            parameter_name = ""
            parameter_description = ""

        for line in parsed:
            stripped_line = line.strip()

            if stripped_line[0:7] == "@param ":
                if parameter_name != "":
                    # Previous parameter complete, about to start a new one
                    add_parameter(parameter_name, parameter_description)
                
                # We have encountered a new parameter, start recording the info
                end_of_param_name = re.search("[A-Za-z0-9] ", stripped_line[8:len(stripped_line)]).end()

                parameter_name = stripped_line[7:7 + end_of_param_name]
                parameter_description = stripped_line[8 + end_of_param_name:len(stripped_line)]
                continue

            if parameter_name != "" and stripped_line[0:1] == "@":  
                # Already started parsing a parameter, but now encountering a new tag
                add_parameter(parameter_name, parameter_description)
                continue

            if parameter_name != "":
                # Have found a parameter already, and now its description has spilled on to another line
                if stripped_line == "": # Add a paragraph break
                    parameter_description += "\n"
                elif parameter_description[-1:] == "\n": # Do not add an extra space for new paragraphs.
                    parameter_description += stripped_line
                else:
                    parameter_description += " " + stripped_line

        if parameter_name != "":   # Final catch for parameters not added yet
            add_parameter(parameter_name, parameter_description)
    
    def get_throws() -> None:
        """Goes through the doc string and looks for exceptions annotated by the @throws tag"""
        error_type = None
        error_description = None

        def add_throw(type:str, desc: str) -> None:
            """
                Adds the error name and description to the throws list.
                Can have multiple errors of the same type and description.
            """
            nonlocal error_type
            nonlocal error_description

            if type is not None:
                type = type.strip() # Trying to strip None causes an error. This is only needed if an error type given

            if desc is not None:
                desc = desc.strip()

            throws.append({"type": type, "description": desc})
            error_type = None
            error_description = None

        for line in parsed:
            stripped_line = line.strip()

            if stripped_line[0:8] == "@throws ":
                if error_description is not None or error_type is not None:
                    # Previous parameter complete, about to start a new one
                    add_throw(error_type, error_description)
                
                # We have encountered a new parameter, start recording the info
                if stripped_line[8:9] == "[":
                    end_of_throw_type = re.search("]", stripped_line[8:len(stripped_line)]).end()

                    error_type = stripped_line[9:7 + end_of_throw_type]
                    error_description = stripped_line[8 + end_of_throw_type:len(stripped_line)]
                    if error_description == "":
                        error_description = None
                else:
                    error_type = None
                    error_description = stripped_line[8:len(stripped_line)]
                continue

            if (error_description is not None  or error_type is not None) and stripped_line[0:1] == "@":  
                # Already started parsing a parameter, but now encountering a new tag
                add_throw(error_type, error_description)
                continue

            if error_description is not None or error_type is not None:
                # Have found a parameter already, and now its description has spilled on to another line
                if error_description is not None:
                    if stripped_line == "": # Add a paragraph break
                        error_description += "\n"
                    elif error_description[-1:] == "\n": # Do not add an extra space for new paragraphs.
                        error_description += stripped_line
                    else:
                        error_description += " " + stripped_line

        if error_description is not None or error_type is not None:   # Final catch for parameters not added yet
            add_throw(error_type, error_description)

    # Parse Tags (Alphabetical Order)
    get_parameters()
    get_throws()

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
        "parameters": parameters,
        "private": parse_docstring_functions.get_private(docstring), # If False, this implicitly makes this a public module
        "returns": parse_docstring_functions.get_returns(docstring),
        "since": parse_docstring_functions.get_since(docstring),
        "throws": throws,
        "todo": parse_docstring_functions.get_todo(docstring),
        "version": parse_docstring_functions.get_version(docstring)
    }
