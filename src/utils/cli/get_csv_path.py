from file_manager.file_manager_service import FileManagerService


def getCsvPath() -> str:
    isPathReady: bool = False
    csv_path: str = ""
    fileManagerInstance: FileManagerService = FileManagerService()

    while not isPathReady:
        csv_path = promptCsvPath()
        isPathReady = fileManagerInstance.validatePath(csv_path)

    return csv_path


def promptCsvPath() -> str:
    RAW_PATH = input("\nPlease provide the path to the CSV file: ")
    return RAW_PATH
