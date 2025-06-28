from typing import Any, Optional, Tuple
from dataclasses import dataclass


DEFAULT_DELIMITER = ","

@dataclass
class ScriptConfiguration:
    file_path:str
    field: str
    value:str
    delimiter: str
    key: Optional[str]
    accept: Optional[bool]

def check_help_params(argv: str) -> bool:
    if(len(argv) != 1):
        return False
    
    return argv[0].strip() == "--help"

def parse_params(argv: list[str]) -> ScriptConfiguration:
    # extract parameters

    params = dict(arg.split('=', 1) for arg in argv)

    # Extract required values
    field = params.get("field")
    value = params.get("value")
    file_path = params.get("file")
    key_opt = params.get("key")  # optional
    accept_opt = params.get("accept")
    delimiter_opt = params.get("delimiter")  # if not exist 

    # sanity checks: all must be non-empty strings (key may be None)
    def _check_str(name: str, val: Any):
        if not isinstance(val, str) or not val.strip():
            raise TypeError(f"'{name}' must be a non-empty string")

    _check_str('file', file_path)
    _check_str('field', field)
    _check_str('value', value)
    # _check_str('key', key_opt)    This is a comment since key field is optional

    if(not isinstance(delimiter_opt, str) or not delimiter_opt.strip()):
        delimiter_opt = DEFAULT_DELIMITER
    
    return ScriptConfiguration(file_path=file_path, field=field, value=value,key=key_opt,
                               delimiter=delimiter_opt, accept=accept_opt)
