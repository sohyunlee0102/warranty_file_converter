from typing import Final

from model.catl_battery_models_enum import ECatlBatteryModels

DRIVER_CONFIG_PATHS: Final = {
    ECatlBatteryModels.EnerOne: "driver_configs/enerone.json",
    ECatlBatteryModels.EnerOnePlus: "driver_configs/enerone_plus.json",
    ECatlBatteryModels.EnerCPlus: "driver_configs/enerc_plus.json",
}
