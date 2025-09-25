from model.driver_config.driver_configuration_dto import DriverConfigurationDto
from model.driver_config.register_description_dto import RegisterDescriptionDto


def getRequiredHeaders(driverConfig: DriverConfigurationDto) -> dict[str, list[str]]:
    mbmuDriverConfig = driverConfig.MBMU
    sbmuDriverConfig = driverConfig.SBMU

    requiredMbmuHeaders: list[str] = []
    for key, value in mbmuDriverConfig.items():
        if isinstance(value, RegisterDescriptionDto) and value.required is True:
            requiredMbmuHeaders.append(key.upper())

    requiredSbmuHeaders: list[str] = []
    for key, value in sbmuDriverConfig.items():
        if isinstance(value, RegisterDescriptionDto) and value.required is True:
            requiredSbmuHeaders.append(key.upper())

    return {
        "MBMU": requiredMbmuHeaders,
        "SBMU": requiredSbmuHeaders,
    }
