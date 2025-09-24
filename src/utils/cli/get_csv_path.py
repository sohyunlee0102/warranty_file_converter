from file_manager.file_manager_service import FileManagerService


def getCsvPath() -> str:
    isPathReady: bool = False
    csvPath: str = ""
    fileManagerInstance: FileManagerService = FileManagerService()

    while not isPathReady:
        csvPath = promptCsvPath()
        isPathReady = fileManagerInstance.validatePath(csvPath)

    return csvPath


def promptCsvPath() -> str:
    return input("\nPlease provide the path to the CSV file: ")
