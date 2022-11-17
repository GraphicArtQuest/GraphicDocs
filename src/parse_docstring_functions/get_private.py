def get_private(docstring: str) -> None:
    """Goes through the doc string and looks for a @private tag"""

    parsed = docstring.splitlines()

    # Note: Because the parser assumes public by default and private takes precedence over public, there is no need
    #   for an additional @public tag search. Lack of a @private tag indicates it is public.

    for line in parsed:

        if line.strip() == "@private":
            return True
    
    return False
