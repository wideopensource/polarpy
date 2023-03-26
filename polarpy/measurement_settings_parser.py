from .constants import MeasurementType
from .header_parser import MeasurementSettingsHeader
from .stream_reader import StreamReader

# todo foss: proper error handling


class MeasurementSettingsParser:
    def __init__(self, header: MeasurementSettingsHeader, reader: StreamReader):
        self._header = header
        self._reader = reader

    def parse_sample_rate(self):
        array_length = self._reader.pull_int8()

        for i in range(array_length):
            self._reader.pull_int16()

        return True

    def parse_resolution(self):
        array_length = self._reader.pull_int8()

        for i in range(array_length):
            self._reader.pull_int16()

        return True

    def parse_range(self):
        array_length = self._reader.pull_int8()

        for i in range(array_length):
            self._reader.pull_int16()

        return True

    def parse_setting(self):
        setting_type = self._reader.pull_int8()

        if 0x00 == setting_type:
            return self.parse_sample_rate()

        if 0x01 == setting_type:
            return self.parse_resolution()

        if 0x02 == setting_type:
            return self.parse_range()

        print(f"bad setting type {setting_type}")

        return False

    def parse_PPG_settings_response(self):
        while not self._reader.EOF:
            self.parse_setting()

        return True

    def parse_ACC_settings_response(self):
        while not self._reader.EOF:
            self.parse_setting()

        return True

    def _parse(self):
        measurement_type = self._header.measurement_type

        if MeasurementType.ECG == measurement_type:
            return self.parse_ECG_settings_response()

        if MeasurementType.PPG == measurement_type:
            return self.parse_PPG_settings_response()

        if MeasurementType.ACC == measurement_type:
            return self.parse_ACC_settings_response()

        if MeasurementType.PPI == measurement_type:
            return self.parse_PPI_settings_response()

        if MeasurementType.GYRO == measurement_type:
            return self.parse_GYRO_settings_response()

        if MeasurementType.MAG == measurement_type:
            return self.parse_MAG_settings_response()

        print(f"bad measurement type {measurement_type.name}")

        return False

    @staticmethod
    def parse(header: MeasurementSettingsHeader, reader: StreamReader):
        parser = MeasurementSettingsParser(header=header, reader=reader)
        parser._parse()
