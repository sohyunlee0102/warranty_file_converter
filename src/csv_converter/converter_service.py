import math

from pandas import DataFrame, Series, concat
from tqdm import tqdm

from alarm_translator.alarm_translator_service import AlarmTranslatorService
from model.driver_config.driver_configuration_dto import (
    DriverConfigurationDto,
    RegisterDescriptionDto,
)
from model.driver_config.register_description_dto import (
    AlarmRegisterDescriptionDto,
    ValueRegisterDescriptionDto,
)
from utils.catl_sbmu_offset_register_const import CATL_SBMU_OFFSET_REGISTER
from value_translator.value_translator_service import ValueTranslatorService


class ConverterService:
    sbmuId: int = 0
    nextSbmuStartRegister: int = 2 * CATL_SBMU_OFFSET_REGISTER
    sbmuAddressOffset: int = 0
    dataFrameList: list[DataFrame] = []
    dataframeArrayId: int = 0
    sbmuSheetName = "MBMU"
    dateColumn = Series()
    dateColumnHeader: str

    def __init__(self, driverConfig: DriverConfigurationDto):
        self.driverConfig = driverConfig
        self.dataFrameList.append(DataFrame())
        self.dataFrameList[0].Name = "MBMU"

    def convert(self, csvData: DataFrame) -> list[DataFrame]:
        conversionProgressBar = tqdm(
            total=csvData.shape[1], desc="Processing columns", leave=False
        )

        for columnName in csvData.columns:
            self.__processColumn(csvData[columnName])
            conversionProgressBar.update(1)

        conversionProgressBar.write("✅ Data converted successfully.")
        conversionProgressBar.clear()
        conversionProgressBar.close()
        conversionProgressBar.refresh()
        return self.dataFrameList

    def __processColumn(self, columnInfo: Series):
        columnHeader = str(columnInfo.name)
        columnConfig = self.__getColumnConfig(columnHeader)

        if columnConfig:
            userFriendlyHeader = getattr(columnConfig, "targetColumn", columnHeader)
            newColumn = self.__convertColumn(
                columnInfo, columnHeader, columnConfig, userFriendlyHeader
            )

            self.dataFrameList[self.dataframeArrayId][userFriendlyHeader] = newColumn

    def __convertColumn(
        self, columnInfo, columnHeader, columnConfig, userFriendlyHeader
    ):
        newColumn = Series(columnInfo)
        subColumnNameSeries = Series(
            [self.__getHexNameHeader(columnHeader)], index=[" "]
        )
        if columnHeader == "DATE":
            if hasattr(columnInfo, "dt"):
                try:
                    newColumn = concat(
                        [subColumnNameSeries, columnInfo.dt.tz_localize(None)]
                    )
                except Exception:
                    pass
            self.dateColumn = newColumn
            self.dateColumnHeader = userFriendlyHeader
        elif isinstance(columnConfig, ValueRegisterDescriptionDto):
            translator = ValueTranslatorService(
                columnInfo, columnConfig.offset, columnConfig.conversionFactor
            )
            newColumn = concat([subColumnNameSeries, translator.translateColumn()])
        elif isinstance(columnConfig, AlarmRegisterDescriptionDto):
            translator = AlarmTranslatorService(
                columnInfo, columnConfig.alarmBitLength, columnConfig.alarmMap
            )
            newColumn = concat([subColumnNameSeries, translator.translateColumn()])
        elif isinstance(columnConfig, RegisterDescriptionDto):
            newColumn = concat([subColumnNameSeries, columnInfo])
        return newColumn

    def __getHexNameHeader(self, columnHeader):
        hexHeader = columnHeader
        try:
            hexHeader = hex(int(columnHeader, 16)).upper()
        except:
            pass
        return hexHeader

    def __getColumnConfig(self, columnHeader: str) -> RegisterDescriptionDto | None:
        columnHexValue = 0
        try:
            columnHexValue = int(columnHeader, 16)
        except:
            return self.driverConfig.MBMU.get(columnHeader)

        if math.isnan(columnHexValue):
            return None

        if columnHexValue < CATL_SBMU_OFFSET_REGISTER:
            return self.driverConfig.MBMU.get(columnHeader)
        else:
            if self.dataframeArrayId == 0:
                self.__setupNewSbmuDataframe()
            sbmuAddress = self.__getStringAddress(columnHexValue)
            return self.driverConfig.SBMU.get(sbmuAddress)

    def __setupNewSbmuDataframe(self):
        self.sbmuSheetName = f"SBMU{self.sbmuId + 1}"
        self.dataframeArrayId += 1

        newDataframe = DataFrame()
        newDataframe.Name = self.sbmuSheetName
        newDataframe[self.dateColumnHeader] = self.dateColumn

        self.dataFrameList.append(newDataframe)

    def __getStringAddress(self, address: int) -> str:
        sbmuAddress = address - self.sbmuAddressOffset

        if sbmuAddress >= self.nextSbmuStartRegister:
            self.sbmuId += 1
            self.sbmuAddressOffset = CATL_SBMU_OFFSET_REGISTER * self.sbmuId
            sbmuAddress -= CATL_SBMU_OFFSET_REGISTER
            self.__setupNewSbmuDataframe()

        return f"{sbmuAddress:X}"
