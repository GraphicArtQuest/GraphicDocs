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

        - @deprecated
        - @example
        - @global
        - @ignore
        - @license
        - @param
        - @private
        - @public
        - @returns
        - @since
        - @throws
        - @version
    """

    # Guard clause
    if not isinstance(docstring, str):
        return

    description = ""

    deprecated = False
    examples = []
    is_global = False
    ignore = False
    license = None
    parameters = []
    private = False # If False, this implicitly makes this a public module
    returns = ""
    since = None
    throws = []
    version = None

    parsed = docstring.splitlines()

    ###############################################################
    # Description
    ###############################################################

    def get_description() -> str:
        """Parses the docstring up to the end of the description and formats it into paragraphs.
            Only goes up to the first tag, nothing after that gets recorded here."""
            
        def find_description_end() -> int:
            """Searches the docstring and finds which the first tag. The line before is where the description ends."""
            i = 0
            for line in parsed:
                this_line = line.strip()
                if this_line[0:1] == "@":
                    return i - 1
                i += 1
            
            return i # No tags found, the entire thing is the description

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

    def get_deprecated() -> str:
        """
            Goes through the doc string and looks for the final deprecation value annotated by a @deprecated tag.
            Only the last @deprecated tag will get recorded.
            
            If no description is provided, the returned value will be `True`, otherwise it will be the provided string.
        """
        desc = ""
        record_desc = False # Used as a flag to tell if in the process of recording a block of description text
        found_deprecated = False

        for line in parsed:
            stripped_line = line.strip()
            
            if stripped_line[0:11] == "@deprecated":
                # Start a new @deprecated check.
                # Only the last @deprecated should work, so no need to check if we've already found one 
                desc = desc.strip()
                record_desc = True
                found_deprecated = True
                
                # We have encountered a new deprecated description, start recording the info
                desc = stripped_line[11:len(stripped_line)]
                continue

            if desc != "" and stripped_line[0:1] == "@" and record_desc:
                # Already started parsing a deprecation string, but now encountering a new tag
                desc = desc.strip()
                record_desc = False
                continue

            if desc != "" and record_desc:
                # Have found a deprecated tag already, and now its description has spilled on to another line
                if stripped_line == "": # Add a paragraph break
                    desc += "\n"
                elif desc[-1:] == "\n": # Do not add an extra space for new paragraphs.
                    desc += stripped_line
                else:
                    desc += " " + stripped_line

        if desc != "":   # If trying to .strip() the value 'None', then it will throw an error.
            return desc.strip()
        elif found_deprecated:
            return True
        return False

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

    def get_global() -> None:
        """Goes through the doc string and looks for a @global tag"""

        for line in parsed:

            if line.strip() == "@global":
                return True
        
        return False

    def get_ignore() -> None:
        """Goes through the doc string and looks for an @ignore tag"""

        for line in parsed:

            if line.strip() == "@ignore":
                return True
        
        return False

    def get_license() -> str:
        """
            Goes through the doc string and looks for the final license value annotated by a `@license` tag.
            Only the last `@license` tag will get recorded.

            If both name and text are provided, the returned object has both values.
            
            If only name or text is provided, the returned value for the other variable be `None`.

            If neither is provided, or the tag is not used, it returns `None`.
        """
        text = ""
        record_text = False # Used as a flag to tell if in the process of recording a block of description text
        license_name = ""

        for line in parsed:
            stripped_line = line.strip()
            
            if stripped_line[0:8] == "@license":
                # Start a new @license check.
                # Only the last @license should work, so no need to check if we've already found one 
                text = text.strip()
                record_text = True
                
                # We have encountered a new license description, start recording the info
                text = ""
                license_name = line.strip()[9:len(line)]
                continue

            if stripped_line[0:1] == "@" and record_text:
                # Already started parsing a deprecation string, but now encountering a new tag
                text = text.strip()
                record_text = False
                continue

            if record_text:
                # Have found a license tag already, and now its description has spilled on to another line
                if stripped_line == "": # Add a paragraph break
                    text += "\n"
                elif text[-1:] == "\n": # Do not add an extra space for new paragraphs.
                    text += stripped_line
                else:
                    text += " " + stripped_line

        text = text.strip()
        if text == "":
            text = None

        if license_name == "":
            license_name = None

        if text is None and license_name is None:
            return None                
        return {"name": license_name, "text": text}

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
        # Note: Because the parser assumes public by default and private takes precedence over public, there is no need
        #   for an additional @public tag search. Lack of a @private tag indicates it is public.

        for line in parsed:

            if line.strip() == "@private":
                return True
        
        return False

    def get_returns() -> str:
        """Goes through the doc string and looks for the final return value annotated by the @returns tag"""
        desc = ""
        record_desc = False # Used as a flag to tell if in the process of recording a block of description text

        for line in parsed:
            stripped_line = line.strip()
            
            if stripped_line[0:9] == "@returns ":
                # Start a new @returns check. Only the last @returns should work, so no check if we've already found one 
                desc = desc.strip()
                record_desc = True
                
                # We have encountered a new return description, start recording the info
                desc = stripped_line[9:len(stripped_line)]
                continue

            if desc != "" and stripped_line[0:1] == "@" and record_desc:
                # Already started parsing a parameter, but now encountering a new tag
                desc = desc.strip()
                record_desc = False
                continue

            if desc != "" and record_desc:
                # Have found a returns tag already, and now its description has spilled on to another line
                if stripped_line == "": # Add a paragraph break
                    desc += "\n"
                elif desc[-1:] == "\n": # Do not add an extra space for new paragraphs.
                    desc += stripped_line
                else:
                    desc += " " + stripped_line

        if desc != "":   # If trying to .strip() the value 'None', then it will throw an error.
            return desc.strip()

    def get_since() -> str:
        """
            Goes through the doc string and looks for the final since value annotated by a `@since` tag.
            Only the last `@since` tag will get recorded.
            
            If no description is provided or the tag is omitted, the returned value will remain `False`.
            Otherwise, it will be the provided string.
        """
        desc = ""
        record_desc = False # Used as a flag to tell if in the process of recording a block of description text

        for line in parsed:
            stripped_line = line.strip()
            
            if stripped_line[0:6] == "@since":
                # Start a new @since check.
                # Only the last @since should work, so no need to check if we've already found one 
                desc = desc.strip()
                record_desc = True
                
                # We have encountered a new since description, start recording the info
                desc = stripped_line[6:len(stripped_line)]
                continue

            if desc != "" and stripped_line[0:1] == "@" and record_desc:
                # Already started parsing a since string, but now encountering a new tag
                desc = desc.strip()
                record_desc = False
                continue

            if desc != "" and record_desc:
                # Have found a since tag already, and now its description has spilled on to another line
                if stripped_line == "": # Add a paragraph break
                    desc += "\n"
                elif desc[-1:] == "\n": # Do not add an extra space for new paragraphs.
                    desc += stripped_line
                else:
                    desc += " " + stripped_line

        if desc != "":   # If trying to .strip() the value 'None', then it will throw an error.
            return desc.strip()
        return None
   
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

    def get_version() -> str:
        """
            Goes through the doc string and looks for the final version value annotated by a `@version` tag.
            Only the last `@version` tag will get recorded.
            
            If no description is provided or the tag is omitted, the returned value will remain `None`.
            Otherwise, it will be the provided string.
        """
        desc = ""
        record_desc = False # Used as a flag to tell if in the process of recording a block of description text
        this_tag = "@version"

        for line in parsed:
            stripped_line = line.strip()
            
            if stripped_line[0:len(this_tag)] == this_tag:
                # Start a new @version check.
                # Only the last @version should work, so no need to check if we've already found one 
                desc = desc.strip()
                record_desc = True
                
                # We have encountered a new version description, start recording the info
                desc = stripped_line[len(this_tag):len(stripped_line)]
                continue

            if desc != "" and stripped_line[0:1] == "@" and record_desc:
                # Already started parsing a version string, but now encountering a new tag
                desc = desc.strip()
                record_desc = False
                continue

            if desc != "" and record_desc:
                # Have found a version tag already, and now its description has spilled on to another line
                if stripped_line == "": # Add a paragraph break
                    desc += "\n"
                elif desc[-1:] == "\n": # Do not add an extra space for new paragraphs.
                    desc += stripped_line
                else:
                    desc += " " + stripped_line

        if desc != "":   # If trying to .strip() the value 'None', then it will throw an error.
            return desc.strip()
        return None

    # Begin parsing the docstring
    description = get_description()

    # Parse Tags (Alphabetical Order)
    deprecated = get_deprecated()
    get_examples()
    is_global = get_global()
    ignore = get_ignore()
    license = get_license()
    get_parameters()
    private = get_private()
    returns = get_returns()
    since = get_since()
    get_throws()
    version = get_version()

    return {
        "description": description,

        # Tags (Alphabetical Order)
        "deprecated": deprecated,
        "examples": examples,
        "global": is_global,
        "ignore": ignore,
        "license": license,
        "parameters": parameters,
        "private": private,
        "returns": returns,
        "since": since,
        "throws": throws,
        "version": version
    }
