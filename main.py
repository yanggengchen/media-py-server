import pymongo
from multiprocessing import Process, Event
import data
import time


def fetch_data(stop):
    while not stop.is_set():
        raw = data.get_data()
        client = pymongo.MongoClient("127.0.0.1", 27017)
        db = client["media_monitor"]
        db["sensor_raw"].insert_one(raw)
        client.close()
        time.sleep(10)


def daemon(stop):
    input("Press any key to stop...\n")
    stop.set()


if __name__ == "__main__":
    e = Event()
    Process(target=fetch_data, args=(e, )).start()
    daemon(e)
