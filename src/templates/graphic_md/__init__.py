import os

import src.templates.graphic_md.page_builder as page_builder

def register_hooks(core) -> None:
    """ Registers a series of hooks into the core instance."""

    def graphic_md_action_hook():
        pass

    def graphic_md_filter_hook(input: any = None) -> any:
        return input

    core.console("Registering Graphic_MD Template Hooks...")

    # TEMPLATE FILTERS AND ACTIONS
    core.filters.add("graphic_md_output_file_path", graphic_md_filter_hook, 0)

    core.actions.add("graphic_md_register_hooks", graphic_md_action_hook, 0)
    core.actions.add("graphic_md_overwrite_existing_page", graphic_md_action_hook, 0)
    core.actions.add("graphic_md_file_closed", graphic_md_action_hook, 0)
    core.actions.add("graphic_md_skipped_output", graphic_md_action_hook, 0)
    core.actions.add("graphic_md_build_complete", graphic_md_action_hook, 0)

def build(core) -> None:

    register_hooks(core)
    core.do_action('graphic_md_register_hooks')

    core.console("Building documentation pages with the Graphic_MD template...")

    num_built:int = 0   # For statistics tracking

    if not os.path.exists(core.config["destination"]):
        os.mkdir(core.config["destination"])

    for module in core.parsed_results:
        destination = os.path.join(core.config["destination"], module["name"]).split('.')[0] + ".md"
        destination = core.apply_filter('graphic_md_output_file_path', destination)

        if os.path.exists(destination):
            if core.config['destination_overwrite']:
                core.do_action('graphic_md_overwrite_existing_page', {"existing_page": destination})
            else:
                core.do_action('graphic_md_skipped_output', {"existing_page": destination})
                continue

        result = page_builder.build_page(module, core, destination)

        file = open(destination, "w+")
        file.write(result)
        file.close()

        num_built += 1
        core.do_action('graphic_md_file_closed', {"built_page": destination})

    # Final statistics and reporting completion
    num_parse = len(core.parsed_results)
    parsing_analysis = {"parsed": num_parse, "skipped": num_parse - num_built, "built": num_built}

    core.do_action("graphic_md_build_complete", parsing_analysis)
