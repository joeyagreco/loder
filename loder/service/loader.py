import json
import yaml
import os
from typing import Any, Optional
from loder.enumeration.EnvVarSource import EnvVarSource
from loder.model.EnvData import EnvData
from loder.model.EnvVarMemory import EnvVarMemory

from loder.model.Settings import Settings
from dotenv import load_dotenv


def define(
    key: str, as_type: type, default_value: Optional[Any] = None, description: str = ""
) -> None:
    """
    Define an ENV var in code.
    """
    # validation
    if default_value and type(default_value) != as_type:
        # TODO: this does not play nice with complex generic types like: dict[str, int]
        raise TypeError(
            f"Expected key '{key}' to be of type '{as_type}'. Received default value of type '{type(default_value)}'"
        )
    EnvVarMemory.set(
        key=key,
        env_data=EnvData(
            as_type=as_type,
            description=description,
            env_var_source=EnvVarSource.CODE,
            value=default_value,
        ),
    )


def __load_env_vars_from_os(as_processed: bool = False) -> None:
    if Settings.load_env_vars_from_os:
        load_dotenv()
        env_vars = os.environ

        for key, value in env_vars.items():
            # if no prefix set, load all vars
            # if prefix set, only load vars with that prefix + "_"
            if Settings.os_env_prefix and not key.startswith(f"{Settings.os_env_prefix}_"):
                continue

            EnvVarMemory.set(
                key=key.removeprefix(f"{Settings.os_env_prefix}_"),
                env_data=EnvData(env_var_source=EnvVarSource.OS, value=value),
                as_processed=as_processed,
            )


def __load_env_vars_from_files(as_processed: bool = False) -> None:
    env_var_dicts: list[dict[str, Any]] = []
    for file_path in Settings.env_var_absolute_file_paths:
        _, ext = os.path.splitext(file_path)

        if ext == ".json":
            with open(file_path, "r") as f:
                env_var_dicts.append(json.load(f))
        elif ext in [".yaml", ".yml"]:
            with open(file_path, "r") as f:
                env_var_dicts.append(yaml.safe_load(f))
        else:
            raise ValueError(f"Unsupported file type {ext}")

    for env_var_dict in env_var_dicts:
        for key, value in env_var_dict.items():
            EnvVarMemory.set(
                key=key,
                env_data=EnvData(
                    env_var_source=EnvVarSource.FILE, value=value, as_type=type(value)
                ),
                as_processed=as_processed,
            )


def __load_all_env_vars(as_processed: bool = False) -> None:
    if Settings.load_env_vars_from_os:
        __load_env_vars_from_os(as_processed)
    if Settings.load_env_vars_from_files:
        __load_env_vars_from_files(as_processed)


def process():
    """
    The env vars loaded last will overwrite the env vars loaded first.

    Load Order:
        1. OS
        2. File
        3. CODE

    Meaning Code will overwrite File and File will overwrite OS.
    """
    __load_all_env_vars(as_processed=True)
    EnvVarMemory.process()


def reset():
    EnvVarMemory.reset()
