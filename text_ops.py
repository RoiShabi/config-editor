from typing import TextIO

def search_line_index_in_content(lines_in_file: list[str], field_name: str) -> int:
    index = 0
    for line in lines_in_file:
        if(line.startswith(field_name)):
            return index
        else:
            index += 1
    return index

def update_line_with_key(line: str, key: str) -> str:
    char_index = line.find(key)
    if(char_index == -1):
        new_line = line + ' ' + key
        return new_line
    else:
        return line
