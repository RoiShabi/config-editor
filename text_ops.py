from typing import TextIO
from dataclasses import dataclass


def search_line_index_in_content(lines_in_file: list[str], field_name: str) -> int:
    index = 0
    for line in lines_in_file:
        if(line.startswith(field_name)):
            return index
        else:
            index += 1
    return index

@dataclass
class TextMarkedSpan:
    line_content: str
    content_to_insert: str
    start_index_to_delete: int
    size_to_delete: int

def update_line_with_key(line: str, key: str) -> TextMarkedSpan:
    STATIC_LINE_ENDING = "\n"
    char_index = line.find(key)
    newline_char_idx = len(line) - len(STATIC_LINE_ENDING)
    if(char_index == -1):
        new_line = line[:newline_char_idx] + ' ' + key + line[newline_char_idx:]
        value_start_index = len(new_line)-len(STATIC_LINE_ENDING)
        span = TextMarkedSpan(line_content=line, start_index_to_delete=value_start_index,  )
        return new_line
    else:
        return line

def update_line_with_value(line: str, )