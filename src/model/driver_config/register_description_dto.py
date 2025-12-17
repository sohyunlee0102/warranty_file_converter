from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RegisterDescriptionDto:
    required: bool
    targetColumn: str
    sourceAliases: Optional[List[str]] = field(default=None, kw_only=True)


@dataclass
class ValueRegisterDescriptionDto(RegisterDescriptionDto):
    offset: int
    conversionFactor: float


@dataclass
class AlarmRegisterDescriptionDto(RegisterDescriptionDto):
    alarmBitLength: int
    alarmMap: dict[str, dict[str, str]]


@dataclass
class StatusRegisterDescriptionDto(RegisterDescriptionDto):
    status: Optional[dict[str, str]]
    bitmask: Optional[dict[str, str]]
