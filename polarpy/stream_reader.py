from io import BytesIO


class StreamReader:
    def __init__(self, data: str, epoch_us: int):
        parts = data.strip().split(' ')
        bytes = bytearray([int(s, 16) for s in parts])

        self._data_len = len(bytes)
        self._bytes_remaining = self._data_len
        self._stream = BytesIO(bytes)
        self._read_next_byte()
        self._epoch_us = epoch_us

        self.EOF = False

    def _read_next_byte(self) -> int:
        next_byte = self._stream.read(1)
        self.EOF = 0 == len(next_byte)
        self._next_byte = -1 if self.EOF else next_byte[0]

    def _pull_byte(self):
        b = self._next_byte
        self._read_next_byte()
        self._bytes_remaining -= 1
        return b

    def pull_int8(self):
        return self._pull_byte()

    def pull_int16(self):
        l = self._pull_byte()
        h = self._pull_byte()
        v = l + (h << 8)
        if v >= 0x8000:
            v = -(0xffff - v)

        return v

    def pull_int22(self) -> int:
        l = self._pull_byte()
        m = self._pull_byte()
        h = self._pull_byte() & 0x3f

        v = (l & 0xff) + ((m & 0xff) << 8) + ((h & 0xff) << 16) & 0x3fffff

        if v >= 0x200000:
            v = -(0x3fffff - v)

        return v

    def pull_int64(self):
        d0 = self._pull_byte()
        d1 = self._pull_byte()
        d2 = self._pull_byte()
        d3 = self._pull_byte()
        d4 = self._pull_byte()
        d5 = self._pull_byte()
        d6 = self._pull_byte()
        d7 = self._pull_byte()
        v = d0 + (d1 << 8) + (d2 << 16) + (d3 << 24) + \
            (d4 << 32) + (d5 << 40) + (d6 << 48) + (d7 << 56)

        return v

    def pull_timestamp(self) -> int:
        timestamp_us = self.pull_int64() / 1000

        if 0 == self._epoch_us:
            self._epoch_us = timestamp_us

        timestamp_us -= self._epoch_us

        return timestamp_us
