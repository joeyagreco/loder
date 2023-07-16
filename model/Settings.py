from typing import Optional


class Settings:
    allow_env_var_key_override: bool = (
        True  # whether or not to allow env var keys to be overwritten
    )
    case_sensitive_keys: bool = False  # whether or not keys should be case sensitive
    load_env_vars_from_os: bool = True  # whether or not to load env vars from the OS
    os_env_prefix: Optional[
        str
    ] = None  # the case-sensitive prefix to filter on when loading env vars from the OS
