from .constants import Constants, PPGFrameType, ACCFrameType, MeasurementType
from .callbacks import Callbacks

from .stream_reader import StreamReader
from .headers import MeasurementPacketHeader, MeasurementSettingsHeader
from .settings import StreamSettings

# todo foss: proper error handling


class MeasurementParser:
    def __init__(self, header: MeasurementPacketHeader, reader: StreamReader, settings: StreamSettings, callbacks: Callbacks):
        self._header = header
        self._reader = reader
        self._settings = settings
        self._callbacks = callbacks

    def parse_PPG_24bit(self):
        timestamp_us = self._header.start_timestamp_us
        period_us = Constants.sample_period_us(self._settings.PPG_sample_rate)

        while not self._reader.EOF:
            ppg0 = self._reader.pull_int22()
            ppg1 = self._reader.pull_int22()
            ppg2 = self._reader.pull_int22()
            ambient = self._reader.pull_int22()

            if self._callbacks.on_measurement:
                payload = (int(timestamp_us), ppg0, ppg1, ppg2, ambient,)
                self._callbacks.on_measurement(
                    MeasurementType.PPG, payload)

            timestamp_us += period_us

        self._final_timestamp_us = timestamp_us - period_us

        return True

    def parse_PPG(self):
        if PPGFrameType.PPGFrameType24 == self._header.frame_type:
            rv = self.parse_PPG_24bit()
        else:
            print(f"unknown PPG frame type {self._header.frame_type}")
            rv = False

        return rv

    def parse_ACC_16bit(self):
        timestamp_us = self._header.start_timestamp_us
        period_us = Constants.sample_period_us(self._settings.ACC_sample_rate)

        while not self._reader.EOF:
            x = self._reader.pull_int16()
            y = self._reader.pull_int16()
            z = self._reader.pull_int16()

            if self._callbacks.on_measurement:
                payload = (int(timestamp_us), x, y, z,)
                self._callbacks.on_measurement(
                    MeasurementType.ACC, payload)

            timestamp_us += period_us

        self._final_timestamp_us = timestamp_us - period_us

        return True

    def parse_ACC(self):
        if ACCFrameType.ACCFrameType16 == self._header.frame_type:
            rv = self.parse_ACC_16bit()
        else:
            print(f"unknown ACC frame type {self._header.frame_type}")
            rv = False

        return rv

    def _parse(self):
        if MeasurementType.PPG == self._header.measurement_type:
            return self.parse_PPG()

        if MeasurementType.ACC == self._header.measurement_type:
            return self.parse_ACC()

        print(f"unknown measurement type {self._header.measurement_type}")

        return False

    @staticmethod
    def parse(header: MeasurementSettingsHeader, reader: StreamReader, settings: StreamSettings, callbacks):
        parser = MeasurementParser(header, reader, settings, callbacks)
        return parser._parse()
