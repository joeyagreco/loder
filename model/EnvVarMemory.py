from exception.DuplicateKeyException import DuplicateKeyException
from model.EnvData import EnvData

from model.Settings import Settings


class EnvVarMemory:
    """
    Used to store all env vars.
    """

    env_vars: dict[str, EnvData] = {}

    @classmethod
    def print(cls):
        for key, val in cls.env_vars.items():
            print(f"{key}: {val}")
        # env_vars_pretty = [f"{key}: {val}\n" for key, val in cls.env_vars.items()]
        # print(f"EnvVarMemory(env_vars={env_vars_pretty}")

    @classmethod
    def get(cls, *, key: str) -> EnvData:
        return cls.env_vars[key]

    @classmethod
    def set(cls, *, key: str, env_data: EnvData) -> None:
        if not Settings.allow_env_var_key_override and key in cls.env_vars:
            raise DuplicateKeyException(f"Key '{key}' is already taken.")
        key = key if Settings.case_sensitive_keys else key.upper()
        cls.env_vars[key] = env_data
