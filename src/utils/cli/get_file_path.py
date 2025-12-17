import os

from file_manager.file_manager_service import FileManagerService


def getPath() -> str:
    isPathReady: bool = False
    inputPath: str = ""
    fileManagerInstance: FileManagerService = FileManagerService()

    while not isPathReady:
        inputPath = promptFilePath()

        if (inputPath.startswith('"') and inputPath.endswith('"')) or (
            inputPath.startswith("'") and inputPath.endswith("'")
        ):
            inputPath = inputPath[1:-1]

        if os.path.isdir(inputPath):
            isPathReady = True
        elif fileManagerInstance.validatePath(inputPath):
            isPathReady = True
        else:
            print("❌ Invalid path. Please enter a valid file or folder path.")
            continue

    return inputPath


def promptFilePath() -> str:
    return input("\nPlease provide the path to the CSV/Excel file or folder: ")
