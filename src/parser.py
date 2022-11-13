def parse_docstring(docstring: str) -> dict:
    """
        Parses a doc string and returns a dict of the string formatted into component parts.
        
        The description must be at the top. Everything before the first tag gets treated as description.

        The parser treats consecutive lines as part of a single paragraph. To make a new paragraph, add an additional
        blank line to separate it from the previous one.

        You can use ordered lists by putting them on their own line using either a "-" or "<ul>" character.
        Omitting the space after the '-' character will not treat it as an unordered list.

        Ordered lists can be created with the "<ol>" character before it.
    """
    # Guard clause
    if not isinstance(docstring, str):
        return

    description = ""

    parsed = docstring.splitlines()

    def find_description_end() -> int:
        """Searches the docstring and finds which the first tag. The line before is where the description ends."""
        i = 0
        for line in parsed:
            this_line = line.strip()
            if this_line[0:1] == "@":
                return i - 1
            i += 1
        
        return i # No tags found, the entire thing is the description

    def get_description() -> str:
        """Parses the docstring up to the end of the description and formats it into paragraphs.
            Only goes up to the first tag, nothing after that gets recorded here."""
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

    
    description = get_description()

    return {
        "description": description
    }
