"""Top-level package for warranty-converter-script.

Expose a small public API and package metadata here.
"""

import os
import time
from pathlib import Path

from csv_converter.converter_service import ConverterService
from csv_validator.csv_validator_service import CsvValidatorService
from file_manager.file_manager_service import FileManagerService
from utils.cli.get_driver_model import getDriverModel
from utils.cli.get_file_path import getPath
from utils.get_driver_configuration import getDriverConfiguration
from utils.multi_file_processor import MultiFileProcessor
from utils.normalize_headers import normalizeHeaders


def processCsvFile():
    print("Starting CSV/Excel file processing...")
    fileManagerInstance = FileManagerService()

    inputPath = getPath()
    fileList = []

    if os.path.isdir(inputPath):
        for extension in ("*.csv", "*.xlsx", "*.xls", "*.xlsm"):
            for filePath in Path(inputPath).glob(extension):
                fileName = filePath.name.lower()
                if not fileName.startswith("~$") and "_converted" not in fileName:
                    fileList.append(str(filePath))
        if not fileList:
            print("❌ No CSV/Excel files found in the folder.")
            return
    elif os.path.isfile(inputPath):
        fileList = [inputPath]
    else:
        print(f"❌ Invalid path: {inputPath}")
        return

    processor = MultiFileProcessor(fileManagerInstance, pauseOnError=True)
    processor.processFiles(fileList)


if __name__ == "__main__":
    try:
        processCsvFile()
    except KeyboardInterrupt:
        input("\nPress Enter to exit...")
    except Exception as e:
        input("Press Enter to exit...")
    except SystemExit:
        raise
