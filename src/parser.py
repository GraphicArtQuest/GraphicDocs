import re

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

        - @example
        - @param
        - @private
        - @returns
        - @throws
    """

    # Guard clause
    if not isinstance(docstring, str):
        return

    description = ""

    examples = []
    parameters = []
    private = False
    returns = ""
    throws = []

    parsed = docstring.splitlines()

    ###############################################################
    # Description
    ###############################################################

    def find_description_end() -> int:
        """Searches the docstring and finds which the first tag. The line before is where the description ends."""
        i = 0
        for line in parsed:
            this_line = line.strip()
            if this_line[0:1] == "@":
                return i - 1
            i += 1
        
        return i # No tags found, the entire thing is the description

    def get_description() -> str:
        """Parses the docstring up to the end of the description and formats it into paragraphs.
            Only goes up to the first tag, nothing after that gets recorded here."""
        parsed_desc = ""
        for i in range(0, find_description_end()):
            if parsed_desc != "" and parsed[i].strip() == "":   # Make sure the opening doesn't have a carriage returns
                parsed_desc += "\n"
            elif parsed_desc[-1:] == "\n":  # No spaces after new lines
                parsed_desc += parsed[i].strip()
            elif parsed[i].strip()[0:2] == "- ": # Bulleted (i.e. unordered) lists
                    parsed_desc += "\n" + parsed[i].strip()
            elif parsed[i].strip()[0:4] == "<ul>": # Bulleted (i.e. unordered) lists using <ul> code
                parsed_desc += "\n- " + parsed[i].strip()[4:len(parsed[i].strip())]
            elif parsed[i].strip()[0:4] == "<ol>": # Numbered (i.e. ordered) lists
                parsed_desc += "\n" + parsed[i].strip()[4:len(parsed[i].strip())]
            else:   # continue the sentence from the interrupted paragraph with a space separator
                parsed_desc += " " + parsed[i].strip()
        return parsed_desc.strip()


    ###############################################################
    # Tags
    ###############################################################

    def get_examples() -> None:
        """
        Goes through the doc string and looks for examples annotated by the @example tag.
        
        Note: JSDoc example tag allows <caption> after this. This function does not support that at this time.
        """
        code_block = None
        caption = ""
        code_offset = 0

        def add_example(code: str, capt: str) -> None:
            """
                Adds the example code to the examples dictionary entry.
                Can have multiple examples, and each can be the exact same if desired.
            """
            nonlocal code_block

            if capt == "":
                capt = None
            
            examples.append({"caption": capt, "code": code.strip('\n')})
            code_block = None

        for line in parsed:

            if line.strip()[0:8] == "@example":
                if code_block is not None:
                    # Previous example code block complete, about to start a new one
                    add_example(code_block, caption)
                
                # We have encountered a new example, start recording the info
                code_offset = re.search("@example", line).start()    # How many white spaces exist before the @example tag
                code_block = ""

                caption = line.strip()[9:len(line)]
                continue

            if code_block is not None and line.strip()[0:1] != "@":
                code_block += line[code_offset:len(line)] + "\n"
                continue
            
            if code_block is not None and line.strip()[0:1] == "@":  
                # Already started parsing an example block, but now encountering a new tag
                add_example(code_block, caption)
        
        if code_block is not None:   # Final catch for examples not added yet
            add_example(code_block, caption)

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
    
    def get_private() -> None:
        """Goes through the doc string and looks for a @private tag"""

        for line in parsed:

            if line.strip() == "@private":
                return True
        
        return False

    def get_returns() -> str:
        """Goes through the doc string and looks for the final return value annotated by the @returns tag"""
        return_desc = ""
        record_return_description = False

        for line in parsed:
            stripped_line = line.strip()
            
            if stripped_line[0:9] == "@returns ":
                # Start a new @returns check. Only the last @returns should work, so no check if we've already found one 
                return_desc = return_desc.strip()
                record_return_description = True
                
                # We have encountered a new return description, start recording the info
                return_desc = stripped_line[9:len(stripped_line)]
                continue

            if return_desc != "" and stripped_line[0:1] == "@" and record_return_description:
                # Already started parsing a parameter, but now encountering a new tag
                return_desc = return_desc.strip()
                record_return_description = False
                continue

            if return_desc != "" and record_return_description:
                # Have found a returns tag already, and now its description has spilled on to another line
                if stripped_line == "": # Add a paragraph break
                    return_desc += "\n"
                elif return_desc[-1:] == "\n": # Do not add an extra space for new paragraphs.
                    return_desc += stripped_line
                else:
                    return_desc += " " + stripped_line

        if return_desc != "":   # If trying to .strip() the value 'None', then it will throw an error.
            return return_desc.strip()
    
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


    # Begin parsing the docstring
    description = get_description()

    # Parse Tags (Alphabetical Order)
    get_examples()
    get_parameters()
    private = get_private()
    returns = get_returns()
    get_throws()

    return {
        "description": description,

        # Tags (Alphabetical Order)
        "examples": examples,
        "parameters": parameters,
        "private": private,
        "returns": returns,
        "throws": throws,
    }
