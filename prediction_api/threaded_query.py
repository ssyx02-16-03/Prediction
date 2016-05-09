from threading import Thread
import numpy as np
import time


def _append(function, in_array, out_array, index):
    out_array[index] = function(in_array[index])


def threaded_query(function, times):
    threads = []
    values = np.array([None] * len(times))
    for i in range(len(times)):
        thread = Thread(
                target=_append,
                args=(function, times, values, i)
                )
        threads.append(thread)
        thread.start()
        time.sleep(0.010)  # pretty arbitrary delay, keep an eye!
    for thread in threads:
        thread.join()
    return values
