from model.driver_config.driver_configuration_dto import DriverConfigurationDto
from model.driver_config.register_description_dto import RegisterDescriptionDto
from model.required_headers_dto import RequiredHeadersDto


def getRequiredHeaders(driverConfig: DriverConfigurationDto) -> RequiredHeadersDto:
    mbmuDriverConfig = driverConfig.MBMU
    sbmuDriverConfig = driverConfig.SBMU

    requiredMbmuHeaders: list[str] = []
    for key, value in mbmuDriverConfig.items():
        if isinstance(value, RegisterDescriptionDto) and value.required is True:
            if getattr(value, "sourceAliases", None):
                for alias in value.sourceAliases:
                    requiredMbmuHeaders.append(alias.upper())
            else:
                requiredMbmuHeaders.append(key.upper())

    requiredSbmuHeaders: list[str] = []
    for key, value in sbmuDriverConfig.items():
        if isinstance(value, RegisterDescriptionDto) and value.required is True:
            if getattr(value, "sourceAliases", None):
                for alias in value.sourceAliases:
                    requiredSbmuHeaders.append(alias.upper())
            else:
                requiredSbmuHeaders.append(key.upper())

    return RequiredHeadersDto(
        MBMU=requiredMbmuHeaders,
        SBMU=requiredSbmuHeaders,
    )
