import datetime
import os.path
import json

import dateutil.parser

def load_data(date: datetime.date):
    data_file = os.path.join(os.getenv("EPAPER_DATA"), f"receipts_{date.strftime("%Y-%m-%d")}.json")
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return {"receipts": []}

_data = None
_data_day = None

def init_data():
    global _data, _data_day
    if _data_day != datetime.datetime.today().date():
        _data_day = datetime.datetime.today().date()
        _data = load_data(_data_day)

def save_data():
    init_data()
    data_file = os.path.join(os.getenv("EPAPER_DATA"), f"receipts_{datetime.datetime.today().date().strftime("%Y-%m-%d")}.json")
    with open(data_file, "w") as f:
        json.dump(_data, f, indent=4)

def get_data():
    init_data()
    return _data


# Helper function to find a receipt by id and person


def find_receipt(id):
    return next((r for r in get_data()["receipts"] if r["id"] == id), None)


def create_receipt_from_person(person, time=None):
    if time is None:
        time = datetime.datetime.now()
    id = max([0, *(receipt["id"] for receipt in get_data()["receipts"])]) + 1
    number = max([0, *(receipt["number"] for receipt in get_data()["receipts"]
                       if dateutil.parser.isoparse(receipt["date_created"]).date() == time.date())]) + 1
    return {
        "id": id, "number": number, "person": person,
        "products": [], "state": "in_progress", "date_created": time.isoformat()
    }