import re

import pandas as pd

from utils.catl_sbmu_offset_register_const import CATL_SBMU_OFFSET_REGISTER


def getNumberOfStrings(data: pd.DataFrame) -> int:
    lastColumn = data.columns[-1:].values[0]

    match = re.search(r"^\[?(?:0x)?0*([0-9a-fA-F]+)\]?$", lastColumn)
    if not match:
        raise ValueError(f"❌ Invalid format for the last column: {lastColumn}")

    hexValue = match.group(1)
    number = int(hexValue, 16)

    numberOfString = number / CATL_SBMU_OFFSET_REGISTER
    return int(numberOfString)
