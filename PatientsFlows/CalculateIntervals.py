import numpy as np
import matplotlib as plt
from scipy.integrate import simps


from sklearn import linear_model, neighbors
from sklearn.gaussian_process import GaussianProcess
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures

from elastic_api.TimeToEventLoader import TimeToEventLoader


start_time = "2016-03-31 17:00"
end_time = "2016-04-03 17:00"

percent_new = 0.1
percent_old = 1-percent_new

ttt = TimeToEventLoader(start_time, end_time, 0)
ttt.set_search_triage()

times = ttt.get_event_times()
ttt_times = np.column_stack(times)
ttt_times = ttt_times[np.argsort(ttt_times[:,1])]
arr_times = ttt_times[:,0]
tri_times = ttt_times[:,1]
ttt_times = (ttt_times[:,1]-ttt_times[:,0])/60000
arr_times = np.asanyarray(arr_times)[:, np.newaxis]
tri_times = np.asanyarray(tri_times)[:, np.newaxis]
print ttt_times
ttt_means = []
ttt_mean = ttt_times[0]
for i in range(0, len(tri_times), 1):
    ttt_mean = ttt_mean * percent_old + ttt_times[i] * percent_new
    ttt_means.append(ttt_mean)
'''
arr_times = arr_times[np.argsort(arr_times)]
arrivial_speeds=[]
arrivial_speeds.append(arr_times[1] - arr_times[0])
arrivial_speed = arr_times[1] - arr_times[0]
for i in range(0, len(arr_times)-1, 1):
    arrivial_speed = arrivial_speed * percent_old + (arr_times[i+1]-arr_times[i]) * percent_new
    arrivial_speeds.append(arrivial_speed)

tri_times = tri_times[np.argsort(tri_times)]
done_speeds=[]
done_speeds.append(tri_times[1] - tri_times[0])
done_speed = tri_times[1] - tri_times[0]
for i in range(0, len(tri_times)-1, 1):
    done_speed = done_speed * percent_old + (tri_times[i+1]-tri_times[i]) * percent_new
    done_speeds.append(done_speed)
'''
#arrivial_speeds = np.column_stack(arrivial_speeds)[0]/60000
#done_speeds = np.column_stack(done_speeds)[0]/60000
ttt_means = np.asarray(ttt_means)
print ttt_means

X = (tri_times-tri_times[0])/60000
X_plot = np.linspace(0, (X[len(X)-1])+60, 100)[:, np.newaxis]
#degree = 10
#model = make_pipeline(PolynomialFeatures(degree), Ridge())
#model = neighbors.KNeighborsRegressor(2, weights='distance')


# Instanciate a Gaussian Process model
gp = GaussianProcess(corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1,
                     random_start=100)

# Fit to data using Maximum Likelihood Estimation of the parameters
gp.fit(X, tri_times)


#plt.plot((arr_times-arrivial_speeds[0])/60000, 60/arrivial_speeds)
#plt.plot((tri_times-arrivial_speeds[0])/60000, 60/done_speeds)
plt.plot(X, ttt_means)
plt.plot(X_plot, gp.predict(X_plot))
#plt.plot(arr_times, arrivial_speeds-done_speeds)

plt.show()
