import json
from typing import Any

from model.catl_battery_models_enum import ECatlBatteryModels
from utils.driver_config_path_const import DRIVER_CONFIG_PATHS


def getDriverConfiguration(driverModel: ECatlBatteryModels) -> dict[str, Any]:
    configPath = DRIVER_CONFIG_PATHS.get(driverModel)

    if not configPath:
        raise ValueError(
            f"❌ No configuration path found for driver model: {driverModel}"
        )

    with open(configPath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data
