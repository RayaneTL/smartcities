# Grove RGB LED (P9813) - driver pour MicroPython (2 fils)
# Adapté du code Seeed Studio

from machine import Pin
import time

class P9813:
    def __init__(self, clk_pin, data_pin, num_leds=1):
        self.clk = Pin(clk_pin, Pin.OUT)
        self.data = Pin(data_pin, Pin.OUT)
        self.num_leds = num_leds
        self.buf = [(0, 0, 0)] * num_leds
        self.show()

    def _send_byte(self, b):
        for i in range(8):
            self.data.value((b >> (7 - i)) & 1)
            self.clk.value(1)
            self.clk.value(0)

    def _calc_hdr(self, r, g, b):
        hdr = 0xC0
        if (b & 0x80) == 0: hdr |= 0x20
        if (b & 0x40) == 0: hdr |= 0x10
        if (g & 0x80) == 0: hdr |= 0x08
        if (g & 0x40) == 0: hdr |= 0x04
        if (r & 0x80) == 0: hdr |= 0x02
        if (r & 0x40) == 0: hdr |= 0x01
        return hdr

    def _start_frame(self):
        for _ in range(4):
            self._send_byte(0x00)

    def _end_frame(self):
        for _ in range(4):
            self._send_byte(0x00)

    def set_led(self, n, r, g, b):
        if 0 <= n < self.num_leds:
            self.buf[n] = (r & 0xFF, g & 0xFF, b & 0xFF)

    def show(self):
        self._start_frame()
        for (r, g, b) in self.buf:
            hdr = self._calc_hdr(r, g, b)
            self._send_byte(hdr)
            self._send_byte(b)
            self._send_byte(g)
            self._send_byte(r)
        self._end_frame()
