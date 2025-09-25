from dataclasses import dataclass

from model.driver_config.register_description_dto import RegisterDescriptionDto


@dataclass
class DriverConfigurationDto:
    timeMaxIntervalInSeconds: int
    MBMU: dict[str, RegisterDescriptionDto]
    SBMU: dict[str, RegisterDescriptionDto]
