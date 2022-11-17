import re

def get_examples(docstring: str) -> None:
    """
    Goes through the doc string and looks for examples annotated by the @example tag.
    
    Note: JSDoc example tag allows <caption> after this. This function does not support that at this time.
    """
    
    parsed = docstring.splitlines()
    
    examples = []

    code_block = None
    caption = ""
    code_offset = 0

    def add_example(code: str, capt: str) -> None:
        """
            Adds the example code to the examples dictionary entry.
            Can have multiple examples, and each can be the exact same if desired.
        """
        nonlocal code_block

        if capt == "":
            capt = None
        
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
