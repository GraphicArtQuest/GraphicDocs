def get_authors(docstring: str) -> None:
    """Goes through the docstring and looks for authors annotated by the @author tag"""
    
    parsed = docstring.splitlines()
    
    authors_array = []
    author_name = ""
    author_email = ""

    for line in parsed:
        stripped_line = line.strip()

        if stripped_line[0:8] == "@author ":
            # We have encountered a new parameter, start recording the info
            email_start = stripped_line.find("[", 9)
            email_end = stripped_line.find("]", 9)

            if email_start > 0 and email_end > 0:
                author_name = stripped_line[8:email_start - 1].strip()
                author_email = stripped_line[email_start + 1:email_end].strip()
            else:
                author_name = stripped_line[8:len(stripped_line)].strip()
                author_email = None

            authors_array.append({"name": author_name, "email": author_email})
    
    if len(authors_array) > 0:
        return authors_array
    return None