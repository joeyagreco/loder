from typing import Any
from exception.DuplicateKeyException import DuplicateKeyException

from model.Settings import Settings


class EnvVars:
    """
    Used to store all env vars.
    """

    env_vars = {}

    def get(cls, *, key: str) -> Any:
        return cls.env_vars[key]

    def set(cls, *, key: str, value: Any) -> None:
        if not Settings.allow_override and key in cls.env_vars:
            raise DuplicateKeyException(f"Key '{key}' is already taken.")
        cls.env_vars[key] = value
