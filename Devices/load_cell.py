from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from labjack import ljm
from collections import deque

class LoadCell:
    def __init__(self, name, input_channel_1, input_channel_2, max_voltage, max_load, scalar_offset, linear_offset, x, y, parent):
        self.name = name
        self.input_channel_1 = input_channel_1
        self.input_channel_2 = input_channel_2
        self.max_voltage = max_voltage
        self.max_load = max_load
        self.label = QtWidgets.QLabel("0000.0", parent)
        self.label.setGeometry(x, y, int(47 * parent.scaled_width/parent.static_width), int(14*parent.windim_y/parent.static_y))
        self.label.setStyleSheet("background-color: #9100FF; color: white; font-size: 12pt; font-weight: bold; font-family: 'Courier New', monospace;")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setContentsMargins(2, 1, 2, 1)
        self.load = 0.0
        self.data = deque(maxlen=5)  # Store last 5
        self.redline = None
        self.linear_offset = linear_offset
        self.scalar_offset = scalar_offset

    def update_load(self, handle):
        try:
            names = ["", "AIN3"]
            voltages = ljm.eReadNames(handle, 2, [self.input_channel_1, self.input_channel_2])
            voltage_diff = voltages[0] - voltages[1]
            # print(f"Load Cell: {voltage_diff}")
            self.load = self.scalar_offset * voltage_diff / self.max_voltage * self.max_load - self.linear_offset
            self.label.setText(f"{self.load:.1f}")
            self.data.append(self.load)
        except Exception as e:
            self.load = float('nan')
            self.data.append(self.load)
            raise Exception(f"load_cell.py: Error reading load from {self.input_channel_1}: {e}")
