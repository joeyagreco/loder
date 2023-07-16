from typing import Any

from enumeration.EnvVarSource import EnvVarSource


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

    def __str__(self):
        return f"EnvData(value={self.value}, description='{self.description}', env_var_source={self.env_var_source.value}, as_type={self.as_type})"

    def __repr__(self):
        return self.__str__()
