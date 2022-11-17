def get_version(docstring: str) -> str | None:
    """
        Goes through the docstring and looks for the version value of an object as annotated by a `@version` tag.

        If the docstring has more than one of these tags, the function will only record the last `@version` tag found.
        If the tag is not included or is left blank, it will return `None`.

        For example:
        - `@version v1.2.2`
            - Returns: `"v1.2.2"`
    """

    parsed = docstring.splitlines()

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
