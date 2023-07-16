from typing import Any

from enumeration.EnvVarSource import EnvVarSource


class EnvData:
    def __init__(
        self,
        *,
        value: Any,
        description: str = "",
        env_var_source: EnvVarSource,
        as_type: type = str
    ):
        self.as_type = as_type
        self.description = description
        self.env_var_source = env_var_source
        self.value = value
