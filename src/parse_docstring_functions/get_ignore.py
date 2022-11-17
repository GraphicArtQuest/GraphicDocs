def get_ignore(docstring: str) -> None:
    """Goes through the doc string and looks for an @ignore tag"""
    
    parsed = docstring.splitlines()

    for line in parsed:

        if line.strip() == "@ignore":
            return True
    
    return False
