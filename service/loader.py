import json
import yaml
import os
from typing import Any, Optional
from enumeration.EnvVarSource import EnvVarSource
from model.EnvData import EnvData
from model.EnvVarMemory import EnvVarMemory

from model.Settings import Settings
from dotenv import load_dotenv


def define_env_var(
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


def load_env_vars_from_os() -> None:
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
            )


def load_env_vars_from_files() -> None:
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
            )
