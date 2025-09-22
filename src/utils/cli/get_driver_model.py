import math
from typing import Any

from model.catl_battery_models_enum import ECatlBatteryModels


def getDriverModel() -> ECatlBatteryModels:
    isValidModel: bool = False
    driverModel: str | Any = math.nan
    while not isValidModel:
        driverModel = promptDriverModel()
        try:
            ECatlBatteryModels(int(driverModel))
            isValidModel = True
        except ValueError:
            print("❌ Invalid option. Please choose a valid driver model.\n")
    return ECatlBatteryModels(int(driverModel))


def promptDriverModel() -> str:
    print("Please provide the driver model:")

    for model in ECatlBatteryModels:
        print(f"\t {model.value}. {model.name}")

    return input("Choose an option (1-3): ").strip()
