from dataclasses import dataclass
import fdb


import os


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
        tva=float(row[3]),
        den_tip=row[4],
        stoc=float(row[5]),
        grupa=row[6],
        pret_vanz=row[7],
        pret_v_tva=float(row[8]),
        is_valuta=bool(row[9]),
        cod_bare=row[10],
        cod_fe=row[11],
        cod_cpv=row[12],
        plu=row[13]
    )