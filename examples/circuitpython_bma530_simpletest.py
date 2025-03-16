# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 Seth Kerr for Oak Dev Tech
#
# SPDX-License-Identifier: Unlicense

import bma530

import time
import board
import busio

# these pins are on the RPGA Feather. Change to the I2C pins on your board.
i2c = busio.I2C(board.D11,board.D10)

bma = bma530.BMA530(i2c)

bma.check_health()
bma.set_default_config()

while True:
    
    while (not bma.data_ready()):
        time.sleep(0.1)
        pass
    
    print("data is ready!")
    data = bma.get_accel_data()
    
    print("X: ",(data[1] << 8) | data[0], "Y: ", (data[3] << 8) | data[2],"Z: ", (data[5] << 8) | data[4] )
    plot_data = ((data[1] << 8) | data[0],(data[3] << 8) | data[2],(data[5] << 8) | data[4])
    print(plot_data)
    time.sleep(0.1)
