import json

from model.catl_battery_models_enum import ECatlBatteryModels
from model.driver_config.driver_configuration_dto import DriverConfigurationDto
from model.driver_config.register_description_dto import (
    AlarmRegisterDescriptionDto,
    RegisterDescriptionDto,
    ValueRegisterDescriptionDto,
)
from utils.driver_config_path_const import DRIVER_CONFIG_PATHS


def _buildRegisterDescription(value: dict) -> RegisterDescriptionDto:
    if "alarmBitLength" in value or "alarmMap" in value:
        return AlarmRegisterDescriptionDto(
            required=value.get("required", False),
            targetColumn=value.get("targetColumn", ""),
            alarmBitLength=value.get("alarmBitLength", 0),
            alarmMap=value.get("alarmMap", {}),
        )
    if "offset" in value or "conversionFactor" in value:
        return ValueRegisterDescriptionDto(
            required=value.get("required", False),
            targetColumn=value.get("targetColumn", ""),
            offset=value.get("offset", 0),
            conversionFactor=value.get("conversionFactor", 1.0),
        )

    return RegisterDescriptionDto(
        required=value.get("required", False),
        targetColumn=value.get("targetColumn", ""),
    )


def getDriverConfiguration(driverModel: ECatlBatteryModels) -> DriverConfigurationDto:
    configPath = DRIVER_CONFIG_PATHS.get(driverModel)

    if not configPath:
        raise ValueError(
            f"❌ No configuration path found for driver model: {driverModel}"
        )

    with open(configPath, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Build MBMU and SBMU maps into DTO instances
    mbmuJsonData = data.get("MBMU", {}) or {}
    sbmuJsonData = data.get("SBMU", {}) or {}

    mbmu: dict[str, RegisterDescriptionDto] = {}
    for key, value in mbmuJsonData.items():
        mbmu[key] = _buildRegisterDescription(value)

    sbmu: dict[str, RegisterDescriptionDto] = {}
    for key, value in sbmuJsonData.items():
        sbmu[key] = _buildRegisterDescription(value)

    return DriverConfigurationDto(
        timeMaxIntervalInSeconds=data.get("timeMaxIntervalInSeconds", 0),
        MBMU=mbmu,
        SBMU=sbmu,
    )
