import json
import logging
import time

from influxdb import InfluxDBClient
import requests

logging.basicConfig(format="%(asctime)s %(levelname)-8s %(message)s",
                    level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")

client = InfluxDBClient(host="influxdb", port=8086, database="barcelocorona")
DATE_KEY = "data"
DATA_SOURCES = ["623z-r97q"]
# DATA_SOURCES = ["623z-r97q", "jj6z-iyrp", "qwj8-xpvk", "xuwf-dxjd"]
TIME_SLEEP = 3600
RESOURCE_URL = "https://analisi.transparenciacatalunya.cat/resource"


def db_inserter(measurements_dictionary):
    for measurement in measurements_dictionary:
        time = measurement[DATE_KEY]
        for key in measurement:
            if key != DATE_KEY:
                point = [
                    {
                        "measurement": key,
                        "fields": {"value": int(measurement[key])},
                        "time": time
                    }
                ]
                client.write_points(point)


def get_measurements(source):
    response = requests.get(f"{RESOURCE_URL}/{source}.json")
    if not response.ok:
        return None
    return response.json()


def check_if_updated(source, measurements_dictionary):
    try:
        with open(f"data/{source}.json", "r+") as f:
            if json.load(f) == measurements_dictionary:
                return False
    except FileNotFoundError:
        logging.info(f"First iteration, file for {source} will be created")
    with open(f"data/{source}.json", "w") as f:
        json.dump(measurements_dictionary, f)
    return True


def loop_forever():
    while True:
        for source in DATA_SOURCES:
            logging.info(f"Updating source {source}")
            measurements_dictionary = get_measurements(source)
            if not measurements_dictionary:
                logging.error(f"Couldn't get data for source {source}")
                break
            updated = check_if_updated(source, measurements_dictionary)
            if not updated:
                logging.info(f"Source {source} retrieved but not updated, already up to date")
                break
            db_inserter(measurements_dictionary)
            logging.info(f"Source {source} updated")
        logging.info(f"Sleeping for {TIME_SLEEP} seconds")
        time.sleep(TIME_SLEEP)


if __name__ == "__main__":
    loop_forever()
