import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.product import Product
from app.models.location import Location
from app.models.inventory import Inventory
from app.models.agv import AGV

def seed():
    db = SessionLocal()
    try:
        # เช็คก่อนว่ามี data แล้วหรือยัง
        if db.query(Product).first():
            print("Seed data already exists, skipping...")
            return

        print("Seeding products...")
        products = [
            Product(sku="SKU-001", name="หน้ากากอนามัย",   weight=0.1),
            Product(sku="SKU-002", name="ถุงมือยาง",        weight=0.2),
            Product(sku="SKU-003", name="แอลกอฮอล์เจล",    weight=0.5),
            Product(sku="SKU-004", name="ชุด PPE",          weight=1.2),
            Product(sku="SKU-005", name="เทอร์โมมิเตอร์",  weight=0.3),
            Product(sku="SKU-006", name="ถุงซิปล็อค",       weight=0.1),
            Product(sku="SKU-007", name="กล่องกระดาษ",      weight=0.4),
            Product(sku="SKU-008", name="เทปกาว",           weight=0.3),
            Product(sku="SKU-009", name="ฟองน้ำกันกระแทก", weight=0.2),
            Product(sku="SKU-010", name="ป้ายบาร์โค้ด",    weight=0.05),
        ]
        db.add_all(products)
        db.flush()

        print("Seeding locations...")
        locations = []

        # Shelf locations — 3 rows x 8 cols = 24 shelves
        shelf_layout = [
            # Row A (grid row 1–2)
            ("A1",1,1),("A2",1,2),("A3",1,3),("A4",1,4),
            ("A5",2,1),("A6",2,2),("A7",2,3),("A8",2,4),
            # Row B (grid row 1–2, col 6–9)
            ("B1",1,6),("B2",1,7),("B3",1,8),("B4",1,9),
            ("B5",2,6),("B6",2,7),("B7",2,8),("B8",2,9),
            # Row C (grid row 1–2, col 11–14)
            ("C1",1,11),("C2",1,12),("C3",1,13),("C4",1,14),
            ("C5",2,11),("C6",2,12),("C7",2,13),("C8",2,14),
        ]
        for code, row, col in shelf_layout:
            locations.append(Location(code=code, zone="shelf", row=row, col=col))

        # Special zones
        locations += [
            Location(code="INBOUND-1",  zone="inbound",  row=0,  col=0),
            Location(code="INBOUND-2",  zone="inbound",  row=0,  col=1),
            Location(code="OUTBOUND-1", zone="outbound", row=11, col=13),
            Location(code="OUTBOUND-2", zone="outbound", row=11, col=14),
            Location(code="CHARGE-1",   zone="charge",   row=11, col=0),
            Location(code="CHARGE-2",   zone="charge",   row=11, col=1),
            Location(code="CHARGE-3",   zone="charge",   row=11, col=2),
        ]
        db.add_all(locations)
        db.flush()

        print("Seeding inventory...")
        shelf_locs = [l for l in locations if l.zone == "shelf"]
        for i, product in enumerate(products):
            db.add(Inventory(
                product_id=product.id,
                location_id=shelf_locs[i].id,
                quantity=50
            ))

        print("Seeding AGVs...")
        agvs = [
            AGV(name="AGV-01", state="idle", battery=100.0, current_row=11, current_col=0),
            AGV(name="AGV-02", state="idle", battery=88.0,  current_row=11, current_col=1),
            AGV(name="AGV-03", state="idle", battery=74.0,  current_row=11, current_col=2),
        ]
        db.add_all(agvs)
        db.commit()
        print("✅ Seed data created successfully!")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()