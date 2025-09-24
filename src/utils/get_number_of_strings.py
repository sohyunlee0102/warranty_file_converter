import re

import pandas as pd


def getNumberOfStrings(data: pd.DataFrame) -> int:
    lastColumn = data.columns[-1:].values[0]

    match = re.search(r"^\[?(?:0x)?0*([0-9a-fA-F]+)\]?$", lastColumn)
    if not match:
        raise ValueError(f"❌ Invalid format for the last column: {lastColumn}")

    hexValue = match.group(1)
    number = int(hexValue, 16)

    numberOfString = number / 0x400
    return int(numberOfString)
