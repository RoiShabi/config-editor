#!/usr/bin/env python3

import sys
from params_parse import parse_params

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

if __name__ == "__main__":
    main()
