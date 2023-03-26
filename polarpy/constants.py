from enum import IntEnum


class DeviceType(IntEnum):
    H10 = 1,
    OH1 = 2


class CommandType(IntEnum):
    GetMeasurementSettings = 1,
    StartMeasurement = 2


class SettingType(IntEnum):
    SampleRate = 0,
    Resolution = 1,
    Range = 2,


class RangeSetting(IntEnum):
    Range8G = 0x0008,


class SampleRateSetting(IntEnum):
    SampleRate50 = 0x0032
    SampleRate135 = 0x0082
    SampleRate200 = 0x00c8
    SampleRateUnknown = -1


class ResolutionSetting(IntEnum):
    Resolution16 = 0x0010
    Resolution22 = 0x0016


class ACCFrameType(IntEnum):
    ACCFrameType8 = 0,
    ACCFrameType16 = 1,
    ACCFrameType24 = 2,
    ACCFrameTypeDelta = 128


class PPGFrameType(IntEnum):
    PPGFrameType24 = 0,
    PPGFrameTypeDelta = 128


class ControlPointResponseType(IntEnum):
    FeatureRead = 0x0f,
    Response = 0xf0


class ResponseOpCode(IntEnum):
    GetMeasurementSettings = 1,
    StartMeasurement = 2


class MeasurementType(IntEnum):
    ECG = 0,
    PPG = 1,
    ACC = 2,
    PPI = 3,
    GYRO = 5,
    MAG = 6


class Constants:
    def frame_size(measurement_type: MeasurementType, frame_type) -> int:
        if MeasurementType.ACC == measurement_type:
            if ACCFrameType.ACCFrameType8 == frame_type:
                return 3
            if ACCFrameType.ACCFrameType16 == frame_type:
                return 6
            if ACCFrameType.ACCFrameType24 == frame_type:
                return 9
            return 0

        if MeasurementType.PPG == measurement_type:
            if PPGFrameType.PPGFrameType24 == frame_type:
                return 12
            return 0

        return 0

    def sample_period_us(sample_rate: SampleRateSetting) -> int:
        if SampleRateSetting.SampleRate135 == sample_rate:
            return 1000000 / 135
        if SampleRateSetting.SampleRate200 == sample_rate:
            return 1000000 / 200
        if SampleRateSetting.SampleRate50 == sample_rate:
            return 1000000 / 50

        return 0


if __name__ == "__main__":
    print(MeasurementType.ACC.value)
