from dataclasses import dataclass
from typing import Optional


@dataclass
class RegisterDescriptionDto:
    required: bool
    targetColumn: str


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
