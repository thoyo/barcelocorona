import json

from influxdb import InfluxDBClient


client = InfluxDBClient(host="influxdb", port=8086, database="barcelocorona")
DATE_KEY = "data"


def db_inserter(measurements_dictionary):
    for measurement in measurements_dictionary:
        time = measurement[DATE_KEY]
        for key in measurement:
            if key != DATE_KEY:
                point = [
                    {
                        "measurement": key,
                        "fields": {"value": measurement[key]},
                        "time": time
                    }
                ]
                client.write_points(point)


json_623z_r97q = json.load(open("data/623z-r97q.json"))
json_jj6z_iyrp = json.load(open("data/jj6z-iyrp.json"))
json_qwj8_xpvk = json.load(open("data/qwj8-xpvk.json"))
json_xuwf_dxjd = json.load(open("data/xuwf-dxjd.json"))

db_inserter(json_623z_r97q)
db_inserter(json_jj6z_iyrp)
db_inserter(json_qwj8_xpvk)
db_inserter(json_xuwf_dxjd)

