import pymongo
from multiprocessing import Process, Event
import data
import time


def fetch_data(stop):
    last_time = 0
    while not stop.is_set():
        if time.time() - last_time < 10:
            continue
        else:
            last_time = time.time()
        raw = data.get_data()
        client = pymongo.MongoClient("127.0.0.1", 27017)
        db = client["media_monitor"]
        db["sensor_raw"].insert_one(raw)
        client.close()


def web_server():
    import web_server
    web_server.run()


def daemon(stop):
    input("Press any key to stop...\n")
    stop.set()


if __name__ == "__main__":
    e = Event()
    Process(target=fetch_data, args=(e, )).start()
    web_process = Process(target=web_server)
    web_process.daemon = True
    web_process.start()
    daemon(e)
