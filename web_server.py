import pymongo
import flask

app = flask.Flask(__name__)


@app.route("/")
def welcome():
    return "{status: \"OK\", error: 0, message: \"Welcome\"}"


@app.route("/monitor", methods=["GET"])
def monitor():
    client = pymongo.MongoClient("127.0.0.1", 27017)
    db = client["media_monitor"]
    result = db["sensor_raw"].find({}).sort([{"time", pymongo.DESCENDING}]).limit(1)
    result_array = [i for i in result]
    if len(result_array) == 0:
        return {
            "status": "FAIL",
            "error": 1,
            "message": "DB is empty"
        }
    else:
        del result_array[0]["_id"]
        return {
            "status": "OK",
            "error": 0,
            "data": result_array[0]
        }


@app.route("/monitor/after/<time>", methods=["GET"])
def monitor_after(time):
    client = pymongo.MongoClient("127.0.0.1", 27017)
    db = client["media_monitor"]
    result = db["sensor_raw"].find({"time": {"$gt": float(time)}})
    result_array = [i for i in result]
    if len(result_array) == 0:
        return {
            "status": "FAIL",
            "error": 1,
            "message": "DB is empty"
        }
    else:
        for i in result_array:
            del i["_id"]
        return {
            "status": "OK",
            "error": 0,
            "data": result_array
        }


@app.route("/monitor/limit/<int:cnt>", methods=["GET"])
def monitor_limit(cnt):
    client = pymongo.MongoClient("127.0.0.1", 27017)
    db = client["media_monitor"]
    result = db["sensor_raw"].find({}).sort([{"time", pymongo.DESCENDING}]).limit(cnt)
    result_array = [i for i in result]
    if len(result_array) == 0:
        return {
            "status": "FAIL",
            "error": 1,
            "message": "DB is empty"
        }
    else:
        for i in result_array:
            del i["_id"]
        return {
            "status": "OK",
            "error": 0,
            "data": result_array
        }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)