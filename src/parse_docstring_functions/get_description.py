def get_description(docstring: str) -> str:
    """Parses the docstring up to the end of the description and formats it into paragraphs.
        Only goes up to the first tag, nothing after that gets recorded here."""
    
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
    return parsed_desc.strip()
