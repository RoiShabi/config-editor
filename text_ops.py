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

STATIC_LINE_ENDING = "\"\n"
STATIC_FIELD_ASSIGNMENT = "=\""
STATIC_KEY_ASSIGNMENT = "="
STATIC_VALUES_LIST_SEPERATION = " "
STATIC_VALUES_SEPERATION = ";"

def mark_key_in_line(line: str, key: str) -> TextMarkedSpan:
    if (not line.endswith(STATIC_LINE_ENDING)):
        raise ValueError(line)
    existing_key_start_index = line.find(key)
    if(existing_key_start_index == -1):
        #doesnt exist
        end_content_index = len(line) - len(STATIC_LINE_ENDING)
        extended_key_content = STATIC_VALUES_LIST_SEPERATION + key + STATIC_KEY_ASSIGNMENT
        span = TextMarkedSpan(line_content=line, content_to_insert=extended_key_content, start_index_to_mark=end_content_index, size_to_delete=0)
        return span
    else:
        #exists
        assignment_index = existing_key_start_index + len(key)
        end_char_of_key = assignment_index+len(STATIC_KEY_ASSIGNMENT)
        actual_assignment_string = line[assignment_index : end_char_of_key]
        if(actual_assignment_string != STATIC_KEY_ASSIGNMENT):
            raise AssertionError("Key exists, but it is not followed by assingment sign. Expected sign: " + STATIC_KEY_ASSIGNMENT)
        span = TextMarkedSpan(line_content=line, content_to_insert="", start_index_to_mark=existing_key_start_index, size_to_delete=0)
        return span

def set_value_to_span(marked_content: TextMarkedSpan, value: str) -> None:
    # First, we create new string with where existing value may be presented
    # It's range is from the end of the already marked span, to a STATIC_VALUES_LIST_SEPERATION
    index_to_cut_before = marked_content.start_index_to_mark + marked_content.size_to_delete
    line_content_cut_before = marked_content.line_content[index_to_cut_before:]
    index_to_cut_after = line_content_cut_before.find(STATIC_VALUES_LIST_SEPERATION)
    
    line_content_cut_before_and_after: str
    if(index_to_cut_after == -1):
        line_content_cut_before_and_after = line_content_cut_before
    else:
        line_content_cut_before_and_after = line_content_cut_before[:index_to_cut_after]
    
    # Search if value exists, if so just return since no changes are required
    if(line_content_cut_before_and_after.find(value) != -1):
        return
    else:
        is_there_value_after = len(line_content_cut_before_and_after) != 0
        element_suffix = ""
        if(is_there_value_after):
            element_suffix = STATIC_VALUES_SEPERATION

        marked_content.content_to_insert += value + element_suffix

def generate_new_line(marked_content: TextMarkedSpan) -> str:
    newline = marked_content.line_content[:marked_content.start_index_to_mark] + marked_content.content_to_insert + marked_content.line_content[marked_content.start_index_to_mark + marked_content.size_to_delete:]
    return newline