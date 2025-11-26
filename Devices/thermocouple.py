from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from labjack import ljm
from collections import deque

class Thermocouple:
    def __init__(self, name, input_channel_1, max_voltage, max_temp, scalar_offset, linear_offset, x, y, parent):
        self.name = name
        self.input_channel_1 = input_channel_1
        self.max_voltage = max_voltage
        self.max_temp = max_temp
        self.label = QtWidgets.QLabel("0000.0", parent)
        self.label.setGeometry(x, y, int(47 * parent.scaled_width/parent.static_width), int(14*parent.windim_y/parent.static_y))
        self.label.setStyleSheet("background-color: #f0d043; color: white; font-size: 12pt; font-weight: bold; font-family: 'Courier New', monospace;")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setContentsMargins(2, 1, 2, 1)
        self.temperature = 0.0
        self.data = deque(maxlen=5)  # Store last 5
        self.redline = None
        self.linear_offset = linear_offset
        self.scalar_offset = scalar_offset

    def update_temperature(self, handle):
        try:
            voltage_1 = ljm.eReadName(handle, self.input_channel_1)
            # print(voltage_1)
            self.temperature = self.scalar_offset * voltage_1 / self.max_voltage * self.max_temp - self.linear_offset
            self.label.setText(f"{self.temperature:.1f}")
            self.data.append(self.temperature)
        except Exception as e:
            self.temperature = float('nan')
            self.data.append(self.temperature)
            raise Exception(f"thermocouple.py: Error reading temperature from {self.input_channel_1}: {e}")
