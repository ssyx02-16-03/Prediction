import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import shift

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

percent_new = 0.1
percent_old = 1-percent_new

def run(loader):

    times = loader.get_event_times()
    both_times = np.column_stack(times)
    both_times = both_times[np.argsort(both_times[:,1])]
    arr_times = both_times[:,0]
    event_times = both_times[:,1]
    wait_times = (both_times[:,1]-both_times[:,0])/60000
    arr_times = np.asanyarray(arr_times)[:, np.newaxis]
    event_times = np.asanyarray(event_times)[:, np.newaxis]

    wait_means = []
    wait_mean = wait_times[0]
    for i in range(0, len(event_times), 1):

        wait_mean = wait_mean * percent_old + wait_times[i] * percent_new
        wait_means.append(wait_mean)

    wait_means = np.asarray(wait_means)

    X = (event_times-event_times[0])/60000
    return X, wait_means

def get_speeds(loader):

    times = loader.get_event_times()
    both_times = np.column_stack(times)
    both_times = both_times[np.argsort(both_times[:,1])]
    arr_times = both_times[:,0]
    event_times = both_times[:,1]

    arr_times = arr_times[np.argsort(arr_times)]
    arrivial_speeds=[]
    arrivial_speeds.append(arr_times[1] - arr_times[0])
    arrivial_speed = arr_times[1] - arr_times[0]
    for i in range(0, len(arr_times)-1, 1):
        arrivial_speed = arrivial_speed * percent_old + (arr_times[i+1]-arr_times[i]) * percent_new
        arrivial_speeds.append(arrivial_speed)

    tri_times = event_times[np.argsort(event_times)]
    done_speeds=[]
    done_speeds.append(tri_times[1] - tri_times[0])
    done_speed = tri_times[1] - tri_times[0]
    for i in range(0, len(tri_times)-1, 1):
        done_speed = done_speed * percent_old + (tri_times[i+1]-tri_times[i]) * percent_new
        done_speeds.append(done_speed)
    arrivial_speeds = np.asarray(arrivial_speeds)
    done_speeds = np.asarray(done_speeds)
    arr_times = np.asarray(arr_times)[:, np.newaxis]
    X = (arr_times-arr_times[0])/60000
    return X, arrivial_speeds/60000, done_speeds/60000


start_time = "2016-03-24 12:00"
end_time = "2016-03-29 12:00"
interval = 5
start_time_min = parse_date.date_to_millis(start_time)/60000
end_time_min = (parse_date.date_to_millis(end_time)-parse_date.date_to_millis(start_time))/60000

ttt = TimeToEventLoader(start_time, end_time, 0)
ttt.set_search_triage()
X1, y1 = run(ttt)
X_plot = np.linspace(0, end_time_min, 5*24*60)[:, np.newaxis]
X2, y2, y3 = get_speeds(ttt)

'''
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
'''
model = neighbors.KNeighborsRegressor(5, weights='distance')
#model = make_pipeline(PolynomialFeatures(10), Ridge())
model.fit(X1, y1)
y1_p = model.predict(X_plot)

model.fit(X2, y2)
y2_p = model.predict(X_plot)
model.fit(X1, y3)
y3_p = model.predict(X_plot)

'''
model.fit(X4, y4)
y4_p = model.predict(X_plot)
model.fit(X5, y5)
y5_p = model.predict(X_plot)
'''

y6_p = shift(y1_p, -30, cval=0)
y7_p = shift(y1_p, -15, cval=0)
X = np.column_stack([X_plot, y1_p, y2_p, y3_p, y6_p, y7_p])
y = shift(y1_p, 30, cval=0)

#poly = make_pipeline(PolynomialFeatures(3), Ridge())
mpl = MLPRegressor(beta_1=0.99)
'''
y_t = y[-1000:-2]
y = y[0:-1000]
X_t = X[-1000:-2]
X = X[0:-1000]
mpl.fit(X, y)
poly.fit(X, y)
mpl_pred = mpl.predict(X_t)
poly_pred = poly.predict(X_t)
'''
mpl_pred = cross_val_predict(mpl, X, y, cv=10)
#poly_pred = cross_val_predict(poly, X, y, cv=10)
#nn_pred = cross_val_predict(model, X, y, cv=10)
print mpl.get_params()

def plot_cross():
    fig, ax = plt.subplots()
    ax.scatter(y, mpl_pred, c='b', marker='x')
#    ax.scatter(y, poly_pred, c='y', marker ='+')
    #ax.scatter(y, nn_pred, c='r')
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel('Measured')
    ax.set_ylabel('Predicted')
    plt.show()

#mpl_pred = shift(mpl_pred, 30, cval=0)
#poly_pred = shift(poly_pred, 30, cval=0)

def plot_time():
    X = X_plot
#    plt.plot(X, y6_p, c='blue')
#    plt.plot(X, mpl_pred, c='red')
#    plt.plot(X, poly_pred, c='cyan')
    plt.plot(X_plot, y1_p, c='green')
    plt.plot(X_plot, y2_p)
    plt.plot(X_plot, y3_p)
    plt.show()
plot_time()

'''
gp.fit(X, y)
y_pred = gp.predict(X)

fig = plt.figure()
plt.plot(X_plot, y, 'r', label=u'ttt')
plt.plot(X_plot, y_pred, 'b', label=u'Prediction')
plt.legend(loc='upper left')
plt.show()


from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcess
from sklearn.gaussian_process.kernels \
    import RBF, WhiteKernel, RationalQuadratic, ExpSineSquared
from sklearn.datasets import fetch_mldata

# Kernel with optimized parameters
k1 = 50.0**2 * RBF(length_scale=50.0)  # long term smooth rising trend
k2 = 2.0**2 * RBF(length_scale=100.0) \
     * ExpSineSquared(length_scale=1.0, periodicity=10.0)  # seasonal component
# medium term irregularities
k3 = 0.5**2 * RationalQuadratic(length_scale=1.0, alpha=1.0)
k4 = 0.1**2 * RBF(length_scale=0.1) \
     + WhiteKernel(noise_level=0.1**2,
                   noise_level_bounds=(1e-3, np.inf))  # noise terms
kernel = k1 + k2 + k3 + k4

gp = GaussianProcessRegressor(kernel=kernel, alpha=0,
                              normalize_y=True)
gp.fit(X, y)

X_ = np.linspace(X.min(), X.max() + 60, 1000)[:, np.newaxis]
y_pred, y_std = gp.predict(X_, return_std=True)

# Illustration
plt.scatter(X, y, c='k')
plt.plot(X_, y_pred)
#plt.plot(v_x, v)
plt.fill_between(X_[:, 0], y_pred - y_std, y_pred + y_std,
                 alpha=0.5, color='k')
plt.xlim(X_.min(), X_.max())
plt.tight_layout()
plt.show()
'''
