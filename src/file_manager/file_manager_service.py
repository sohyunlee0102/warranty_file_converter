import os

import pandas as pd


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

    def getCsvData(self, csvPath: str) -> pd.DataFrame:
        data = pd.read_csv(csvPath)

        return data
