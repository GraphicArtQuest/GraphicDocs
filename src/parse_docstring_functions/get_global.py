def get_global(docstring: str) -> None:
    """Goes through the doc string and looks for a @global tag"""
    
    parsed = docstring.splitlines()

    for line in parsed:

        if line.strip() == "@global":
            return True
    
    return False