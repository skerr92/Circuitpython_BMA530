# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 Seth Kerr for Oak Dev Tech
#
# SPDX-License-Identifier: MIT
"""
`bma530`
================================================================================

Driver library for Bosch Sensortec BMA530 Advanced Accelerometer


* Author(s): Seth Kerr

Implementation Notes
--------------------

**Hardware:**


**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
"""

# imports

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/skerr92/Circuitpython_BMA530.git"

import time

import adafruit_bus_device.i2c_device as i2c_device  # pylint: disable=R0402
from micropython import const

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/skerr92/circuitpython_bma530.git"


i2c_addr = 24 #hex 0x18

BMA530_CMD = 0x7E
BMA530_HEALTH = 0x02
BMA530_ACCEL_DATA = 0x18
BMA530_DATA_RDY = 0x11
BMA530_ENABLE = 0x30
BMA530_CONFIG = 0x31
BMA530_RANGE = 0x32


class BMA530:
    
    def __init__(self,i2c,addr=i2c_addr):
        self._i2c = i2c_device.I2CDevice(i2c,addr)
        self._buffer = bytearray(1)
        
    def _write_register_byte(self, register, value):
        # Write a byte value to the specifier register address.
        with self._i2c:
            self._i2c.write(bytes([register, value]))

    def _read_register_bytes(self, register, result, length=None):
        # Read the specified register address and fill the specified result byte
        # array with result bytes.
        if length is None:
            length = len(result)
        with self._i2c:
            self._i2c.write_then_readinto(bytes([register]), result, in_end=length)
            
    def reset(self):
        """Reset the BMA530 into a default state ready to detect axial acceleration."""
        # Write to the reset register.
        self._write_register_byte(BMA530_CMD, 0xB6)
        time.sleep(1)  # This 1ms delay here probably isn't necessary but can't hurt.
        
    def check_health(self):
        """Check the health of the BMA530"""
        self._read_register_bytes(BMA530_HEALTH,self._buffer)
        print(self._buffer[0] & 0x0F)
        
    def set_default_config(self):
        """Set a default configuration"""
        self._write_register_byte(BMA530_ENABLE,0x00) # disable the accelerometer
        self._write_register_byte(BMA530_CONFIG,0xA6) # ODR 100Hz, Normal Filtering, HPM
        self._write_register_byte(BMA530_RANGE,0x0C) # range of +/-2g, Fool-off IIR -60dB
        self._write_register_byte(BMA530_ENABLE,0x0F)
        print("configured default config")
        
    def data_ready(self):
        """Check to see if the data is ready"""
        self._read_register_bytes(BMA530_DATA_RDY,self._buffer)
        return (self._buffer[0] & 0x01)
        
    def get_accel_data(self):
        """Get The entire acceleration data buffer"""
        accel_buf = bytearray(6)
        self._read_register_bytes(BAM530_ACCEL_DATA,accel_buf)
        return accel_buf
        
    def get_x_accel_data(self):
        """Get the X Direction Data"""
        accel_buf = bytearray(6)
        self._read_register_bytes(BMA530_ACCEL_DATA,accel_buf)
        return ((accel_buf[1] << 8) | accel_buf[0])
        
    def get_y_accel_data(self):
        """Get the Y Direction Data"""
        accel_buf = bytearray(6)
        self._read_register_bytes(BMA530_ACCEL_DATA,accel_buf)
        return ((accel_buf[3] << 8) | accel_buf[2])
        
    def get_z_accel_data(self):
        """Get the Z Direction Data"""
        accel_buf = bytearray(6)
        self._read_register_bytes(BMA530_ACCEL_DATA,accel_buf)
        return ((accel_buf[5] << 8) | accel_buf[4])
