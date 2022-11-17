def get_deprecated(docstring: str) -> bool | str:
    """
        Goes through the docstring and looks for the final deprecation value annotated by a `@deprecated` tag.
        Only the last @deprecated tag will get recorded.
        
        If the tag is not included, this function returns `False`. If just the tag is included, it returns `True`.
        If a description is provided after the tag, it returns the provided string.

        For example:
        - `@deprecated`
        - `@deprecated This was deprecated in v1.5.2 because it was superceded by a newer function.`
    """

    parsed = docstring.splitlines()

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
