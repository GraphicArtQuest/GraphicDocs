def get_license(docstring: str) -> dict[str | None, str | None] | None:
    """
        Goes through the doc string and looks for the final license value annotated by a `@license` tag.
        If the docstring has more than one of these tags, the function will only record the last `@license` tag found.

        The license name is everything on the first line following the `@license ` tag, and the text is everything
        on the subsequent lines up until the next tag or the end of the docstring.

        If both name and text are provided, the returned object has both values.
        If only name or text is provided, the function returns `None` for that key.

        If neither is provided, or the tag is not used, it returns `None`.

        For example:
        - `@license MIT`
            - Returns: `{"name": "MIT", "text": None}`
        - ```
    """

    parsed = docstring.splitlines()

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
