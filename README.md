# polarpy

Tools for reading and fusing live data streams from Polar OH1 (PPG) and H10 (ECG) sensors.

## Requirements

If installing from the repo you need [`pygatttool`](https://github.com/wideopensource/pygatttool) (`pip install pygatttool`).

## Installation

```
pip install polarpy
```

## Usage

The following code starts the raw PPG and IMU streams on a Polar OH1, fuses the blocks pf data in the two streams at 135Hz, and provides a single output stream, each record having a timestamp, the PPG signal values for each of the 3 pairs of LEDs, and the corresponding accerelometer x, y and z readings.

```
from polarpy import OH1

OH1_ADDR = "A0:9E:1A:7D:3C:5D"
OH1_CONTROL_ATTRIBUTE_HANDLE = 0x003f
OH1_DATA_ATTRIBUTE_HANDLE = 0x0042

def callback(type: str, timestamp: float, payload: dict):
    print(f'{timestamp} {payload}')

if '__main__' == __name__:
    device = OH1(address=OH1_ADDR,
                 control_handle=OH1_CONTROL_ATTRIBUTE_HANDLE,
                 data_handle=OH1_DATA_ATTRIBUTE_HANDLE,
                 callback=callback)

    if device.start():
        while device.run():
            pass
```

The output looks something like this:

```
3.94 {'ppg0': 263249, 'ppg1': 351764, 'ppg2': 351928, 'ax': 0.775, 'ay': -0.42, 'az': 0.476}
3.947 {'ppg0': 263297, 'ppg1': 351964, 'ppg2': 352077, 'ax': 0.775, 'ay': -0.42, 'az': 0.476}
3.954 {'ppg0': 263319, 'ppg1': 352062, 'ppg2': 352013, 'ax': 0.778, 'ay': -0.417, 'az': 0.481}
3.962 {'ppg0': 263293, 'ppg1': 352106, 'ppg2': 352082, 'ax': 0.778, 'ay': -0.417, 'az': 0.481}
3.969 {'ppg0': 263440, 'ppg1': 352273, 'ppg2': 352199, 'ax': 0.778, 'ay': -0.417, 'az': 0.481}

...
```

The callback is used (rather than returning data from `run()`) because the blocks of PPG, ECG and IMU data arrive with different lengths and at different speeds. The individual samples from each channel must be buffered and interleaved, timestamps interpolated, then delivered asynchronously through the callback. 

The address and attribute handles for your particular device can be found using `gatttool` or another BLE tool such as nRF Connect.
