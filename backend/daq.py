import datetime
import os
import os.path
import sqlite3
import json

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
