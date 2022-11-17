def get_ignore(docstring: str) -> bool:
    """
        Goes through the docstring and looks for an `@ignore` tag. This indicates that the generated documentation
        should not include this object in the output.

        If found, it returns `True`. If omitted, it returns `False`.
    """

    parsed = docstring.splitlines()

    for line in parsed:

        if line.strip() == "@ignore":
            return True
    
    return False
