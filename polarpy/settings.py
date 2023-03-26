from .constants import SampleRateSetting


class StreamSettings:
    def __init__(self):
        self.ACC_sample_rate = SampleRateSetting.SampleRateUnknown
        self.PPG_sample_rate = SampleRateSetting.SampleRateUnknown
        self.ECG_sample_rate = SampleRateSetting.SampleRateUnknown
        self.epoch_us = 0
