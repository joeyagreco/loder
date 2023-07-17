from loder.exception.DuplicateKeyException import DuplicateKeyException
from loder.model.EnvData import EnvData
from loder.model.Settings import Settings


class EnvVarMemory:
    """
    Used to store all env vars.
    """

    env_vars: dict[str, EnvData] = {}
    env_vars_unprocessed: dict[str, EnvData] = {}

    @classmethod
    def print(cls):
        print("\nPROCESSED\n____________")
        for key, val in cls.env_vars.items():
            print(f"{key}: {val}")
        if len(cls.env_vars) == 0:
            print("<empty>")
        print("\nUNPROCESSED\n____________")
        for key, val in cls.env_vars_unprocessed.items():
            print(f"{key}: {val}")
        if len(cls.env_vars_unprocessed) == 0:
            print("<empty>")

    @classmethod
    def get(cls, *, key: str) -> EnvData:
        return cls.env_vars[key]

    @classmethod
    def set(cls, *, key: str, env_data: EnvData, as_processed: bool = False) -> None:
        if as_processed:
            if not Settings.allow_env_var_key_override and key in cls.env_vars:
                raise DuplicateKeyException(f"Key '{key}' is already taken.")
            key = key if Settings.case_sensitive_keys else key.upper()
            cls.env_vars[key] = env_data
        else:
            cls.env_vars_unprocessed[key] = env_data

    @classmethod
    def process(cls) -> None:
        for key, env_data in cls.env_vars_unprocessed.items():
            cls.set(key=key, env_data=env_data, as_processed=True)
        cls.env_vars_unprocessed = {}

    @classmethod
    def reset(cls) -> None:
        cls.env_vars_unprocessed = {}
        cls.env_vars = {}
