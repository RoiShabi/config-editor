from typing import Any, Optional, Tuple


def parse_params(args: str) -> Tuple[str, str, str, Optional[str]]:
    # extract parameters

    params = dict(arg.split('=', 1) for arg in args)

    # Extract required values
    field = params.get("field")
    value = params.get("value")
    file_path = params.get("file")
    key_opt = params.get("key")  # optional

    # sanity checks: all must be non-empty strings (key may be None)
    def _check_str(name: str, val: Any):
        if not isinstance(val, str) or not val.strip():
            raise TypeError(f"'{name}' must be a non-empty string")

    _check_str('file', file_path)
    _check_str('field', field)
    _check_str('value', value)
    # _check_str('key', key_opt)    This is a comment since key field is optional

    return file_path, field, value, key_opt
