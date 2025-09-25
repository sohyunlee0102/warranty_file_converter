from model.driver_config.driver_configuration_dto import DriverConfigurationDto
from model.required_headers_dto import RequiredHeadersDto


def getRequiredHeaders(driverConfig: DriverConfigurationDto) -> RequiredHeadersDto:
    mbmuDriverConfig = driverConfig.MBMU
    sbmuDriverConfig = driverConfig.SBMU

    requiredMbmuHeaders: list[str] = []
    for key, value in mbmuDriverConfig.items():
        if isinstance(value, dict) and value.get("required") is True:
            requiredMbmuHeaders.append(key.upper())

    requiredSbmuHeaders: list[str] = []
    for key, value in sbmuDriverConfig.items():
        if isinstance(value, dict) and value.get("required") is True:
            requiredSbmuHeaders.append(key.upper())

    return RequiredHeadersDto(
        MBMU=requiredMbmuHeaders,
        SBMU=requiredSbmuHeaders,
    )
