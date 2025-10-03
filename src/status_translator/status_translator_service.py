from pandas import Series


class StatusTranslatorService:
    def __init__(
        self,
        column: Series,
        statusLookup: dict[str, str],
        bitmaskLookup: dict[str, str],
    ):
        self.column = column
        self.statusLookup = statusLookup
        self.bitmaskLookup = bitmaskLookup

    def translateColumn(self) -> Series:
        results = self.column.apply(lambda rawValue: self.__translateCell(rawValue))

        return results

    def __translateCell(self, rawValue):
        if self.bitmaskLookup:
            setLabelForBit = (
                self.statusLookup.get("1")
                if self.statusLookup and "1" in self.statusLookup
                else None
            )
            return self.__mapBitmaskValue(rawValue, self.bitmaskLookup, setLabelForBit)

        if self.statusLookup:
            return self.__mapStatusValue(rawValue, self.statusLookup)

        return rawValue

    def __mapStatusValue(self, rawValue, statusLookup: dict | None):
        if not statusLookup:
            return rawValue
        try:
            if isinstance(rawValue, str):
                normalizedString = rawValue.strip()
                if normalizedString.lower().startswith("0x"):
                    numericValue = int(normalizedString, 16)
                else:
                    numericValue = int(float(normalizedString))
            else:
                numericValue = int(rawValue)
        except Exception:
            return rawValue
        return statusLookup.get(str(numericValue), rawValue)

    def __mapBitmaskValue(
        self,
        rawValue,
        bitLabelLookup: dict[str, str] | None,
        setLabel: str | None = None,
    ):
        if not bitLabelLookup:
            return rawValue
        try:
            if isinstance(rawValue, str):
                normalizedString = rawValue.strip()
                if normalizedString.lower().startswith("0x"):
                    bitfieldValue = int(normalizedString, 16)
                else:
                    bitfieldValue = int(float(normalizedString))
            else:
                bitfieldValue = int(rawValue)
        except Exception:
            return rawValue

        if bitfieldValue == 0:
            return "normal"

        enabledLabels: list[str] = []

        for bitIndexString, elementLabel in bitLabelLookup.items():
            bitIndex = int(bitIndexString)
            if (bitfieldValue >> bitIndex) & 1:
                suffix = f": {setLabel}" if setLabel else ""
                enabledLabels.append(f"{elementLabel}{suffix}")

        return ", ".join(enabledLabels) if enabledLabels else "normal"
