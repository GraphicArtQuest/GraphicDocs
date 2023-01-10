import os

tableofcontents:list = []

def md_header(header_level: int = 1) -> str:
    """ Heler function to format a specified number of Markdown headers (i.e. H1 - H6) using the `#` character.

        @param header_level Corresponds to the number of `#` characters to return. Will default to 1 if provided a
        non-coercible integer or any number less than 1.
        @returns A string of `#` characters.
    """
    try:
        header_level = max(int(header_level), 1)
    except:
        header_level = 1

    result = ""
    for i in range(header_level):
        result += "#"

    return result

def md_link(text, target: str = "#") -> str:
    """ Helper function to format a link into Markdown syntax.

        @param text The plain text for the link.
        @param the hyperlink target for the link.
        @returns A markdown formatted link as `[text](target)`
    """
    return f"[{text}]({target})"

def md_source(sourcefile: str, lineno: tuple) -> str:
    """ Helper function to format source file locations."""
    
    if not sourcefile:
        return ""

    link = os.path.relpath(sourcefile, os.path.dirname(destination_filepath)).replace('\\', '/')

    sourcefile = sourcefile.split('\\')[-1]
    sourcefile = sourcefile.split('/')[-1] # Makes sure to grab the final part of whichever the filename is

    if lineno:
        lineno_part = f", lines {lineno[0]} thru {lineno[1]}"
        link += f"#L{lineno[0]}-L{lineno[1]}"
    else:
        lineno_part = ""

    source_text = f"_Source: {md_link(sourcefile + lineno_part, link)}_\n"
    return source_text

def ds_deprecated(docstring: dict) -> str:
    """ Formats the docstring 'deprecated' block for Markdown.
        @param A parsed docstring object.
        @returns Proper Markdown formatted text."""

    if not docstring:
        return ""

    result = ""
    if docstring["deprecated"] == True:
        result += "***NOTE: THIS FUNCTION IS DEPRECATED***" # Default statement if no description provided
    elif isinstance(docstring["deprecated"], str):
        result += f"***DEPRECATED: {docstring['deprecated']}***"
    return result + "\n\n"

def ds_description(docstring: dict) -> str:
    """ Formats the docstring 'description' block for Markdown.
        @param A parsed docstring object.
        @returns Proper Markdown formatted text.
    """

    if not docstring:
        return ""

    if docstring["description"]:
        return "> " + docstring["description"].replace("\n", "\n>\n> ") + "\n\n"
    return ""

def ds_examples(examples: list[dict]) -> str:
    """ Formats the docstring 'example' block for Markdown.
        @param A parsed docstring object's `examples` list.
        @returns Proper Markdown formatted text.
    """
    if not examples:
        return ""

    result = ""
    for example in examples:
        if example["caption"]:
            result += example["caption"] + "\n\n"
        result += "```python\n"
        result += example["code"] + "\n"
        result += "```\n\n"

    return result

def create_imports_block(import_data: dict) -> str:
    """ A helper function to create the imported data block.

        @param import_data The parsed data entry from the module info's `imported` key.
        @returns A formatted string to write into the documentation markdown file.
    """
    result = ""
    if import_data["modules"]:
        result += "\n*Modules*\n"
        for module in import_data["modules"]:
            result += f"- {module}\n"

    if import_data["classes"]:
        result += "\n*Classes*\n"
        for cls in import_data["classes"]:
            result += f"- {cls[1]} (from `{cls[0]}`)\n"

    if import_data["functions"]:
        result += "\n*Functions*\n"
        for function in import_data["functions"]:
            result += f"- {function[1]} (from `{function[0]}`)\n"

    if result:
        tableofcontents.append("- [Imports](#imports)")
        return "## Imports\n" + result + "\n"
    else:
        return  ""

def argument_list(args_list: list) -> str:
    """ Processes the arguments into a readable format.
        
        @param args_list A parsed list of argument data.
        @returns A Markdown formatted version of the data with required parameters in bold and optionals italicized. 
        For example: `(*arg1*, *arg2*, _arg3_)`
    """
    if not args_list:
        return ""

    argument_list = ""
    for arg in args_list:
        if arg["required"]:
            argument_list += f"**`{arg['name']}`**,  "
        else:
            argument_list += f"_`{arg['name']}`_,  "
    if argument_list:
        argument_list = argument_list[:-3]  # Strip off trailing comma and space `, `

    return argument_list

def argument_table(args_list: list, params_list: list) -> str:
    """ Processes the arguments detailed info into an easily readable table.
        
        @param args_list A parsed list of argument data.
        @param params_list A parsed list of docstring parameters
        @returns A Markdown formatted table of argument data. 
    """
    if not args_list:
        return ""

    result = "|Argument |Type |Default | Description\n"
    result += "|:---|:---:|:---|:---|\n"
    for arg in args_list:
        # Build out each data row of the arguments table
        name = f"`{arg['name']}`"
        try:
            type = f"`{arg['type'].__name__}`"
        except:
            type = f"`{arg['type']}`"
        type = type.replace('|', '\|')  # Prevent rendering issues with Markdown tables by escaping the pipe

        if not arg['required']:
            name += " _(Optional)_"
            if arg['type'] == str:
                default = f"`'{arg['default']}'`"
            else:
                default = f"`{arg['default']}`"
        else:
            default = ""

        try:
            # If no parameters were provided, trying to access will throw an error
            params = params_list['parameters']
            desc = ""
            for param in params:
                if arg['name'] in param:
                    desc = param[arg['name']]
                    break
        except:
            desc = ""

        result += f"|{name} |{type} |{default} | {desc}|\n"
    
    return result + "\n"

def formatted_definition(name: str, arguments: list[dict]) -> str:
    """ Helper to neatly format class and function names with their arguments

        @param name The name of the class or function
        @arguments A parsed arguments list
        @returns A Markdown formatted name
    """

    if arguments:
        result = f"`{name}`( {argument_list(arguments)} )"
    else:
        result = f"`{name}`()"
    
    return result

def create_function_block(function_data: dict) -> str:
    """ A helper function to create a function data block.

        @param class_data The parsed data entry from the module info's `classes` key.
        @returns A formatted string to write into the documentation markdown file.
    """
    docstring = function_data["docstring"]

    if docstring and (docstring["private"] or docstring["ignore"]):
        return ""

    hyperlink = f"<a id='{function_data['name'].lower()}'></a>\n\n"
    result = f"{formatted_definition(function_data['name'], function_data['arguments'])}{hyperlink}\n\n"
    result += argument_table(function_data['arguments'], function_data['docstring'])
    result += ds_deprecated(docstring)
    result += ds_description(docstring)

    result += md_source(function_data['sourcefile'], function_data['lineno']) + "\n"

    if docstring["returns"]:
        if isinstance(function_data['returns'], type):
            returns = function_data['returns'].__name__
        else:
            returns = function_data['returns']  # Catches things like `True`

        result += f"**Returns** -> `{returns}`: {docstring['returns']}\n\n"

    if docstring["examples"]:
        result += "Examples:\n\n"
        result += ds_examples(docstring["examples"])

    return result

def create_class_block(class_data: dict, header_level: int = 1) -> str:
    """ A helper function to create a class data block.

        @param class_data The parsed data entry from the module info's `classes` key.
        @returns A formatted string to write into the documentation markdown file.
    """

    if not class_data:
        return ""

    docstring = class_data["docstring"]

    if docstring and (docstring["private"] or docstring["ignore"]):
        return ""

    class_hyperlink = f"<a id=''></a>\n\n"
    result = f"{md_header(header_level)} {formatted_definition(class_data['name'], class_data['arguments'])}{class_hyperlink}\n\n"
    result += argument_table(class_data['arguments'], class_data['docstring'])
    result += ds_deprecated(docstring)
    if class_data["parent"]:
        result += f"Extends: `{class_data['parent']}`\n\n"

    result += ds_description(docstring)

    if class_data["sourcefile"]:
        result += f"_Source: [{os.path.splitext(class_data['sourcefile'])}]({class_data['sourcefile']})_"
    
    result += md_source(class_data['sourcefile'], class_data['lineno'])

    if class_data["subclasses"]:
        result += f"{md_header(header_level + 1)} Subclasses\n\n"

        for subclass in class_data["subclasses"]:
            result += f"- {subclass}"

    if class_data["methods"]:
        result += f"**Class Methods:**\n\n"

        for method in class_data["methods"]:
            info = create_function_block(class_data["methods"].get(method))

            if info:    # Prevent printing out private or ignored items
                info = info.replace('\n', '\n    ')
                result += f"- {info}\n"
                tableofcontents.append(f"        - [{method}](#class-{class_data['name'].lower() + method})")

    return result + "\n"

def build_page(module_info: dict, core, destination: str) -> str:
    """ Assembles an individual module documentation page.
        @param module_info The parsed module dictionary
        @param core A reference to the core object building this
        @param destination The desired output filepath
        @returns A consolidated string ready to insert into a file
    """
    # pp.pprint(module_info)
    global destination_filepath
    destination_filepath = destination  # Used when determining relative path links
    tableofcontents.clear()

    toc_replace_phrase = "<!-- REPLACE THIS COMMENT WITH TABLE OF CONTENTS -->"

    page = f"# Module: _`{module_info['name'][:-3]}`_\n\n"
    page += f"{md_source(module_info['sourcefile'], None)}\n\n"

    page += "Table of Contents\n\n"
    page += f"{toc_replace_phrase}\n\n"

    page += create_imports_block(module_info["imported"])

    page += "----\n\n"

    if module_info["classes"]:
        page += "# Classes\n\n"
        tableofcontents.append('- [Classes](#classes)')
        for cls in module_info["classes"]:
            if module_info["classes"].get(cls): # Prevents writing null classes
                link = 'class-' + cls.lower()

                tableofcontents.append(f"    - [{cls}](#{link})")
                formatted_entry = create_class_block(module_info["classes"].get(cls), 2)
                formatted_entry = formatted_entry.replace("<a id='", f"<a id='{link}")  # Match up class function links

                page += formatted_entry
                page += "----\n\n"

    if module_info["functions"]:
        page += "# Functions\n\n"
        tableofcontents.append('- [Functions](#functions)')
        for func in module_info["functions"]:
            if func:
                tableofcontents.append(f"    - [{func}](#{func.lower()})")
                page += "## " + create_function_block(module_info["functions"].get(func))
                page += "----\n\n"

    try:
        page += core.config["graphic_md"]["footer"]
    except:
        pass

    page = page.replace(toc_replace_phrase, "\n".join(tableofcontents))
    return page
