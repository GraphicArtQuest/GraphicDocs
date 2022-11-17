import re

def get_parameters(docstring: str) -> list[dict[str]] | None:
    """
        Goes through the doc string and looks for parameters annotated by the `@param` tag.

        If no tags are found, it returns `None`. Otherwise, it returns a list of dicts. Each dict has a single key
        with the name of the parameter, and the key value is the description of what that parameter does.

        For example:
        - `@param MyParam This is my parameter description.
            - Returns: `{"MyParam": "This is my parameter description."}`
    """

    parsed = docstring.splitlines()

    parameters = []
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

    if len(parameters) > 0:
        return parameters
    return None
