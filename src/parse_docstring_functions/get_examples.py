import re

def get_examples(docstring: str) -> list[dict[str | None, str]] | None:
    """
        Goes through the docstring and looks for examples annotated by the `@example` tag.

        If no examples are found, it returns `None`. Otherwise, it returns a list of dictionaries with keys
        `caption` and `code`. You can include as many examples as you need to.

        The caption is a short description of what this example does. It consists of all the text on the line following
        the `@example` tag. Leaving this blank will return `None` for that key.

        Everything on the subsequent lines until the next tag or the end of the docstring will get treated as formatted
        Python code. The indendation is based on the spacing to the `@example` tag, so any code to the left of this
        will get cut off.

        Although the caption is optional, there must be example code beneath the tag. If there is no code, this function
        will ignore that partiucular tag.
    """

    parsed = docstring.splitlines()

    examples = []

    code_block = None
    caption = ""
    code_offset = 0

    def add_example(code: str, capt: str) -> None:
        """
            Adds the example code dictionary to the examples list.
            Can have multiple examples, and each can be the exact same if desired.
        """
        nonlocal code_block

        if capt == "":
            capt = None
        if code.strip('\n') == "":
            return None # Empty code examples are meaningless

        examples.append({"caption": capt, "code": code.strip('\n')})
        code_block = None

    for line in parsed:

        if line.strip()[0:8] == "@example":
            if code_block is not None:
                # Previous example code block complete, about to start a new one
                add_example(code_block, caption)

            # We have encountered a new example, start recording the info
            code_offset = re.search("@example", line).start()    # How many white spaces exist before the @example tag
            code_block = ""

            caption = line.strip()[9:len(line)]
            continue

        if code_block is not None and line.strip()[0:1] != "@":
            code_block += line[code_offset:len(line)] + "\n"
            continue

        if code_block is not None and line.strip()[0:1] == "@":  
            # Already started parsing an example block, but now encountering a new tag
            add_example(code_block, caption)

    if code_block is not None:   # Final catch for examples not added yet
        add_example(code_block, caption)

    if len(examples) > 0:
        return examples
    return None
