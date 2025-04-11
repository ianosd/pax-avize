import datetime
import os.path
import json

def load_data(date: datetime.date):
    data_file = os.path.join(os.getenv("EPAPER_DATA"), f"receipts_{date.strftime("%Y-%m-%d")}.json")
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            return json.load(f)
    return {"receipts": []}

data = None
data_day = None
def init_data():
    global data, data_day
    if data_day != datetime.datetime.today().date():
        data_day = datetime.datetime.today().date()
        data = load_data(data_day)

def save_data():
    init_data()
    data_file = os.path.join(os.getenv("EPAPER_DATA"), f"receipts_{datetime.datetime.today().date().strftime("%Y-%m-%d")}.json")
    with open(data_file, "w") as f:
        json.dump(data, f, indent=4)

def get_data():
    init_data()
    return data