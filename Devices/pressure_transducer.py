from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from labjack import ljm
from collections import deque

class PressureTransducer:
    def __init__(self, name, input_channel_1, input_channel_2, min_voltage, max_voltage, max_psi, scalar_offset, linear_offset, x, y, parent=None):
        self.name = name
        self.input_channel_1 = input_channel_1
        self.input_channel_2 = input_channel_2
        self.min_voltage = min_voltage
        self.max_voltage = max_voltage
        self.voltage_range = max_voltage - min_voltage
        self.max_psi = max_psi
        self.label = QtWidgets.QLabel("0000.0", parent)
        self.label.setGeometry(x, y, int(47 * parent.scaled_width/parent.static_width), int(14*parent.windim_y/parent.static_y))
        self.label.setStyleSheet("background-color: #00baff; color: white; font-size: 12pt; font-weight: bold; font-family: 'Courier New', monospace;")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setContentsMargins(2, 1, 2, 1)
        self.pressure = 0.0
        self.data = deque(maxlen=5)  # Store last 5
        self.redline = None
        self.linear_offset = linear_offset
        self.scalar_offset = scalar_offset

    def update_pressure(self, handle):
        try:
            voltage_1 = ljm.eReadName(handle, self.input_channel_1)
            if self.input_channel_2 != "":
                voltage_2 = ljm.eReadName(handle, self.input_channel_2)
            else:
                voltage_2 = 0
            voltage_diff = voltage_1 - voltage_2
            # if self.input_channel_1 == "AIN92":
            #     print(f"{self.input_channel_1},{self.input_channel_2}: {voltage_diff}")
            self.pressure = self.scalar_offset * (voltage_diff-self.min_voltage) / self.voltage_range * self.max_psi - self.linear_offset
            self.label.setText(f"{self.pressure:.1f}")
            self.data.append(self.pressure)
        except Exception as e:
            self.pressure = float('nan')
            self.data.append(self.pressure)
            raise Exception(f"pressure_transducer.py: Error reading pressure from {self.input_channel_1}: {e}")
