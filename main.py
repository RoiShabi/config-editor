#!/usr/bin/env python3

import sys
from params_parse import check_help_params, parse_params, ScriptConfiguration
from typing import Optional
from text_ops import search_line_index_in_content, mark_key_in_line, set_value_to_span, generate_new_line, TextMarkedSpan, STATIC_LINE_ENDING, STATIC_FIELD_ASSIGNMENT

def print_help():
    help_msg = \
        "Usage:\tconfig_editor.py file_path=... field=... value=... [OPTIONS]\n"\
            "Patches small changes in a file, used for automations for environment setup. See project's tests for best utilization.\n\n"
    
    help_msg += "OPTIONS:\n"\
        "\tdelimiter=...\tControl the delimiter used to seperate between values. Default is \',\'\n"\
        "\t\t\t  e.g \':\' is used in format \"\"PATH=\"element1:element2:element3\" \"\"\n"\
        "\t\t\t  e.g \',\' is used in format \"\"GRUB_CMDLINE_LINUX_DEFAULT=\"isolcpu=element1,element2,element3\" \"\"\n"\
        \
        "\tkey=...\t\tUsed if files where under the field the values are organized in a key=value or key=value1,value2 pairs\n"\
        "\t\t\t  e.g \',\' is used in format \"\"GRUB_CMDLINE_LINUX_DEFAULT=\"isolcpu=element1,element2,element3\" \"\"\n"\

    help_msg += "\n"
    print(help_msg)

def main(input_argv: list[str]) -> int:
    argv_filtered = input_argv[1:]

    if(check_help_params(argv_filtered)):
        print_help()
        return 0

    user_config: ScriptConfiguration
    try:
        user_config = parse_params(argv_filtered)
    except Exception as e:
        print(f"Error: {e}\n")
        print_help()
        return 1
        
    
    with open(user_config.file_path, 'r+') as file:
        lines_in_file = file.readlines()
        selected_line_index = search_line_index_in_content(lines_in_file, user_config.field)
        original_line_content: str
        if (selected_line_index == len(lines_in_file)):
            # Create new line
            lines_in_file.append("")
            original_line_content = None
            selected_line_content = user_config.field + STATIC_FIELD_ASSIGNMENT + STATIC_LINE_ENDING
        else:
            original_line_content = lines_in_file[selected_line_index]
            selected_line_content = original_line_content
        
        if (user_config.key is None):
            end_content_index = len(selected_line_content) - len(STATIC_LINE_ENDING)
            content_to_paste_span = TextMarkedSpan(line_content=selected_line_content, content_to_insert="", start_index_to_mark=len(user_config.field+STATIC_FIELD_ASSIGNMENT))
        else:
            content_to_paste_span = mark_key_in_line(selected_line_content, user_config.key)

        set_value_to_span(content_to_paste_span, user_config.value, user_config.delimiter)
        new_line = generate_new_line(content_to_paste_span)
        
        if(original_line_content != new_line):
            # Write if there was actual change
            lines_in_file[selected_line_index] = new_line
            file.seek(0)
            file.writelines(lines_in_file)
            file.truncate()


        print("Debug content:")
        print("Parsed parameters:")
        print(f"  file     = {user_config.file_path}")
        print(f"  field    = {user_config.field}")
        print(f"  value    = {user_config.value}")
        print(f"  key      = {user_config.key}")
        print(f"Inner variables:")
        print(f"  updated_line_by_key   = {content_to_paste_span}")
        print(f"  updated_line_result (line {selected_line_index})  =")
        print(f"  old: {original_line_content}")
        print(f"  new: {new_line}")
        
        return 0

if __name__ == "__main__":
    errcode = main(sys.argv)
    exit(errcode)
