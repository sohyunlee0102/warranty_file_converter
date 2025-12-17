import json
import os
import sys

from model.catl_battery_models_enum import EBatteryModels
from model.driver_config.driver_configuration_dto import DriverConfigurationDto
from model.driver_config.register_description_dto import (
    AlarmRegisterDescriptionDto,
    RegisterDescriptionDto,
    StatusRegisterDescriptionDto,
    ValueRegisterDescriptionDto,
)
from utils.driver_config_path_const import DRIVER_CONFIG_PATHS


def _buildRegisterDescription(value: dict) -> RegisterDescriptionDto:
    targetColumn = value.get("targetColumn", "")
    if not targetColumn:
        raise ValueError(
            "Target column description not found in the register information"
        )

    if "alarmBitLength" in value or "alarmMap" in value:
        return AlarmRegisterDescriptionDto(
            required=value.get("required", False),
            targetColumn=targetColumn,
            sourceAliases=value.get("sourceAliases", None),
            alarmBitLength=value.get("alarmBitLength", 1),
            alarmMap=value.get("alarmMap", {}),
        )
    if "offset" in value or "conversionFactor" in value:
        return ValueRegisterDescriptionDto(
            required=value.get("required", False),
            targetColumn=targetColumn,
            sourceAliases=value.get("sourceAliases", None),
            offset=value.get("offset", 0),
            conversionFactor=value.get("conversionFactor", 1.0),
        )

    if "status" in value or "bitmask" in value:
        return StatusRegisterDescriptionDto(
            required=value.get("required", False),
            targetColumn=targetColumn,
            sourceAliases=value.get("sourceAliases", None),
            status=value.get("status"),
            bitmask=value.get("bitmask"),
        )

    return RegisterDescriptionDto(
        required=value.get("required", False),
        targetColumn=targetColumn,
        sourceAliases=value.get("sourceAliases", None),
    )


def getDriverConfiguration(driverModel: EBatteryModels) -> DriverConfigurationDto:
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

    def _applyAliases(mappingList: dict[str, RegisterDescriptionDto]):
        additions: dict[str, RegisterDescriptionDto] = {}
        for registerKey, registerDescription in mappingList.items():
            aliases = getattr(registerDescription, "sourceAliases", None)
            if aliases:
                for alias in aliases:
                    aliasKey = alias.upper()
                    if aliasKey not in mappingList:
                        additions[aliasKey] = registerDescription
        mappingList.update(additions)

    _applyAliases(mbmu)
    _applyAliases(sbmu)

    return DriverConfigurationDto(
        timeMaxIntervalInSeconds=data.get("timeMaxIntervalInSeconds", 0),
        MBMU=mbmu,
        SBMU=sbmu,
    )
