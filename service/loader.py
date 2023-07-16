from typing import Any, Optional


def define(
    key: str, as_type: type, default_value: Optional[Any] = None, description: str = ""
) -> None:
    # validation
    if default_value and type(default_value) != as_type:
        raise TypeError(
            f"Expected key '{key}' to be of type '{as_type}'. Received default value of type '{type(default_value)}'"
        )

