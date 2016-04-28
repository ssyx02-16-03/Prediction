import numpy as np


class RAvgEstimator:

    def __init__(self, window):
        """
        :window: (time-) window to compute mean on
        """
        self.window = float(window)

    def fit(self, x, y):
        self.fit_x = x
        self.fit_y = y

    def predict(self, x):
        y = np.array([None] * len(x))
        for i in range(len(x)):
            numerator = float(0)
            denominator = float(0)
            for j in range(len(self.fit_x)):
                if 0 <= x[i] - self.fit_x[j] <= self.window:
                    numerator = numerator + self.fit_y[j]
                    denominator = denominator + 1
            y[i] = numerator / denominator
        return y
