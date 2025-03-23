from bottle import Bottle, request, response, hook
import json
import os.path
import datetime
import dateutil.parser
import xml.etree.ElementTree as ET

app = Bottle()

# the decorator


# Enable CORS
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.add_header('Access-Control-Allow-Origin', '*')
        response.add_header('Access-Control-Allow-Headers', 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')
        response.add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, OPTIONS')

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)
        else:
            response.set_header("Allow", 'GET, POST, PUT, PATCH, OPTIONS')
            return {}

    return _enable_cors


DATA_FILE = "receipts.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"receipts": []}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data();

VALID_STATES = {"canceled", "in_progress", "submitted", "cashed"}

# Helper function to find a receipt by id and person
def find_receipt(id):
    return next((r for r in data["receipts"] if r["id"] == id), None)

def create_receipt_from_person(person, time=None):
    if time is None:
        time = datetime.datetime.now()
    id = max([0, *(receipt["id"] for receipt in data["receipts"])]) + 1
    number = max([0, *(receipt["number"] for receipt in data["receipts"]
                      if dateutil.parser.isoparse(receipt["date_created"]).date() == time.date())]) + 1
    return {
        "id": id, "number": number, "person": person,
        "products": [], "state": "in_progress", "date_created": time.isoformat()
    }

@app.route("/receipts", method=['OPTIONS', 'POST'])
@enable_cors
def create_receipt():
    req = request.json
    if not req or "person" not in req:
        response.status = 400
        return {"error": "Invalid data"}
    
    receipt = create_receipt_from_person(req["person"])
    data["receipts"].append(receipt)
    response.status = 201
    return {"message": "Receipt created", "receipt": receipt}

def get_filter(query):
    def todays_receipts(receipt):
        return dateutil.parser.isoparse(receipt["date_created"]).date() == datetime.datetime.today().date()
    def receipts_since_date(date):
        def filter(receipt):
            return dateutil.parser.isoparse(receipt["date_created"]).date() >= date
        return filter
    def no_filter(_):
        return True
    
    show_param = getattr(query, "show", None)    
    if show_param == "all":
        return no_filter
    elif show_param:
        try:
            date = dateutil.parser.isoparse(show_param)
            return receipts_since_date(date)
        except ValueError:
            print(f"Bad date format for show query parameter: {show_param}")

    return todays_receipts

@app.route("/receipts", methods=["GET", "OPTIONS"])
@enable_cors
def get_receipts():
    filter_fn = get_filter(request.query)
    response.content_type = "application/json"
    return json.dumps([r for r in data["receipts"] if filter_fn(r)])

@app.get("/receipts/<id:int>", method=["GET"])
@enable_cors
def get_receipt(id):
    receipt = find_receipt(id)
    if not receipt:
        response.status = 404
        return {"error": "Receipt not found"}
    return receipt

def as_saga_order(receipt):
    facturi = ET.Element("Facturi")
    factura = ET.SubElement(facturi, "Factura")
    antet = ET.SubElement(factura, "Antet")
    ET.SubElement(antet, "Cod").text = "00378"
    ET.SubElement(antet, "FurnizorCIF").text = "RO4986511"
    todaystr = datetime.datetime.today().strftime("%d.%m.%Y")
    ET.SubElement(antet, "FacturaData").text = todaystr
    ET.SubElement(antet, "FacturaScadenta").text = todaystr

    detalii = ET.SubElement(factura, "Detalii")
    continut = ET.SubElement(detalii, "Continut")
    
    for idx, product in enumerate(receipt["products"], start=1):
        linie = ET.SubElement(continut, "Linie")
        ET.SubElement(linie, "LinieNrCrt").text = str(idx)
        ET.SubElement(linie, "CodArticolFurnizor").text = product["productCode"]
        ET.SubElement(linie, "Cantitate").text = f"{product['quantity']}"
        ET.SubElement(linie, "Pret").text = f"{product['price']}"
        
    return ET.tostring(facturi, encoding="utf-8").decode("utf-8")
    
@app.get("/receipts/<id:int>/saga", method=["GET"])
@enable_cors
def get_saga_xml(id):
    receipt = find_receipt(id)
    if not receipt:
        response.status = 404
        return {"error": "Receipt not found"}
    response.headers['Content-Type'] = 'xml/application'
    fname = f"aviz_{receipt['number']}.xml"
    response.headers['Content-Disposition'] = f'attachment; filename="{fname}"'
    return as_saga_order(receipt)

@app.route("/receipts", method=["PUT", "OPTIONS"])
@enable_cors
def update_receipt():
    req = request.json
    if not req:
        response.status = 400
        return {"error": "Invalid data"}
    
    receipt = find_receipt(req["id"])
    if not receipt:
        response.status = 404
        return {"error": "Receipt not found"}
    
    if "state" in req and req["state"] not in VALID_STATES:
        response.status = 400
        return {"error": "Invalid state"}
    
    receipt.update(req)
    return {"message": "Receipt updated"}

@app.delete("/receipts/<id:int>")
def delete_receipt(id):
    receipt = find_receipt(id)
    if not receipt:
        response.status = 404
        return {"error": "Receipt not found"}
    
    data["receipts"].remove(receipt)
    return {"message": "Receipt deleted"}

if __name__ == "__main__":
    app.run(host="192.168.1.104", port=8082, debug=True)
    print("\nShutting down... Saving data.")
    save_data()
