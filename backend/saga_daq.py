from dataclasses import dataclass
import fdb


import os


@dataclass
class Product:
    cod: str
    denumire: str
    um: str
    tva: float
    stoc: float
    pret_v_tva: float


def get_product_by_code(code):
    # Connect to the Firebird database
    conn = fdb.connect(
        dsn=os.getenv("FIREBIRD_DSN"),
        user=os.getenv("FIREBIRD_USER"),
        password=os.getenv("FIREBIRD_PASSWORD")
    )
    cursor = conn.cursor()

    # Query the product by code
    cursor.execute("SELECT cod,denumire,um,tva,stoc,pret_v_tva FROM ARTICOLE WHERE cod = ?", (code,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise ValueError(f"Product with code {code} not found in Firebird database.")

    # Map the row to the Product dataclass
    return Product(
        cod=row[0],
        denumire=row[1],
        um=row[2],
        tva=float(row[3]),
        stoc=float(row[4]),
        pret_v_tva=float(row[5])
    )