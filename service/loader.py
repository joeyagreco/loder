import os
from typing import Any, Optional
from enumeration.EnvVarSource import EnvVarSource
from model.EnvData import EnvData
from model.EnvVarMemory import EnvVarMemory

from model.Settings import Settings


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
