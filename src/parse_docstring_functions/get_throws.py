import re

def get_throws(docstring: str) -> None:
    """Goes through the doc string and looks for exceptions annotated by the @throws tag"""
    
    parsed = docstring.splitlines()

    throws = []
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

    if len(throws) > 0:
        return throws
    return None