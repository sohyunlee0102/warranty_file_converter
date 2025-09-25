from __future__ import annotations

from typing import Dict, List

import pandas as pd


class AlarmTranslatorService:
    def __init__(
        self,
        alarmColumnRegisters: pd.Series[str],
        alarmBitLength: int,
        alarmMap: Dict[str, Dict[str, str]],
        separator: str = "\n",
    ):
        self.alarmColumnRegisters = alarmColumnRegisters
        self.alarmBitLength = alarmBitLength
        self.alarmMap = alarmMap
        self.separator = separator

    def translateAlarmColumn(self) -> pd.Series[str]:
        if self.alarmBitLength <= 0:
            raise ValueError("alarmBitLength must be positive")

        results = self.alarmColumnRegisters.apply(
            lambda cellIterator: self.translateAlarmCell(cellIterator)
        )

        return results

    def translateAlarmCell(self, cellString: str) -> str:
        try:
            cellValue = int(cellString)
            bitArray = self.decimalToBinaryArray(cellValue)
            alarmNormalizedArray = self.divideBinaryArray(bitArray)
            return self.mapAlarms(alarmNormalizedArray)
        except Exception:
            return cellString

    def decimalToBinaryArray(self, value: int | str) -> List[int]:
        try:
            decimalNumber = int(value)
        except Exception:
            raise ValueError(f"Invalid decimal string: {value}")

        if decimalNumber < 0 or decimalNumber > 0xFFFF:
            raise ValueError(f"Value out of 16-bit range: {decimalNumber}")

        binaryString = bin(decimalNumber)[2:].zfill(16)
        bitArray = [int(bit) for bit in binaryString]
        return bitArray

    def divideBinaryArray(self, binaryArray: List[int]) -> List[str]:
        if self.alarmBitLength <= 0:
            raise ValueError("Alarm bit length must be a positive integer")

        if not all(bit in (0, 1) for bit in binaryArray):
            raise ValueError("Binary array must contain only 0s and 1s")

        paddedBinaryArray = self.getPaddedArray(binaryArray)

        decimalValues = self.getHighToLowArray(paddedBinaryArray)

        # The spec expects reversing the groups so that lower-order groups come first
        decimalValues.reverse()
        return decimalValues

    def getHighToLowArray(self, paddedBinaryArray):
        decimalValues: List[str] = []
        for startIndex in range(0, len(paddedBinaryArray), self.alarmBitLength):
            chunkBits = paddedBinaryArray[startIndex : startIndex + self.alarmBitLength]
            # chunkBits is Most-Significative-Bit-first
            chunkValue = 0
            for bit in chunkBits:
                chunkValue = (chunkValue << 1) | bit
            decimalValues.append(str(chunkValue))

        return decimalValues

    def getPaddedArray(self, binaryArray):
        remainder = len(binaryArray) % self.alarmBitLength
        if remainder != 0:
            paddingNeeded = self.alarmBitLength - remainder
            paddedBinaryArray = [0] * paddingNeeded + list(binaryArray)
        else:
            paddedBinaryArray = list(binaryArray)

        return paddedBinaryArray

    def mapAlarms(self, dividedValues: List[str]) -> str:
        mappedTexts: List[str] = []

        for position, value in enumerate(dividedValues):
            if value == 0:
                continue

            alarmDescription = self.getAlarmDescription(position, value)
            mappedTexts.append(alarmDescription)

        if not mappedTexts:
            return "normal"

        return self.separator.join(mappedTexts)

    def getAlarmDescription(self, position, value):
        alarmDescription = None
        positionAlarmValues = self.alarmMap.get(str(position))
        if positionAlarmValues:
            alarmDescription = positionAlarmValues.get(value)

        if not alarmDescription:
            alarmDescription = f"unknown alarm in position {position} value {value}"
        return alarmDescription
