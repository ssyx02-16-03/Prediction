import numpy as np
from sklearn.linear_model import LinearRegression


class LWRegressor:
    """
    Locally weighted regressor capable of fitting the meanest of
    noisy datasets to baby smooth curves
    """
    def __init__(self, sigma=1.0):
        """
        The smaller the sigma, the more localized the fit
        """
        self.sigma = sigma

    def fit(self, x, y):
        self.fit_x = x
        self.fit_y = y

    def predict(self, x):
        y_pred = np.array([None] * len(x)).reshape(-1, 1)
        for i in range(len(x)):
            weights = self.gauss_kernel(x[i] - self.fit_x, self.sigma)
            weights = np.ravel(weights)  # cause np wants shape (n, )
            linReg = LinearRegression()
            linReg.fit(self.fit_x, self.fit_y, sample_weight=weights)
            y_pred[i] = linReg.predict(x[i].reshape(-1, 1))
        return y_pred

    def gauss_kernel(self, x, sigma):
        constant = 1.0 / (sigma * np.sqrt(2 * np.pi))
        exponent = -0.5 * (x / sigma) ** 2
        return constant * np.exp(exponent)
