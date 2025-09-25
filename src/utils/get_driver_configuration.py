import json

from model.catl_battery_models_enum import ECatlBatteryModels
from model.driver_config.driver_configuration_dto import DriverConfigurationDto
from utils.driver_config_path_const import DRIVER_CONFIG_PATHS


def getDriverConfiguration(driverModel: ECatlBatteryModels) -> DriverConfigurationDto:
    configPath = DRIVER_CONFIG_PATHS.get(driverModel)

    if not configPath:
        raise ValueError(
            f"❌ No configuration path found for driver model: {driverModel}"
        )

    with open(configPath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data
