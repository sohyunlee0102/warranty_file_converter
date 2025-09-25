"""Top-level package for warranty-converter-script.

Expose a small public API and package metadata here.
"""

from csv_validator.csv_validator_service import CsvValidatorService
from file_manager.file_manager_service import FileManagerService
from utils.cli.get_csv_path import getCsvPath
from utils.cli.get_driver_model import getDriverModel
from utils.get_driver_configuration import getDriverConfiguration
from utils.get_number_of_strings import getNumberOfStrings
from utils.get_required_headers import getRequiredHeaders
from utils.normalize_headers import normalizeHeaders


def processCsvFile():
    print("Starting CSV file processing...")
    fileManagerInstance = FileManagerService()

    csvPath = getCsvPath()
    csvData = fileManagerInstance.getCsvData(csvPath)
    normalizeHeaders(csvData)
    print(f"Processing CSV file: {fileManagerInstance.getFileName(csvPath)}")

    driverModel = getDriverModel()
    print(f"Selected Driver Model: {driverModel.name}\n")

    driverConfig = getDriverConfiguration(driverModel)
    requiredHeaders = getRequiredHeaders(driverConfig)
    numberOfStrings = getNumberOfStrings(csvData)

    fileValidatorInstance = CsvValidatorService(
        requiredHeaders,
        csvData,
        numberOfStrings,
        driverConfig.timeMaxIntervalInSeconds,
    )
    fileValidatorInstance.validate(csvPath)

    # 4. Add logic to process the CSV file here
    # 5. Create xlsx file


if __name__ == "__main__":
    processCsvFile()
