if "__main__" == __name__:
    from constants import MeasurementType, CommandType
    from constants import SettingType, RangeSetting, SampleRateSetting, ResolutionSetting
else:
    from .constants import MeasurementType, CommandType
    from .constants import SettingType, RangeSetting, SampleRateSetting, ResolutionSetting

import io
from enum import Enum


class CommandBuilder:
    def __init__(self):
        self._stream = io.BytesIO()

    def _write_byte(self, value: int):
        self._stream.write(bytes([value]))

    def _write_int16(self, value: int):
        self._stream.write(bytes([value & 0xff, (value >> 8) & 0xff]))

    def _write_setting_value(self, value: int):
        self._write_byte(1)
        self._write_int16(value)

    @ staticmethod
    def start_measurement(type: MeasurementType):
        command = CommandBuilder()
        command._write_byte(CommandType.StartMeasurement)
        command._write_byte(type)
        return command

    @ staticmethod
    def get_measurement_settings(type: MeasurementType):
        command = CommandBuilder()
        command._write_byte(CommandType.GetMeasurementSettings)
        command._write_byte(type)
        return command

    def build(self) -> bytearray:
        return self._stream.getvalue()

    def add_range(self, range: RangeSetting):
        self._write_byte(SettingType.Range)
        self._write_setting_value(range)
        return self

    def add_sample_rate(self, rate: SampleRateSetting):
        self._write_byte(SettingType.SampleRate)
        self._write_setting_value(rate)
        return self

    def add_resolution(self, resolution: ResolutionSetting):
        self._write_byte(SettingType.Resolution)
        self._write_setting_value(resolution)
        return self


class Commands:
    GetACCSettings = CommandBuilder \
        .get_measurement_settings(MeasurementType.ACC) \
        .build()

    GetPPGSettings = CommandBuilder \
        .get_measurement_settings(MeasurementType.PPG) \
        .build()

    OH1StartACC = CommandBuilder \
        .start_measurement(MeasurementType.ACC) \
        .add_range(RangeSetting.Range8G) \
        .add_sample_rate(SampleRateSetting.SampleRate50) \
        .add_resolution(ResolutionSetting.Resolution16) \
        .build()

    OH1StartPPG = CommandBuilder \
        .start_measurement(MeasurementType.PPG) \
        .add_sample_rate(SampleRateSetting.SampleRate135) \
        .add_resolution(ResolutionSetting.Resolution22) \
        .build()

    H10StartACC = CommandBuilder \
        .start_measurement(MeasurementType.ACC) \
        .add_range(RangeSetting.Range8G) \
        .add_sample_rate(SampleRateSetting.SampleRate200) \
        .add_resolution(ResolutionSetting.Resolution16) \
        .build()


if "__main__" == __name__:
    print(f'OH1StartPPG: {Commands.OH1StartPPG}')
    print(f'OH1StartACC: {Commands.OH1StartACC}')
