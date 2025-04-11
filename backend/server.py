from bottle import Bottle, request, response, hook
import json
import os.path
import datetime
import dateutil.parser
import xml.etree.ElementTree as ET
import os
from collections import namedtuple
import pandas
from daq import save_data, get_data, init_data

Config = namedtuple("Config", [
                    "company_CIF", "default_client_id", "default_client_name", "gestiune_code"])

with open(os.path.join(os.getenv("EPAPER_DATA"), "config.json"),  "r") as f:
    config = Config(**json.load(f))

dtype_dict = {
    'code': 'string',
    'name': 'string',
    'price_no_vat': 'float64',
    'vat_percent': 'float64',
    'unit': 'string'
}

all_products = pandas.read_excel(
    os.path.join(os.getenv("EPAPER_DATA"), "produse.xls"), dtype=dtype_dict, index_col="cod")

def get_product_by_code(code):
    return all_products.loc[code]

init_data()
app = Bottle()

def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.add_header('Access-Control-Allow-Origin', '*')
        response.add_header('Access-Control-Allow-Headers',
                            'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token')
        response.add_header('Access-Control-Allow-Methods',
                            'GET, POST, PUT, PATCH, OPTIONS')

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)
        else:
            response.set_header("Allow", 'GET, POST, PUT, PATCH, OPTIONS')
            return {}

    return _enable_cors

VALID_STATES = {"canceled", "in_progress", "submitted", "cashed"}

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


@app.route("/receipts", method=['OPTIONS', 'POST'])
@enable_cors
def create_receipt():
    req = request.json
    if not req or "person" not in req:
        response.status = 400
        return {"error": "Invalid data"}

    receipt = create_receipt_from_person(req["person"])
    get_data()["receipts"].append(receipt)
    save_data()
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
    return json.dumps([r for r in get_data()["receipts"] if filter_fn(r)])


@app.get("/receipts/<id:int>", method=["GET"])
@enable_cors
def get_receipt(id):
    receipt = find_receipt(id)
    if not receipt:
        response.status = 404
        return {"error": "Receipt not found"}
    return receipt

@app.get("/products/<code>", method=["GET"])
@enable_cors
def get_product(code):
    try:
        db_product = get_product_by_code(code)
    except KeyError:
        return json.dumps([])
    return json.dumps([{"cod": code, "pret_v_tva": db_product.pret_v_tva, "name": db_product.denumire, "stoc": db_product.stoc}])

def as_saga_order(receipt):
    facturi = ET.Element("Facturi")
    factura = ET.SubElement(facturi, "Factura")
    antet = ET.SubElement(factura, "Antet")
    ET.SubElement(antet, "Cod").text = config.default_client_id
    ET.SubElement(antet, "ClientNume").text = config.default_client_name
    ET.SubElement(antet, "FacturaTip").text = "B"
    ET.SubElement(antet, "FurnizorCIF").text = config.company_CIF
    todaystr = datetime.datetime.today().strftime("%d.%m.%Y")
    ET.SubElement(antet, "FacturaData").text = todaystr
    ET.SubElement(antet, "FacturaScadenta").text = todaystr
    ET.SubElement(antet, "FacturaNumar")

    detalii = ET.SubElement(factura, "Detalii")
    continut = ET.SubElement(detalii, "Continut")

    for idx, product in enumerate(receipt["products"], start=1):
        linie = ET.SubElement(continut, "Linie")
                    # <LinieNrCrt>1</LinieNrCrt>
                    # <Descriere>MAR</Descriere>
                    # <Gestiune>0001</Gestiune>
                    # <CodArticolClient>00000001</CodArticolClient>
                    # <CodBare />
                    # <InformatiiSuplimentare></InformatiiSuplimentare>
                    # <UM>BUC</UM>
                    # <Cantitate>1.000</Cantitate>
                    # <Pret>20.0000</Pret>
                    # <Valoare>20.00</Valoare>
                    # <ProcTVA>19</ProcTVA>
                    # <TVA>3.80</TVA>

        try:
            db_product = get_product_by_code(product["productCode"])
            unit, tva, name = db_product.um, db_product.tva, db_product.denumire
        except KeyError:
            print("ERROR! product not found in DB")
            unit = "BUC"
            tva = 19
            name=""

        ET.SubElement(linie, "LinieNrCrt").text = str(idx)
        # ET.SubElement(linie, "Descriere").text = name
        ET.SubElement(linie, "Gestiune").text = config.gestiune_code
        ET.SubElement(
            linie, "CodArticolClient").text = product["productCode"]
                    # <CodBare />
                    # <InformatiiSuplimentare></InformatiiSuplimentare>
        ET.SubElement(linie, "CodBare")
        ET.SubElement(linie, "InformatiiSuplimentare")
        ET.SubElement(linie, "UM").text = unit
        ET.SubElement(linie, "Cantitate").text = f"{product['quantity']}"

        ET.SubElement(linie, "Pret").text = f"{product['price']}"

        price_with_vat = float(product['price'])
        price_no_vat = price_with_vat / (1 + tva/100)
        valoare = price_no_vat*float(product["quantity"])

        ET.SubElement(linie, "Valoare").text = f"{valoare:.2f}"
        ET.SubElement(linie, "ProcTVA").text = f"{tva}"
        ET.SubElement(linie, "TVA").text = f"{valoare*tva/100:.2f}"

    ET.indent(facturi)
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
    save_data()
    return {"message": "Receipt updated"}

if __name__ == "__main__":
    app.run(host=os.getenv("EPAPER_HOST"), port=int(
        os.getenv("EPAPER_PORT")), debug=True)
    print("\nShutting down... Saving data.")
    save_data()
