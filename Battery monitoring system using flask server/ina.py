from micropython import const
import struct
import time

# INA219 Registers
_REG_CONFIG = const(0x00)
_REG_SHUNTVOLTAGE = const(0x01)
_REG_BUSVOLTAGE = const(0x02)
_REG_POWER = const(0x03)
_REG_CURRENT = const(0x04)
_REG_CALIBRATION = const(0x05)

class INA219:
    def __init__(self, shunt_ohms=0.1, i2c=None, address=0x40):
        self.i2c = i2c
        self.address = address
        self.shunt_ohms = shunt_ohms
        self.current_lsb = 0.001
        self.power_lsb = 0.02

    def configure(self):
        # Reset & configure
        config = 0x399F  # 32V range, 320mV shunt, 12-bit ADC
        self._write_register(_REG_CONFIG, config)

        # Calibration
        calibration = int(0.04096 / (self.current_lsb * self.shunt_ohms))
        self._write_register(_REG_CALIBRATION, calibration)

        time.sleep_ms(10)

    def voltage(self):
        raw = self._read_register(_REG_BUSVOLTAGE)
        return (raw >> 3) * 0.004  # volts

    def current(self):
        raw = self._read_register(_REG_CURRENT)
        return raw * self.current_lsb  # amps

    def power(self):
        raw = self._read_register(_REG_POWER)
        return raw * self.power_lsb  # watts

    def _read_register(self, register):
        data = self.i2c.readfrom_mem(self.address, register, 2)
        return struct.unpack(">H", data)[0]

    def _write_register(self, register, value):
        data = struct.pack(">H", value)
        self.i2c.writeto_mem(self.address, register, data)

