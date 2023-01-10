# Graphic MD Template

## About

This template will build a single Markdown file for each module in the parsed source. It outputs all parsed modules into the same output folder regardless of the input heirarchy.

GraphicDocs uses this template by default if you do not provide a different valid template. As the default, it offers limited hooks to tap into.

## Flowchart

When the core's `build()` method executes, it follows the program logic below.
```mermaid
graph TD
    classDef action fill:red, color:white;
    classDef filter fill:blue, color:white;
    subgraph Legend
        legendAction[Action]:::action
        legendFilter[/Filter/]:::filter
        legendTemplate[Template Actions]
    end
```

```mermaid
%%{init: { 'theme':'dark', 'sequence': {'useMaxWidth':false} } }%%
graph TD
    classDef action fill:red,color:white;
    classDef filter fill:blue,color:white;

    BUILD([BUILD])
    COMPLETE([COMPLETE])

    BUILD --> register_hooks[Register Template Hooks] --> graphic_md_register_hooks:::action --> next_build_module


    next_build_module[/Get Next Parsed Module/] --> graphic_md_output_file_path[/graphic_md_output_file_path/]:::filter
    graphic_md_output_file_path --> output_exists{Output<br>Exists?}
    output_exists --> |yes| overwrite{Overwrite?}
    output_exists --> |no| create_new_file[Create New File]

    create_new_file --> individual_page_build[Build Page]
    --> write[Write Results To File]
    --> close[Close File]
    --> graphic_md_file_closed:::action
    --> morebuildingtargets

    overwrite --> |yes|graphic_md_overwrite_existing_page:::action --> individual_page_build
    overwrite --> |no| graphic_md_skipped_output:::action --> morebuildingtargets{More<br>Modules?}


    morebuildingtargets --> |yes|next_build_module
    morebuildingtargets --> |no|graphic_md_build_complete:::action

    graphic_md_build_complete --> COMPLETE
```
