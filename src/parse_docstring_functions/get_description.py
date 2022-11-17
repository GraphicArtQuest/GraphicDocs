def get_description(docstring: str) -> str | None:
    """
        Parses the docstring up to the end of the description (either the first line that has a tag as indicated by the
        `@` symbol, or the end of the string) and formats it into paragraphs.
        
        This function will treat a blank line in a description as a carriage return and start a new paragraph.
        Otherwise, it will treat subsequent lines as continuations of the previous line.

        This function will also parse unordered lists if a line starts with either `"- "` or `"<ul>"` and will parse
        ordered lists if it starts with `"<ol>"`.

        If there is no description, it will return `None`.
    """
    
    parsed = docstring.splitlines()

    def find_description_end() -> int:
        """Searches the docstring and finds which the first tag. The line before is where the description ends."""
        i = 0
        for line in parsed:
            this_line = line.strip()
            if this_line[0:1] == "@":
                return i
            i += 1
        
        return i # No tags found, the entire thing is the description

    parsed_desc = ""
    
    for i in range(0, find_description_end()):
        if parsed_desc != "" and parsed[i].strip() == "":   # Make sure the opening doesn't have a carriage returns
            parsed_desc += "\n"
        elif parsed_desc[-1:] == "\n":  # No spaces after new lines
            parsed_desc += parsed[i].strip()
        elif parsed[i].strip()[0:2] == "- ": # Bulleted (i.e. unordered) lists
                parsed_desc += "\n" + parsed[i].strip()
        elif parsed[i].strip()[0:4] == "<ul>": # Bulleted (i.e. unordered) lists using <ul> code
            parsed_desc += "\n- " + parsed[i].strip()[4:len(parsed[i].strip())]
        elif parsed[i].strip()[0:4] == "<ol>": # Numbered (i.e. ordered) lists
            parsed_desc += "\n" + parsed[i].strip()[4:len(parsed[i].strip())]
        else:   # continue the sentence from the interrupted paragraph with a space separator
            parsed_desc += " " + parsed[i].strip()
    
    if parsed_desc.strip() == "":
        return None
    return parsed_desc.strip()
