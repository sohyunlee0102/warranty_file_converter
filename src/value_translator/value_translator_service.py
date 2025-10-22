from pandas import Series, isna


class ValueTranslatorService:
    def __init__(
        self,
        column: Series,
        offset: int = 0,
        conversionFactor: float = 1,
    ):
        self.column = column
        self.offset = offset
        self.conversionFactor = conversionFactor

    def translateColumn(self) -> Series:
        results = self.column.apply(
            lambda cellIterator: self.__translateCell(cellIterator)
        )

        return results

    def __translateCell(self, cellString: str) -> float | int | str | None:
        if isna(cellString):
            return cellString

        cellValue = int(cellString)
        try:
            return (cellValue + self.offset) * self.conversionFactor
        except Exception:
            return cellValue
