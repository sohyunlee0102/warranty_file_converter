import re

from pandas import DataFrame, Series, Timedelta, api, to_datetime
from tqdm import tqdm

from model.driver_config.driver_configuration_dto import DriverConfigurationDto
from utils.catl_sbmu_offset_register_const import CATL_SBMU_OFFSET_REGISTER
from utils.get_number_of_strings import getNumberOfStrings
from utils.get_required_headers import getRequiredHeaders


class CsvValidatorService:
    def __init__(
        self,
        csvData: DataFrame,
        driverConfig: DriverConfigurationDto,
    ):
        self.csvData = csvData
        self.driverRequiredHeaders = getRequiredHeaders(driverConfig)
        self.numberOfStrings = getNumberOfStrings(csvData)
        self.timeMaxIntervalInSeconds = driverConfig.timeMaxIntervalInSeconds

    def validate(self, csvPath: str) -> bool:
        progressSteps = 5
        validationProgressBar = tqdm(
            total=progressSteps, desc="Validating CSV", unit="step", leave=False
        )
        try:
            self.validateFileExtension(csvPath)
            validationProgressBar.update(1)
            validationProgressBar.refresh()

            headerList = self.csvData.columns.tolist()
            self.validateDuplicatedHeaders(headerList)
            validationProgressBar.update(1)
            validationProgressBar.refresh()

            self.validateRequiredHeaders(headerList)
            validationProgressBar.update(1)
            validationProgressBar.refresh()

            self.validateColumnCountConsistency()
            validationProgressBar.update(1)
            validationProgressBar.refresh()

            self.validateTimeContinuity()
            validationProgressBar.update(1)
            validationProgressBar.refresh()

            validationProgressBar.write("✅ CSV file validation passed.")

            return True
        finally:
            validationProgressBar.clear()
            validationProgressBar.close()
            validationProgressBar.refresh()

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
        requiredHeaders = self.driverRequiredHeaders.MBMU
        if len(self.driverRequiredHeaders.SBMU) > 0:
            for stringIndex in range(0, self.numberOfStrings):
                stringHeaders = [
                    f"{int(header, 16) + (stringIndex * CATL_SBMU_OFFSET_REGISTER):X}"
                    for header in self.driverRequiredHeaders.SBMU
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

        expectedMaxInterval = Timedelta(seconds=self.timeMaxIntervalInSeconds)

        if not (timeDiffs <= expectedMaxInterval).all():
            gapIndices = timeDiffs[timeDiffs > expectedMaxInterval].index.tolist()
            raise ValueError(
                f"❌ Time gaps detected at rows: {gapIndices} — exceeding maximum interval: {expectedMaxInterval}"
            )

        return True

    def _parseDatetimeColumn(self, timeColumn) -> Series:
        self.csvData[timeColumn] = to_datetime(
            self.csvData[timeColumn], errors="coerce", utc=False
        )
        timeSeries = self.csvData[timeColumn]
        return timeSeries

    def _validateDatetimeValues(self, timeColumn, timeSeries):
        if timeSeries.isna().any():
            badRows = timeSeries[timeSeries.isna()].index.tolist()
            raise ValueError(
                f"❌ Time column '{timeColumn}' contains unparsable datetime values at rows: {badRows}"
            )

        if not api.types.is_datetime64_any_dtype(timeSeries):
            raise ValueError(
                f"❌ Time column '{timeColumn}' is not in datetime format."
            )

    def validateColumnCountConsistency(self) -> bool:
        expectedColumnCount: int = len(self.csvData.columns)

        rowLengths = self.csvData.apply(lambda row: row.count(), axis=1)

        invalidRowIndices = rowLengths[rowLengths != expectedColumnCount].index.tolist()
        if invalidRowIndices:
            print(
                f"⚠️ Column count mismatch at rows: {invalidRowIndices}. "
                f"Expected {expectedColumnCount} columns per row."
            )

        return True
