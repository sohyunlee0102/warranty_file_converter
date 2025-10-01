"""Top-level package for warranty-converter-script.

Expose a small public API and package metadata here.
"""

from csv_converter.converter_service import ConverterService
from csv_validator.csv_validator_service import CsvValidatorService
from file_manager.file_manager_service import FileManagerService
from utils.cli.get_csv_path import getCsvPath
from utils.cli.get_driver_model import getDriverModel
from utils.get_driver_configuration import getDriverConfiguration
from utils.normalize_headers import normalizeHeaders


def processCsvFile():
    print("Starting CSV file processing...")
    fileManagerInstance = FileManagerService()

    csvPath = getCsvPath()
    csvData = fileManagerInstance.getCsvData(csvPath)
    print(f"Processing CSV file: {fileManagerInstance.getFileName(csvPath)}")

    driverModel = getDriverModel()
    print(f"Selected Driver Model: {driverModel.name}\n")

    normalizeHeaders(csvData)
    driverConfig = getDriverConfiguration(driverModel)

    fileValidatorInstance = CsvValidatorService(
        csvData,
        driverConfig,
    )
    fileValidatorInstance.validate(csvPath)

    converter = ConverterService(driverConfig)
    dataframeList = converter.convert(csvData)


if __name__ == "__main__":
    processCsvFile()
