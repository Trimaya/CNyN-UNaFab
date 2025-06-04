import numpy as np


class Slope:
    def __init__(self, batch_size=50):
        self.batch_size = batch_size
        self.buffer_x = np.zeros(batch_size)
        self.buffer_y = np.zeros(batch_size)
        self._slope = 0
        self._fill_counter = 0

    def append(self, x, y):
        self.buffer_x = np.roll(self.buffer_x, -1)
        self.buffer_x[-1] = x
        self.buffer_y = np.roll(self.buffer_y, -1)
        self.buffer_y[-1] = y

        if self._fill_counter >= self.batch_size:
            self._slope = np.polyfit(self.buffer_x, self.buffer_y, 1)[0]
        else:
            self._fill_counter += 1
        return self._slope

    @property
    def value(self):
        return self._slope
