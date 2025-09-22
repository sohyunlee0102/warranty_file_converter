"""Top-level package for warranty-converter-script.

Expose a small public API and package metadata here.
"""

from file_manager.file_manager_service import FileManagerService
from utils.cli.get_csv_path import getCsvPath
from utils.cli.get_driver_model import getDriverModel


def processCsvFile():
    print("Starting CSV file processing...")
    fileManagerInstance = FileManagerService()

    csvPath = getCsvPath()
    csvData = fileManagerInstance.getCsvData(csvPath)
    print(f"Processing CSV file: {fileManagerInstance.getFileName(csvPath)}")

    driverModel = getDriverModel()
    print(f"Selected Driver Model: {driverModel.name}\n")

    # 3. Validate CSV format
    # 4. Add logic to process the CSV file here
    # 5. Create xlsx file


if __name__ == "__main__":
    processCsvFile()
