import os
import re
import time
from pathlib import Path

from pandas.errors import ParserError

from csv_converter.converter_service import ConverterService
from csv_validator.csv_validator_service import CsvValidatorService
from utils.cli.get_driver_model import getDriverModel
from utils.get_driver_configuration import getDriverConfiguration
from utils.normalize_headers import normalizeHeaders


class MultiFileProcessor:
    def __init__(
        self,
        fileManagerInstance,
        pauseOnError: bool = True,
        pauseMessage: str = "Press Enter to continue...",
    ):
        self.fileManagerInstance = fileManagerInstance
        self.pauseOnError = pauseOnError
        self.pauseMessage = pauseMessage

    def processFiles(self, fileList: list[str]):
        print(f"\n🔁 Starting batch conversion for {len(fileList)} files ...")

        for filePath in fileList:
            try:
                self._process_single_file(filePath)
            except Exception as e:
                self._print_user_friendly_error(filePath, e)

    def _process_single_file(self, filePath: str):
        fileManagerInstance = self.fileManagerInstance
        fileName = os.path.basename(filePath)

        if "_converted" in Path(fileName).stem.lower():
            return

        fileData = fileManagerInstance.getOriginalData(filePath)

        driverModel = getDriverModel()
        print(f"Selected Driver Model: {driverModel.name}\n")

        start = time.time()
        normalizeHeaders(fileData)
        driverConfig = getDriverConfiguration(driverModel)

        fileValidatorInstance = CsvValidatorService(fileData, driverConfig)
        fileValidatorInstance.validate(filePath)

        converter = ConverterService(driverConfig)
        dataframeList = converter.convert(fileData)
        fileManagerInstance.saveXlsx(filePath, start, dataframeList)

    def _print_user_friendly_error(self, filePath: str, e: Exception):
        rawException = str(e)

        print(f"\n❌ Failed to process {filePath}")

        if isinstance(e, ParserError) or "Error tokenizing data" in rawException:
            message = re.search(
                r"Expected (\d+) fields in line (\d+), saw (\d+)", rawException
            )
            if message:
                expectedValues, lineNumber, actualValues = message.groups()
                print(
                    f"CSV formatting error - line {lineNumber} has {actualValues} columns instead of {expectedValues}.\n"
                )
            else:
                print(
                    "CSV formatting error - one of the rows has an invalid structure.\n"
                )
            if getattr(self, "pauseOnError", False):
                try:
                    input(self.pauseMessage)
                except Exception:
                    pass
            return

        if isinstance(e, FileNotFoundError):
            print("File not found - please check the file path.\n")
            if getattr(self, "pauseOnError", False):
                try:
                    input(self.pauseMessage)
                except Exception:
                    pass
            return

        if isinstance(e, PermissionError) or "Permission denied" in rawException:
            print("Permission issue - file or folder is read-only or restricted.\n")
            if getattr(self, "pauseOnError", False):
                try:
                    input(self.pauseMessage)
                except Exception:
                    pass
            return

        if (
            isinstance(e, UnicodeDecodeError)
            or "codec can't decode" in rawException.lower()
        ):
            print("Encoding error - please save the file as UTF-8 and try again.\n")
            if getattr(self, "pauseOnError", False):
                try:
                    input(self.pauseMessage)
                except Exception:
                    pass
            return

        if (
            "validation" in rawException.lower()
            or "required column" in rawException.lower()
        ):
            print(
                "CSV validation failed - file does not match the required template.\n"
            )
            if getattr(self, "pauseOnError", False):
                try:
                    input(self.pauseMessage)
                except Exception:
                    pass
            return

        print(f"{rawException}\n")
        if getattr(self, "pauseOnError", False):
            try:
                input(self.pauseMessage)
            except Exception:
                pass
