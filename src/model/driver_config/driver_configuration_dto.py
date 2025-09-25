from dataclasses import dataclass

from model.driver_config.register_description_dto import (
    AlarmRegisterDescriptionDto,
    ValueRegisterDescriptionDto,
)


@dataclass
class DriverConfigurationDto:
    timeMaxIntervalInSeconds: int
    MBMU: dict[str, ValueRegisterDescriptionDto | AlarmRegisterDescriptionDto]
    SBMU: dict[str, ValueRegisterDescriptionDto | AlarmRegisterDescriptionDto]
