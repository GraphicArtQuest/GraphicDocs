def get_memberof(docstring: str) -> list[str] | None:
    """
    Goes through the docstring and looks for the `@memberof` tag.
    
    This tag is for a single line only, and takes one argument: the member name following the tag. This name must
    be a valid Python variable name.
    
    If the tag is not included or is invalid, it returns `None`. Otherwise, it returns a list of unique member strings.
    
    For example:
    - `@memberof Tools`
    - `@memberof Tools.Wrenches`
    """

    parsed = docstring.splitlines()

    membersof = []

    for line in parsed:
        stripped_line = line.strip()

        if stripped_line[0:10] == "@memberof ":

            member = stripped_line[10:len(line)].strip()

            if member.isidentifier():
                if member not in membersof:  # Only add unique members
                    membersof.append(member)
            continue

    if len(membersof) > 0:
        return membersof
    return None
