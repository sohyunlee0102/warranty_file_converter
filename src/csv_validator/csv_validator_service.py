import re

import pandas as pd

from utils.catl_sbmu_offset_register_const import CATL_OFFSET_REGISTER


class CsvValidatorService:
    def __init__(
        self,
        requiredHeaders: dict[str, list[str]],
        csvData: pd.DataFrame,
        numberOfStrings: int,
        timeMaxIntervalInSeconds: int,
    ):
        self.csvData = csvData
        self.driverRequiredHeaders: dict[str, list[str]] = requiredHeaders
        self.numberOfStrings = numberOfStrings
        self.timeMaxIntervalInSeconds = timeMaxIntervalInSeconds

    def validate(self, csvPath: str) -> bool:
        self.validateFileExtension(csvPath)

        headerList = self.csvData.columns.tolist()
        self.validateDuplicatedHeaders(headerList)
        self.validateRequiredHeaders(headerList)

        self.validateColumnCountConsistency()

        self.validateTimeContinuity()

        print("✅ CSV file validation passed.")

        return True

    def validateFileExtension(self, csvPath: str) -> bool:
        if not csvPath.lower().endswith(".csv"):
            raise ValueError(
                f"❌ Invalid file extension. Expected a .csv file: {csvPath}"
            )

        return True

    def validateRequiredHeaders(self, headers: list[str]) -> bool:
        requiredHeaders = self._getFullRequiredHeaders()

        missingHeaders = [header for header in requiredHeaders if header not in headers]

        if missingHeaders:
            raise ValueError(
                f"❌ Missing required headers: {', '.join(missingHeaders)}"
            )

        return True

    def _getFullRequiredHeaders(self) -> list[str]:
        requiredHeaders = self.driverRequiredHeaders["MBMU"]
        if len(self.driverRequiredHeaders["SBMU"]) > 0:
            for stringIndex in range(0, self.numberOfStrings):
                stringHeaders = [
                    f"{int(header, 16) + (stringIndex * CATL_OFFSET_REGISTER):X}"
                    for header in self.driverRequiredHeaders["SBMU"]
                ]
                requiredHeaders.extend(stringHeaders)
        return requiredHeaders

    def validateDuplicatedHeaders(self, headers: list[str]) -> bool:
        duplicatedHeaders = set(
            [
                header.split("]")[0]
                for header in headers
                if re.match(r"^(.*)(\]\.\d+)$", header)
            ]
        )

        if duplicatedHeaders:
            raise ValueError(
                f"❌ Duplicated headers found: {', '.join(duplicatedHeaders)}"
            )

        return True

    def validateTimeContinuity(self) -> bool:
        timeColumn = self.csvData.columns[0]
        timeSeries = self._parseDatetimeColumn(timeColumn)

        self._validateDatetimeValues(timeColumn, timeSeries)

        timeSeries = timeSeries.sort_values().reset_index(drop=True)

        timeDiffs = timeSeries.diff().dropna()

        expectedMaxInterval = pd.Timedelta(seconds=self.timeMaxIntervalInSeconds)

        if not (timeDiffs <= expectedMaxInterval).all():
            gapIndices = timeDiffs[timeDiffs > expectedMaxInterval].index.tolist()
            raise ValueError(
                f"❌ Time gaps detected at rows: {gapIndices} — exceeding maximum interval: {expectedMaxInterval}"
            )

        return True

    def _parseDatetimeColumn(self, timeColumn) -> pd.Series:
        self.csvData[timeColumn] = pd.to_datetime(
            self.csvData[timeColumn], errors="coerce", utc=True
        )
        timeSeries = self.csvData[timeColumn]
        return timeSeries

    def _validateDatetimeValues(self, timeColumn, timeSeries):
        if timeSeries.isna().any():
            bad_rows = timeSeries[timeSeries.isna()].index.tolist()
            raise ValueError(
                f"❌ Time column '{timeColumn}' contains unparsable datetime values at rows: {bad_rows}"
            )

        if not pd.api.types.is_datetime64_any_dtype(timeSeries):
            raise ValueError(
                f"❌ Time column '{timeColumn}' is not in datetime format."
            )

    def validateColumnCountConsistency(self) -> bool:
        expectedColumnCount: int = len(self.csvData.columns)

        rowLengths = self.csvData.apply(lambda row: row.count(), axis=1)

        invalidRowIndices = rowLengths[rowLengths != expectedColumnCount].index.tolist()
        if invalidRowIndices:
            raise ValueError(
                f"❌ Column count mismatch at rows: {invalidRowIndices}. "
                f"Expected {expectedColumnCount} columns per row."
            )

        return True
