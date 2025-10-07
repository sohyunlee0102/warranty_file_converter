from typing import Final

from model.catl_battery_models_enum import ECatlBatteryModels
from utils.get_resource_path import getResourcePath

DRIVER_CONFIG_PATHS: Final = {
    ECatlBatteryModels.EnerOne: getResourcePath("driver_configs/enerone.json"),
    ECatlBatteryModels.EnerOnePlus: getResourcePath("driver_configs/enerone_plus.json"),
    ECatlBatteryModels.EnerCPlus: getResourcePath("driver_configs/enerc_plus.json"),
}
