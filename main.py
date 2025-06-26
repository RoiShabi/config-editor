#!/usr/bin/env python3

import sys
from params_parse import parse_params
from typing import Optional
from text_ops import search_line_index_in_content, mark_key_in_line, set_value_to_span, generate_new_line, TextMarkedSpan, STATIC_LINE_ENDING, STATIC_FIELD_ASSIGNMENT

def main(argv: list[str]):
    args = argv[1:]
    file_path:str
    field: str
    value:str
    key: Optional[str]
    try:
        file_path, field, value, key = parse_params(args)
    except Exception as e:
        print(f"Error: {e}")
        print("Usage: python main.py file=<file> field=<field> value=<value> [key=<key>]\n\n")
        raise
        
    
    with open(file_path, 'r+') as file:
        lines_in_file = file.readlines()
        selected_line_index = search_line_index_in_content(lines_in_file, field)
        original_line_content: str
        if (selected_line_index == len(lines_in_file)):
            # Create new line
            lines_in_file.append("")
            original_line_content = None
            selected_line_content = field + STATIC_FIELD_ASSIGNMENT + STATIC_LINE_ENDING
        else:
            original_line_content = lines_in_file[selected_line_index]
            selected_line_content = original_line_content
        
        if (key is None):
            end_content_index = len(selected_line_content) - len(STATIC_LINE_ENDING)
            content_to_paste_span = TextMarkedSpan(line_content=selected_line_content, content_to_insert="", start_index_to_mark=len(field+STATIC_FIELD_ASSIGNMENT))
        else:
            content_to_paste_span = mark_key_in_line(selected_line_content, key)

        set_value_to_span(content_to_paste_span, value)
        new_line = generate_new_line(content_to_paste_span)
        
        if(original_line_content != new_line):
            # Write if there was actual change
            lines_in_file[selected_line_index] = new_line
            file.seek(0)
            file.writelines(lines_in_file)
            file.truncate()


        print("Debug content:")
        print("Parsed parameters:")
        print(f"  file     = {file_path}")
        print(f"  field    = {field}")
        print(f"  value    = {value}")
        print(f"  key      = {key}")
        print(f"Inner variables:")
        print(f"  updated_line_by_key   = {content_to_paste_span}")
        print(f"  updated_line_result (line {selected_line_index})  =")
        print(f"  old: {original_line_content}")
        print(f"  new: {new_line}")

if __name__ == "__main__":
    main(sys.argv)
