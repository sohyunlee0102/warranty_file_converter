import os
import time
from pathlib import Path

from csv_converter.converter_service import ConverterService
from csv_validator.csv_validator_service import CsvValidatorService
from utils.cli.get_driver_model import getDriverModel
from utils.get_driver_configuration import getDriverConfiguration
from utils.normalize_headers import normalizeHeaders


class MultiFileProcessor:
    def __init__(self, fileManagerInstance):
        self.fileManagerInstance = fileManagerInstance

    def processFiles(self, fileList: list[str]):
        print(f"\n🔁 Starting batch conversion for {len(fileList)} files ...")

        for filePath in fileList:
            try:
                self._process_single_file(filePath)
            except Exception as e:
                print(f"❌ Failed to process {filePath}: {e}")

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
