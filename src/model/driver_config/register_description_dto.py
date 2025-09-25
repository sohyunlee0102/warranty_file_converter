from dataclasses import dataclass


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
