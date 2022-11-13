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

        - @param
        - @returns
    """

    # Guard clause
    if not isinstance(docstring, str):
        return

    description = ""

    parameters = []
    returns = ""

    parsed = docstring.splitlines()

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
                parameter_description += " " + stripped_line

        if parameter_name != "":   # Final catch for parameters not added yet
            add_parameter(parameter_name, parameter_description)
    
    def get_returns() -> str:
        """Goes through the doc string and looks for the final return value annotated by the @returns tag"""
        return_desc = ""

        for line in parsed:
            stripped_line = line.strip()
            
            if stripped_line[0:9] == "@returns ":
                if return_desc != "":
                    # Previous returns description complete, about to start a new one
                    return_desc = return_desc.strip()
                
                # We have encountered a new return description, start recording the info
                return_desc = stripped_line[9:len(stripped_line)]
                continue

            if return_desc != "" and stripped_line[0:1] == "@":
                # Already started parsing a parameter, but now encountering a new tag
                return_desc = return_desc.strip()
                continue

            if return_desc != "":
                # Have found a parameter already, and now its description has spilled on to another line
                return_desc += " " + stripped_line

        if return_desc != "":   # Final catch for parameters not added yet
            return return_desc.strip()


    # Begin parsing the docstring
    description = get_description()

    # Parse Tags (Alphabetical Order)
    get_parameters()
    returns = get_returns()

    return {
        "description": description,

        # Tags (Alphabetical Order)
        "parameters": parameters,
        "returns": returns
    }
