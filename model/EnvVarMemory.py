from exception.DuplicateKeyException import DuplicateKeyException
from model.EnvData import EnvData

from model.Settings import Settings


class EnvVarMemory:
    """
    Used to store all env vars.
    """

    env_vars: dict[str, EnvData] = {}

    def get(cls, *, key: str) -> EnvData:
        return cls.env_vars[key]

    def set(cls, *, key: str, env_data: EnvData) -> None:
        if not Settings.allow_env_var_key_override and key in cls.env_vars:
            raise DuplicateKeyException(f"Key '{key}' is already taken.")
        cls.env_vars[key] = env_data
