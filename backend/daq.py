import datetime
import os
import os.path
import sqlite3
import json
import fdb

from backend.server import dtype_dict

import pandas
from dataclasses import dataclass

DB_FILE = os.path.join(os.getenv("EPAPER_DATA"), "receipts.db")


def init_db():
    """Initialize the SQLite database and create the receipts table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER,
            person TEXT,
            products TEXT,
            state TEXT,
            date_created TEXT
        )
    """)
    conn.commit()
    conn.close()


def create_receipt(person):
    """Create a new receipt for a person. The id and number are auto-incremented by the database."""
    time = datetime.datetime.now()

    receipt = {
        "person": person,
        "products": json.dumps([{"productCode": "", "quantity": "", "price": ""}]),  # Store products as a JSON string
        "state": "in_progress",
        "date_created": time.isoformat()
    }

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Insert the receipt into the database
    cursor.execute("""
        INSERT INTO receipts (person, products, state, date_created)
        VALUES (?, ?, ?, ?)
    """, (receipt["person"], receipt["products"], receipt["state"], receipt["date_created"]))

    # Get the auto-incremented id and number
    receipt_id = cursor.lastrowid
    cursor.execute("""
        UPDATE receipts
        SET number = (
            SELECT IFNULL(MAX(number), 0) + 1
            FROM receipts
            WHERE date(date_created) = date(?)
        )
        WHERE id = ?
    """, (receipt["date_created"], receipt_id))

    conn.commit()

    # Add the id and number to the receipt object
    receipt["id"] = receipt_id
    cursor.execute("SELECT number FROM receipts WHERE id = ?", (receipt_id,))
    receipt["number"] = cursor.fetchone()[0]  # Fetch the updated number
    receipt["products"] = json.loads(receipt["products"])  # Convert back to list
    conn.close()

    return receipt


def update_receipt(receipt):
    """Save an existing receipt to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE receipts
        SET person = ?, products = ?, state = ?, date_created = ?
        WHERE id = ?
    """, (receipt["person"], json.dumps(receipt["products"]), receipt["state"], receipt["date_created"], receipt["id"]))
    conn.commit()
    conn.close()


def get_receipts():
    """Retrieve all receipts from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts")
    rows = cursor.fetchall()
    conn.close()

    # Convert rows to a list of dictionaries
    return [
        {
            "id": row[0],
            "number": row[1],
            "person": row[2],
            "products": json.loads(row[3]),
            "state": row[4],
            "date_created": row[5]
        }
        for row in rows
    ]


def find_receipt(id):
    """Find a receipt by its id."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receipts WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "number": row[1],
            "person": row[2],
            "products": json.loads(row[3]),
            "state": row[4],
            "date_created": row[5]
        }
    return None


# Initialize the database when the module is loaded
init_db()

all_products = pandas.read_excel(
    os.path.join(os.getenv("EPAPER_DATA"), "produse.xls"), dtype=dtype_dict, index_col="cod")

@dataclass
class Product:
    cod: str
    denumire: str
    um: str
    tva: float
    den_tip: str
    stoc: float
    grupa: str
    pret_vanz: float
    pret_v_tva: float
    is_valuta: bool
    cod_bare: str
    cod_fe: str
    cod_cpv: str
    plu: str

def get_product_by_code(code):
    # Connect to the Firebird database
    conn = fdb.connect(
        dsn=os.getenv("FIREBIRD_DSN"),
        user=os.getenv("FIREBIRD_USER"),
        password=os.getenv("FIREBIRD_PASSWORD")
    )
    cursor = conn.cursor()

    # Query the product by code
    cursor.execute("SELECT * FROM ARTICOLE WHERE cod = ?", (code,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"Product with code {code} not found in Firebird database.")

    # Map the row to the Product dataclass
    return Product(
        cod=row[0],
        denumire=row[1],
        um=row[2],
        tva=row[3],
        den_tip=row[4],
        stoc=row[5],
        grupa=row[6],
        pret_vanz=row[7],
        pret_v_tva=row[8],
        is_valuta=bool(row[9]),
        cod_bare=row[10],
        cod_fe=row[11],
        cod_cpv=row[12],
        plu=row[13]
    )