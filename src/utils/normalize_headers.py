import pandas as pd


def normalizeHeaders(dataFrame: pd.DataFrame) -> None:
    normalizedColumns = []
    for original in dataFrame.columns:
        converted = stripBrackets(original)
        normalizedColumns.append(converted.upper())
    dataFrame.columns = normalizedColumns


def stripBrackets(header: str) -> str:
    return str(header).strip("[]")
