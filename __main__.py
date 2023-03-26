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
