import re

import pandas as pd


def normalizeHeaders(dataFrame: pd.DataFrame) -> None:
    normalizedColumns = []
    for original in dataFrame.columns:
        converted = stripBracketsAndHexPrefix(original)
        normalizedColumns.append(converted.upper())
    dataFrame.columns = normalizedColumns


def stripBracketsAndHexPrefix(header: str) -> str:
    cleanedHeader = str(header).strip().strip("[]")
    cleanedHeader = re.sub(r"^(0[xX])", "", cleanedHeader)
    cleanedHeader = cleanedHeader.lstrip("0") or "0"

    return cleanedHeader
