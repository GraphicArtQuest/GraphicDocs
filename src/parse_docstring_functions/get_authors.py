def get_authors(docstring: str) -> list[dict[str | None, str | None]] | None:
    """
        Goes through the docstring and looks for authors annotated by the @author tag.

        If no authors are found, it returns `None`. Otherwise, it returns a list of dictionaries with keys
        `name` and `email`. Either author name or email may be left blank, which will return that key as `None`.
        The email value is everything between a set of brackets.

        For example:
        - `@author John Doe`
            - Returns: `{"name": "John Doe", "email": None}`
        - `@author John Doe [John.Doe@myemail.com]`
            - Returns: `{"name": "John Doe", "email": "john.doe@somedomain.com"}`
        - `@author [john.doe@somedomain.com]`
            - Returns: `{"name": None, "email": "john.doe@somedomain.com"}`
    """

    parsed = docstring.splitlines()

    authors = []
    author_name = ""
    author_email = ""

    for line in parsed:
        stripped_line = line.strip()

        if stripped_line[0:8] == "@author ":
            # We have encountered a new author, start recording the info
            email_start = stripped_line.find("[", 9)
            email_end = stripped_line.find("]", 9)

            if email_start > 0 and email_end > 0:
                author_name = stripped_line[8:email_start - 1].strip()
                author_email = stripped_line[email_start + 1:email_end].strip()
            else:
                author_name = stripped_line[8:len(stripped_line)].strip()
                author_email = None

            authors.append({"name": author_name, "email": author_email})
    
    if len(authors) > 0:
        return authors
    return None
