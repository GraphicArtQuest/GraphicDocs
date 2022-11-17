def get_todo(docstring: str) -> str:
    """
        Goes through the doc string and looks for any `@todo` tags. It returns either an array of all the tags
        it found, or if there were no tags then it returns `None`.
    """
    
    parsed = docstring.splitlines()

    desc = ""
    record_desc = False # Used as a flag to tell if in the process of recording a block of description text
    todo_array = []

    for line in parsed:
        stripped_line = line.strip()
        
        if stripped_line[0:6] == "@todo ":
            # Start a new @todo check. Only the last @returns should work, so no check if we've already found one 
            if desc != "":
                # We were in the middle of parsing another todo tag, add this one before continuing
                todo_array.append(desc.strip("\n"))

            desc = desc.strip()
            record_desc = True
            
            # We have encountered a new return description, start recording the info
            desc = stripped_line[6:len(stripped_line)]
            continue

        if desc != "" and stripped_line[0:1] == "@" and record_desc:
            # Already started parsing a parameter, but now encountering a new tag
            desc = desc.strip()
            todo_array.append(desc.strip("\n"))

            desc = ""
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
        desc.strip()
        todo_array.append(desc.strip("\n"))
    
    if len(todo_array) > 0:
        return todo_array
    return None