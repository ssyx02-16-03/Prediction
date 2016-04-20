import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift

from PatientsFlows import TestingPredictions
from PatientsFlows.TestingPredictions import get_speeds
from elastic_api import parse_date
from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
from sklearn import neighbors
from sklearn.cross_validation import cross_val_predict, cross_val_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neural_network import MLPRegressor

from elastic_api.TimeToEventLoader import TimeToEventLoader
from elastic_api.UntriagedLoader import UntriagedLoader

start_time = "2016-03-22 12:00"
end_time = "2016-03-30 12:00"
interval = 10
start_time_min = parse_date.date_to_millis(start_time)/60000
end_time_min = (parse_date.date_to_millis(end_time)-parse_date.date_to_millis(start_time))/60000

ttt = TimeToEventLoader(start_time, end_time, 0)
ttt.set_search_triage()

X1, y1 = TestingPredictions.run(ttt)
X_plot = np.linspace(0, end_time_min, 5*24*60)[:, np.newaxis]

X2, y2, y3 = get_speeds(ttt)


untriage = UntriagedLoader(start_time, end_time, interval)
untriage.set_search_triage()
y4 = untriage.load_vector()
X4 = untriage.get_times()[:, np.newaxis]
X4 = (X4/60000-start_time_min)

wait_loader = AverageTimeWaitedLoader(start_time, end_time, interval)
wait_loader.set_search_triage()
y5 = wait_loader.load_vector()/60000
X5 = wait_loader.get_times()[:, np.newaxis]
X5 = (X5/60000-start_time_min)

model = neighbors.KNeighborsRegressor(5, weights='distance')
#model = make_pipeline(PolynomialFeatures(10), Ridge())
model.fit(X1, y1)
y1_p = model.predict(X_plot)

model.fit(X2, y2)
y2_p = model.predict(X_plot)
model.fit(X1, y3)
y3_p = model.predict(X_plot)


model.fit(X4, y4)
y4_p = model.predict(X_plot)
model.fit(X5, y5)
y5_p = model.predict(X_plot)


y6_p = shift(y1_p, 30, cval=0)
y7_p = shift(y1_p, 15, cval=0)
X = np.column_stack([y1_p, y2_p, y3_p, y4_p, y5_p, y6_p, y7_p])
y = shift(y1_p, -30, cval=0)

poly = make_pipeline(PolynomialFeatures(3), Ridge())
mpl = MLPRegressor()
poly.fit(X,y)
mpl.fit(X,y)

from sklearn.externals import joblib

joblib.dump(poly, 'poly.pkl')
joblib.dump(mpl, 'mpl.pkl')