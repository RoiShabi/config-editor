#!/usr/bin/env python3

import sys
from params_parse import parse_params
from text_ops import search_line_index_in_content, mark_key_in_line, set_value_to_span, TextMarkedSpan, STATIC_LINE_ENDING

def main():
    args = sys.argv[1:]
    try:
        file_path, field, value, key = parse_params(args)
        print("Parsed parameters:")
        print(f"  file     = {file_path}")
        print(f"  field    = {field}")
        print(f"  value    = {value}")
        print(f"  key      = {key}")
    except Exception as e:
        print(f"Error: {e}\n")
        print("Usage: python main.py file=<file> field=<field> value=<value> [key=<key>]")
    
    with open(file_path, 'r') as file:
        lines_in_file = file.readlines()
        selected_line_index = search_line_index_in_content(lines_in_file, field)
        if (selected_line_index == len(lines_in_file)):
            selected_line_content = field + STATIC_LINE_ENDING
        else:
            selected_line_content = lines_in_file[selected_line_index]
        
        if (key is None):
            end_content_index = len(selected_line_content) - len(STATIC_LINE_ENDING)
            content_to_paste_span = TextMarkedSpan(line_content=selected_line_content, content_to_insert="", start_index_to_mark=end_content_index)
        else:
            content_to_paste_span = mark_key_in_line(selected_line_content, key)

        set_value_to_span(content_to_paste_span, value)

        

        print("Debug content:")
        print(f"  selected_line_content  = {selected_line_content}")
        print(f"  updated_line_by_key   = {content_to_paste_span}")

if __name__ == "__main__":
    main()
