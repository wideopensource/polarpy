from .constants import MeasurementType


class Callbacks:
    def __init__(self):
        pass

    def on_measurement(self, type: MeasurementType, payload):
        pass
