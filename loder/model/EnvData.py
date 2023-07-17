from __future__ import annotations
from typing import Any

from loder.enumeration.EnvVarSource import EnvVarSource


class EnvData:
    def __init__(
        self,
        *,
        value: Any,
        description: str = "",
        env_var_source: EnvVarSource,
        as_type: type = str,
    ):
        self.as_type = as_type
        self.description = description
        self.env_var_source = env_var_source
        self.value = value

    def __eq__(self, other: EnvData) -> bool:
        equal = self.value = other.value
        equal = equal and self.description == other.description
        equal = equal and self.env_var_source == other.env_var_source
        equal = equal and self.as_type == other.as_type
        return equal

    def __str__(self):
        return f"EnvData(value={self.value}, as_type={self.as_type}, description='{self.description}', env_var_source={self.env_var_source.value})"

    def __repr__(self):
        return self.__str__()
