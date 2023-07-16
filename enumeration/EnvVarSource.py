from __future__ import annotations

from enum import unique

from enumeration.BaseEnum import BaseEnum


@unique
class EnvVarSource(BaseEnum):
    CODE = "CODE"
    FILE = "FILE"
    OS = "OS"

    @staticmethod
    def items() -> list[tuple[EnvVarSource, str]]:
        return [(member, member.name) for member in EnvVarSource]

    @classmethod
    def from_str(cls, s: str) -> EnvVarSource:
        s_upper = s.upper()
        for member, member_name in EnvVarSource.items():
            if member_name == s_upper:
                return member
        raise ValueError(f"'{s}' is not a valid EnvVarSource.")
