from .constants import MeasurementType


class FeaturesHeader:
    pass


class MeasurementSettingsHeader:
    def __init__(self, measurement_type: MeasurementType, error_code: int = 0, more_frames: bool = False):
        self.measurement_type = measurement_type
        self.error_code = error_code
        self.more_frames = more_frames


class StartMeasurementHeader:
    def __init__(self, measurement_type: MeasurementType, error_code: int = 0, more_frames: bool = False):
        self.measurement_type = measurement_type


class MeasurementPacketHeader:
    def __init__(self, measurement_type: MeasurementType, frame_type: int, start_timestamp_us: int, period_us: int):
        self.measurement_type = measurement_type
        self.frame_type = frame_type
        self.start_timestamp_us = start_timestamp_us
        self.period_us = period_us

        # self.error = 0
        # self.end_timestamp_us = 0
        # self.frame_length_bytes = 0
        # self.number_of_frames = 0
