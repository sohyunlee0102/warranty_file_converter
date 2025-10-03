from __future__ import annotations

from typing import Dict, List

import pandas as pd

__ALARM_NORMAL_STATUS_VALUE = "normal"


class AlarmTranslatorService:
    def __init__(
        self,
        columnSeries: pd.Series[str],
        alarmBitsLength: int,
        definitionMap: Dict[str, Dict[str, str]],
        separatorToken: str = "\n",
    ):
        self.columnSeries = columnSeries
        self.alarmBitsLength = alarmBitsLength
        self.definitionMap = definitionMap
        self.separatorToken = separatorToken

    def translateColumn(self) -> pd.Series[str]:
        if self.alarmBitsLength <= 0:
            raise ValueError("alarmBitLength must be positive")

        results = self.columnSeries.apply(
            lambda cellIterator: self.__translateCell(cellIterator)
        )

        return results

    def __translateCell(self, cellString: str) -> str:
        try:
            cellValue = int(cellString)
            if cellValue == 0:
                return __ALARM_NORMAL_STATUS_VALUE

            bitArray = self.__decimalToBinaryArray(cellValue)
            alarmNormalizedArray = self.__divideBinaryArray(bitArray)
            return self.__mapAlarms(alarmNormalizedArray)
        except Exception:
            return cellString

    def __decimalToBinaryArray(self, value: int | str) -> List[int]:
        try:
            decimalNumber = int(value)
        except Exception:
            raise ValueError(f"Invalid decimal string: {value}")

        if decimalNumber < 0 or decimalNumber > 0xFFFF:
            raise ValueError(f"Value out of 16-bit range: {decimalNumber}")

        binaryString = bin(decimalNumber)[2:].zfill(16)
        bitArray = [int(bit) for bit in binaryString]
        return bitArray

    def __divideBinaryArray(self, binaryArray: List[int]) -> List[str]:
        if self.alarmBitsLength <= 0:
            raise ValueError("Alarm bit length must be a positive integer")

        if not all(bit in (0, 1) for bit in binaryArray):
            raise ValueError("Binary array must contain only 0s and 1s")

        paddedBinaryArray = self.__getPaddedArray(binaryArray)

        decimalValues = self.__getHighToLowArray(paddedBinaryArray)

        # The spec expects reversing the groups so that lower-order groups come first
        decimalValues.reverse()
        return decimalValues

    def __getHighToLowArray(self, paddedBinaryArray):
        decimalValues: List[str] = []
        for startIndex in range(0, len(paddedBinaryArray), self.alarmBitsLength):
            chunkBits = paddedBinaryArray[
                startIndex : startIndex + self.alarmBitsLength
            ]
            # chunkBits is Most-Significative-Bit-first
            chunkValue = 0
            for bit in chunkBits:
                chunkValue = (chunkValue << 1) | bit
            decimalValues.append(str(chunkValue))

        return decimalValues

    def __getPaddedArray(self, binaryArray):
        remainder = len(binaryArray) % self.alarmBitsLength
        if remainder != 0:
            paddingNeeded = self.alarmBitsLength - remainder
            paddedBinaryArray = [0] * paddingNeeded + list(binaryArray)
        else:
            paddedBinaryArray = list(binaryArray)

        return paddedBinaryArray

    def __mapAlarms(self, dividedValues: List[str]) -> str:
        mappedTexts: List[str] = []

        for position, value in enumerate(dividedValues):
            if int(value) == 0:
                continue

            alarmDescription = self.__getAlarmDescription(position, value)
            mappedTexts.append(alarmDescription)

        if not mappedTexts:
            return "normal"

        return self.separatorToken.join(mappedTexts)

    def __getAlarmDescription(self, position, value) -> str:
        alarmDescription = ""
        positionAlarmValues = self.definitionMap.get(str(position))
        if positionAlarmValues:
            alarmDescription = positionAlarmValues.get(value, "")

        if value != 0 and alarmDescription == "":
            alarmDescription = f"unknown alarm in position {position} value {value}"

        return alarmDescription
