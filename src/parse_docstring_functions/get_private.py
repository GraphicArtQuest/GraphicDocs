def get_private(docstring: str) -> bool:
    """
        Goes through the docstring and looks for a `@private` tag. This indicates that this object should be treated as
        private to the object and should not be part of the generated documentation.
        
        If found, it returns `True`. If omitted, it returns `False`.
    """

    parsed = docstring.splitlines()

    # Note: Because the parser assumes public by default and private takes precedence over public, there is no need
    #   for an additional @public tag search. Lack of a @private tag indicates it is public.

    for line in parsed:

        if line.strip() == "@private":
            return True

    return False
