import os
from pathlib import Path
from time import time

from pandas import DataFrame, ExcelWriter, read_csv, read_excel
from tqdm import tqdm

INVALID_CHARS = r'<>:"/\\|?*'


class FileManagerService:
    def validatePath(self, filePath: str) -> bool:
        if not os.path.exists(filePath):
            print(f"❌ Path does not exist: {filePath}")
            return False
        if not os.path.isfile(filePath):
            print(f"❌ Not a file: {filePath}")
            return False
        if not os.access(filePath, os.R_OK):
            print(f"❌ Cannot read file (permission denied): {filePath}")
            return False
        return True

    def getFileName(self, filePath: str) -> str:
        return os.path.basename(filePath)

    def getOriginalData(self, filePath: str) -> DataFrame:
        extension = Path(filePath).suffix.lower()
        print(f"📂 Reading CSV/Excel file: {filePath} ...")
        start = time()

        if extension.endswith(".csv"):
            data = read_csv(filePath)
        elif extension in {".xlsx", ".xls", ".xlsm"}:
            data = read_excel(filePath, engine="openpyxl")

        end = time()
        print(f"✅ File read in {(end - start):4f}s")

        return data

    def saveXlsx(self, csvPath, start, dataframeList):
        filename = Path(self.getFileName(csvPath))
        newFileName = filename.stem + "_converted.xlsx"

        self.__validateFileName(newFileName)

        writingProgressBar = tqdm(
            total=len(dataframeList), desc="Writing Excel sheets", leave=False
        )
        with ExcelWriter(newFileName) as writer:
            for dataFrame in dataframeList:
                dataFrame.to_excel(writer, index=False, sheet_name=dataFrame.Name)
                writingProgressBar.update(1)

        end = time()
        writingProgressBar.write(
            f"✅ Conversion finalized. Process took {end - start:.4f} seconds"
        )
        writingProgressBar.clear()
        writingProgressBar.close()
        writingProgressBar.refresh()

    def __validateFileName(self, newFileName):
        isReadyToWrite = self.__validateOutputPath(newFileName)
        while not isReadyToWrite:
            fileNameInput = input(
                "Please provide a valid output path or press enter to keep the previous value: "
            ).strip()
            if not fileNameInput:
                fileNameInput = newFileName

            isReadyToWrite = self.__validateOutputPath(fileNameInput)

    def __validateOutputPath(self, outputPath: str) -> bool:
        directory = os.path.dirname(outputPath) or "."
        if any(ch in outputPath for ch in INVALID_CHARS):
            print(f"❌ Invalid character in filename: {outputPath}")
            return False
        if not os.path.exists(directory):
            print(f"❌ Directory does not exist: {directory}")
            return False
        if not os.access(directory, os.W_OK):
            print(f"❌ Cannot write to directory (permission denied): {directory}")
            return False
        try:
            with open(outputPath, "a"):  # "a" = append (creates file if missing)
                pass
        except PermissionError:
            print(
                f"❌ Cannot write to file (locked, opened or permission denied): {outputPath}"
            )
            return False
        except OSError as error:
            print(f"❌ Invalid file path or OS error: {error}")
            return False

        return True
