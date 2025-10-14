import math
from typing import Any

from model.catl_battery_models_enum import EBatteryModels


def getDriverModel() -> EBatteryModels:
    isValidModel: bool = False
    driverModel: str | Any = math.nan
    while not isValidModel:
        driverModel = promptDriverModel()
        try:
            EBatteryModels(int(driverModel))
            isValidModel = True
        except ValueError:
            print("❌ Invalid option. Please choose a valid driver model.")
    return EBatteryModels(int(driverModel))


def promptDriverModel() -> str:
    print("\nPlease provide the driver model: ")

    for model in EBatteryModels:
        print(f"\t {model.value}. {model.name}")

    return input("Choose an option (1-4): ").strip()
