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
    line_content: str = ""
    content_to_insert: str = ""
    start_index_to_mark: int = 0
    size_to_delete: int = 0

STATIC_LINE_ENDING = "\n"

def mark_key_in_line(line: str, key: str) -> TextMarkedSpan:
    existing_key_start_index = line.find(key)
    if(existing_key_start_index == -1):
        #doesnt exist
        end_content_index = len(line) - len(STATIC_LINE_ENDING)
        span = TextMarkedSpan(line_content=line, content_to_insert=' '+key, start_index_to_mark=end_content_index, size_to_delete=0)
        return span
    else:
        #exists
        end_char_of_key = existing_key_start_index + len(key)
        span = TextMarkedSpan(line_content=line, content_to_insert="", start_index_to_mark=existing_key_start_index, size_to_delete=0)
        return span

def update_line_with_value(line: str, ):
    pass