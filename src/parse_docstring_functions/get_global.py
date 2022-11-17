def get_global(docstring: str) -> bool:
    """
        Goes through the docstring and looks for a `@global` tag. This indicates that this should be treated as part of
        the global namespace, regardless of where it was found in the code.

        If found, it returns `True`. If omitted, it returns `False`.
    """

    parsed = docstring.splitlines()

    for line in parsed:

        if line.strip() == "@global":
            return True

    return False
