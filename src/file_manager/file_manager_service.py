import os

import pandas as pd


class FileManagerService:
    def validatePath(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            print(f"❌ Path does not exist: {file_path}")
            return False
        if not os.path.isfile(file_path):
            print(f"❌ Not a file: {file_path}")
            return False
        if not os.access(file_path, os.R_OK):
            print(f"❌ Cannot read file (permission denied): {file_path}")
            return False
        return True

    def getFileName(self, file_path: str) -> str:
        return os.path.basename(file_path)

    def getCsvData(self, csvPath: str) -> pd.DataFrame:
        data = pd.read_csv(csvPath)
        data = data.fillna("")

        return data
