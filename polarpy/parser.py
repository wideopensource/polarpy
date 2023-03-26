from .callbacks import Callbacks
from .measurement_parser import MeasurementParser
from .measurement_settings_parser import MeasurementSettingsParser
from .headers import FeaturesHeader, MeasurementSettingsHeader, StartMeasurementHeader, MeasurementPacketHeader
from .header_parser import PacketHeaderParser
from .stream_reader import StreamReader
from .settings import StreamSettings

# todo foss: proper error handling


class Parser:
    def __init__(self, stream_settings: StreamSettings, callbacks: Callbacks):
        self._stream_settings = stream_settings
        self._callbacks = callbacks

        self.EOF = True
        self._epoch_us = 0
        self._bytes_remaining = 0
        self._reader = None

    def parse_features_packet(self, header: FeaturesHeader) -> bool:
        features = self._reader.pull_int8()

        # todo foss: something useful with this
        # print(f"ECG: {features & 0x01}")
        # print(f"PPG: {features & 0x02}")
        # print(f"ACC: {features & 0x04}")
        # print(f"PPI: {features & 0x08}")
        # print(f"RFU: {features & 0x10}")
        # print(f"GYRO: {features & 0x20}")
        # print(f"MAG: {features & 0x40}")

        return True

    def parse_measurement_settings_packet(self, header: MeasurementSettingsHeader):
        return MeasurementSettingsParser.parse(header, self._reader)

    def parse_start_measurement_packet(self, header: StartMeasurementHeader):
        reserved = self._reader.pull_int8()  # todo foss: something

        return True

    def parse_stream(self):
        header = PacketHeaderParser.parse(self._reader)

        if isinstance(header, FeaturesHeader):
            return self.parse_features_packet(header)

        if isinstance(header, MeasurementSettingsHeader):
            return self.parse_measurement_settings_packet(header)

        if isinstance(header, StartMeasurementHeader):
            return self.parse_start_measurement_packet(header)

        if isinstance(header, MeasurementPacketHeader):
            return MeasurementParser.parse(header, self._reader, self._stream_settings, self._callbacks)

        print(f"unknown response type")

        return False

    def parse(self, data: str):
        self._reader = StreamReader(
            data, epoch_us=self._stream_settings.epoch_us)

        if self._reader.EOF:
            print("unexpected EOF 1")
            return False

        rv = self.parse_stream()

        if 0 == self._stream_settings.epoch_us:
            self._stream_settings.epoch_us = self._reader._epoch_us

        return rv
