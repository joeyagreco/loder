from typing import Any


class EnvData:
    
    def __init__(self, value: Any, description: str = ""):
        self.value = value
        self.description = description