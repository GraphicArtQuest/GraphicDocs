def get_namespaces(docstring: str) -> None:
    """
    Goes through the doc string and looks for namespaces annotated by the `@namespace` tag.
    
    The namespace name is required following the tag, and must be a valid Python variable name.

    It may have an optional description. If no description provided, this portion returns `None`.
    
    If no `@namespace` tag found, or an invalid `@namespace` tag(s), it returns `None`.
    """
    
    parsed = docstring.splitlines()

    description = None
    namespace = ""
    namespace_array = []

    def add_namespace(name: str, desc: str) -> None:
        """
            Adds the namespace to the list.
            Can have multiple namespaces, and each can be the exact same if desired.
            Repeated namespaces will get handled in later documentation generating.
        """
        nonlocal description

        if desc is not None:
            desc = desc.strip('\n').strip()
        if desc == "":
            desc = None
        
        name = name.strip()

        if name.isidentifier(): # Namespaces must follow Python variable name validation rules
            namespace_array.append({"name": name, "description": desc})
        description = None

    for line in parsed:
        stripped_line = line.strip()

        if stripped_line[0:11] == "@namespace ":
            if description is not None:
                # Previous namespace description complete, about to start a new one
                add_namespace(namespace, description)
            
            # We have encountered a new namespace, start recording the info
            description = ""

            namespace = stripped_line[11:len(line)]
            continue

        if description is not None and stripped_line[0:1] != "@":
            if stripped_line == "": # Add a paragraph break
                description += "\n"
            elif description[-1:] == "\n": # Do not add an extra space for new paragraphs.
                description += stripped_line
            else:
                description += " " + stripped_line
            continue
        
        if description is not None and stripped_line[0:1] == "@":
            # Already started parsing a namespace, but now encountering a new tag
            add_namespace(namespace, description)
    
    if description is not None:   # Final catch for namespaces not added yet
        add_namespace(namespace, description)
    
    if len(namespace_array) > 0:
        return namespace_array
    return None