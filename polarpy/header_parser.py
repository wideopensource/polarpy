from .constants import Constants, ControlPointResponseType, ResponseOpCode, MeasurementType
from .headers import FeaturesHeader, MeasurementSettingsHeader, StartMeasurementHeader, MeasurementPacketHeader

from .stream_reader import StreamReader

# todo foss: proper error handling


class PacketHeaderParser:
    @staticmethod
    def parse(reader: StreamReader):
        if reader.EOF:
            print("unexpected EOF")
            return None

        response_type = reader.pull_int8()

        if response_type in iter(ControlPointResponseType):
            control_type_response_type = ControlPointResponseType(
                response_type)

            if ControlPointResponseType.FeatureRead == control_type_response_type:
                return FeaturesHeaderParser.parse(reader)

            if ControlPointResponseType.Response == control_type_response_type:
                opcode = ResponseOpCode(reader.pull_int8())

                if ResponseOpCode.GetMeasurementSettings == opcode:
                    return MeasurementSettingsHeaderParser.parse(reader)

                if ResponseOpCode.StartMeasurement == opcode:
                    return StartMeasurementHeaderParser.parse(reader)

                print(f"unknown opcode {opcode}")

                return None

        measurement_type = MeasurementType(response_type)

        return MeasurementHeaderParser.parse(measurement_type, reader)


class FeaturesHeaderParser:
    @ staticmethod
    def parse(reader: StreamReader) -> FeaturesHeader:
        return FeaturesHeader()


class MeasurementSettingsHeaderParser:
    @ staticmethod
    def parse(reader: StreamReader) -> MeasurementSettingsHeader:
        measurement_type = MeasurementType(reader.pull_int8())
        error_code = reader.pull_int8()
        more_frames = reader.pull_int8() != 0

        return MeasurementSettingsHeader(measurement_type=measurement_type, error_code=error_code, more_frames=more_frames)


class StartMeasurementHeaderParser:
    @ staticmethod
    def parse(reader: StreamReader) -> StartMeasurementHeader:
        measurement_type = MeasurementType(reader.pull_int8())
        error_code = reader.pull_int8()
        more_frames = reader.pull_int8() != 0

        return StartMeasurementHeader(measurement_type=measurement_type, error_code=error_code, more_frames=more_frames)


class MeasurementHeaderParser:
    @ staticmethod
    def parse(measurement_type: MeasurementType, reader: StreamReader, period_us: int = 135) -> MeasurementPacketHeader:
        end_timestamp_us = reader.pull_timestamp()
        frame_type = reader.pull_int8()

        frame_size = Constants.frame_size(measurement_type, frame_type)
        if 0 == frame_size:
            print(f"unknown frame size {measurement_type.name}, {frame_type}")

            return None

        number_of_frames = reader._bytes_remaining / frame_size

        start_timestamp_us = end_timestamp_us - \
            (number_of_frames - 1) * period_us

        return MeasurementPacketHeader(
            measurement_type=measurement_type, frame_type=frame_type, start_timestamp_us=start_timestamp_us, period_us=period_us)
