import time

def get_message():
    now = int(time.time()) * 1000
    return {
        "status": "alive",
        "timestamp": now
    }