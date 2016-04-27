import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift

from PatientsFlows import RealTimeWait
from elastic_api import parse_date
from elastic_api.AverageTimeWaitedLoader import AverageTimeWaitedLoader
from sklearn import neighbors
from sklearn.cross_validation import cross_val_predict, cross_val_score
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib


from elastic_api.TimeToEventLoader import TimeToEventLoader
from elastic_api.UntriagedLoader import UntriagedLoader

def get_uniform_axes(X, y, method):
    method.fit(X, y)
    return method.predict(X_plot)

def fit_and_save_model(model, X_, y_, name):
    model.fit(X_, y_)
    joblib.dump(model, name + '.pkl')

def save_data(X, y, min_shift):
    joblib.dump(X, str(min_shift) + 'X.pkl')
    joblib.dump(y, str(min_shift) + 'y.pkl')

start_time = "2016-03-25 12:00"
end_time = "2016-03-30 12:00"
interval = 10
start_time_min = parse_date.date_to_millis(start_time)/60000
end_time_min = (parse_date.date_to_millis(end_time)-parse_date.date_to_millis(start_time))/60000
X_plot = np.linspace(0, end_time_min, 5*24*60)[:, np.newaxis]

def create_model(min_shift):
    ttt = TimeToEventLoader(start_time, end_time, 0)
    ttt.set_search_triage()
    arr, tri, wait, real = RealTimeWait.moving_average(ttt)
    tri = np.asarray(tri)
    tri = tri/60000-start_time_min
    arr = np.asarray(arr)
    arr = arr/60000-start_time_min
    speed_arr, speed_tri = RealTimeWait.get_speeds(ttt)
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

    print 'All data picked up, transforming it to uniform axes'
    model = neighbors.KNeighborsRegressor(5, weights='distance')
    y1_p = get_uniform_axes(tri, wait, model)
    y2_p = get_uniform_axes(arr, speed_arr, model)
    y3_p = get_uniform_axes(tri, speed_tri, model)
    y4_p = get_uniform_axes(X4, y4, model)
    y5_p = get_uniform_axes(X5, y5, model)
    y6_p = shift(y1_p, min_shift, cval=0)
    y7_p = shift(y1_p, min_shift/2, cval=0)

    X = np.column_stack([y1_p, y2_p, y3_p, y4_p, y5_p, y6_p, y7_p])
    y = shift(y1_p, -min_shift, cval=0)
    save_data(X, y, min_shift)

    poly = make_pipeline(PolynomialFeatures(3), Ridge())
    fit_and_save_model(poly, X, y, str(min_shift) + 'poly')
    mpl = MLPRegressor()
    fit_and_save_model(mpl, X, y, str(min_shift) + 'mpl')

create_model(60)
create_model(50)
create_model(40)
create_model(30)
create_model(20)
create_model(10)
create_model(0)