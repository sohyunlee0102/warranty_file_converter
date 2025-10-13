from typing import Final

from model.catl_battery_models_enum import EBatteryModels
from utils.get_resource_path import getResourcePath

DRIVER_CONFIG_PATHS: Final = {
    EBatteryModels.EnerOne: getResourcePath("driver_configs/enerone.json"),
    EBatteryModels.EnerOnePlus: getResourcePath("driver_configs/enerone_plus.json"),
    EBatteryModels.EnerCPlus: getResourcePath("driver_configs/enerc_plus.json"),
    EBatteryModels.Wolong: getResourcePath("driver_configs/wolong.json"),
}
