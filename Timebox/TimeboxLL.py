import bluetooth
import math

from Log import log

TIMEBOX_HELLO = [0, 5, 72, 69, 76, 76, 79, 0]

VIEWTYPES = {
    "clock": 0x00,
    "temp": 0x01,
    "off": 0x02,
    "anim": 0x03,
    "graph": 0x04,
    "image": 0x05,
    "stopwatch": 0x06,
    "scoreboard": 0x07
}

class TimeboxLL():

    def __init__(self, addr):
        self._sock = None
        self._addr = addr

    def _connect(self):
        log('TimeboxLL._connect() connecting...')
        self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self._sock.connect((self._addr, 4))
        if(self._read(256) == TIMEBOX_HELLO):
            log('TimeboxLL._connect() valid hello received')
        else:
            log('TimeboxLL._connect() invalid hello received')

    def _send(self, array):
        self._sock.send(TimeboxLL.toMessage(array))

    def _read(self, amount):
        return [ord(chr(c)) for c in self._sock.recv(amount)]

    def _print_service(self, uuid):

        self._print_service_matches( bluetooth.find_service(uuid = uuid, address = self._addr) )

    def _print_service_matches(self, matches):

        for match in matches:
            print( match )

    def _switch_view(self, type):
        h = [0x04, 0x00, 0x45, VIEWTYPES[type]]
        ck1, ck2 = TimeboxLL._checksum(sum(h))
        return [0x01] + TimeboxLL._mask(h) + TimeboxLL._mask([ck1, ck2]) + [0x02]

    def _set_time_color(cls, r, g, b, x=0x00, h24=True):
        head = [0x09, 0x00, 0x45, 0x00, 0x01 if h24 else 0x00]
        s = sum(head) + sum([r, g, b, x])
        ck1, ck2 = TimeboxLL._checksum(s)
        # create message mask 0x01,0x02,0x03
        return [0x01] + TimeboxLL._mask(head) + TimeboxLL._mask([r, g, b, x]) + TimeboxLL._mask([ck1, ck2]) + [0x02]


    def _volume(self, level):
        head = [0x04, 0x00, 0x08]
        ck1, ck2 = TimeboxLL._checksum(sum(head) + level)
        return [0x01] + head + TimeboxLL._mask([level]) + TimeboxLL._mask([ck1, ck2]) + [0x02]

    @staticmethod
    def _color_comp_conv(cc):
        cc = max(0.0, min(1.0, cc))
        return int(math.floor(255 if cc == 1.0 else  cc * 256.0))

    @staticmethod
    def _color_convert(rgb):
        return [TimeboxLL._color_comp_conv(c) for c in rgb]

    @staticmethod
    def _unmask(bytes, index=0):
        try:
            index = bytes.index(0x03, index)
        except ValueError:
            return bytes

        _bytes = bytes[:]
        _bytes[index + 1] = _bytes[index + 1] - 0x03
        _bytes.pop(index)
        return TimeboxLL._unmask(_bytes, index + 1)

    @staticmethod
    def _mask(bytes):
        _bytes = []
        for b in bytes:
            if (b == 0x01):
                _bytes = _bytes + [0x03, 0x04]
            elif (b == 0x02):
                _bytes = _bytes + [0x03, 0x05]
            elif (b == 0x03):
                _bytes = _bytes + [0x03, 0x06]
            else:
                _bytes += [b]

        return _bytes

    @staticmethod
    def _checksum(s):
        ck1 = s & 0x00ff
        ck2 = s >> 8
        return ck1, ck2

    @staticmethod
    def toMessage(array):
        return ''.join(e for e in array)
