from typing import Optional


class Settings:
    __DEFAULTS = {
        "allow_env_var_key_override": True,
        "case_sensitive_keys": False,
        "env_var_absolute_file_paths": [],
        "load_env_vars_from_files": True,
        "load_env_vars_from_os": True,
        "os_env_prefix": None,
    }
    allow_env_var_key_override: bool = __DEFAULTS[
        "allow_env_var_key_override"
    ]  # whether or not to allow env var keys to be overwritten
    case_sensitive_keys: bool = __DEFAULTS[
        "case_sensitive_keys"
    ]  # whether or not keys should be case sensitive
    env_var_absolute_file_paths: list[str] = __DEFAULTS[
        "env_var_absolute_file_paths"
    ]  # a list of all of the paths to env var files
    load_env_vars_from_files: bool = __DEFAULTS[
        "load_env_vars_from_files"
    ]  # whether or not to load env vars from files (does not include .env files)
    load_env_vars_from_os: bool = __DEFAULTS[
        "load_env_vars_from_os"
    ]  # whether or not to load env vars from the OS
    os_env_prefix: Optional[str] = __DEFAULTS[
        "os_env_prefix"
    ]  # the case-sensitive prefix to filter on when loading env vars from the OS

    @classmethod
    def reset(cls) -> None:
        cls.allow_env_var_key_override: bool = cls.__DEFAULTS["allow_env_var_key_override"]
        cls.case_sensitive_keys: bool = cls.__DEFAULTS["case_sensitive_keys"]
        cls.env_var_absolute_file_paths: list[str] = cls.__DEFAULTS["env_var_absolute_file_paths"]
        cls.load_env_vars_from_files: bool = cls.__DEFAULTS["load_env_vars_from_files"]
        cls.load_env_vars_from_os: bool = cls.__DEFAULTS["load_env_vars_from_os"]
        cls.os_env_prefix: Optional[str] = cls.__DEFAULTS["os_env_prefix"]
