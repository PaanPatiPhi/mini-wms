# grid.py — แผนผัง warehouse ทั้งหมด
# ตรงกับ location table ใน database และ warehouse map บน frontend

ROWS = 12
COLS = 16

# ประเภทของแต่ละ cell
AISLE   = 0  # ทางเดิน AGV วิ่งได้
SHELF   = 1  # ชั้นวางสินค้า AGV วิ่งผ่านไม่ได้
INBOUND = 2  # จุดรับสินค้าเข้า
OUTBOUND= 3  # จุดส่งสินค้าออก
CHARGE  = 4  # จุดชาร์จแบตเตอรี่

# สร้าง grid เริ่มต้นเป็น aisle ทั้งหมด
GRID = [[AISLE] * COLS for _ in range(ROWS)]

# วาง shelf zones — ตรงกับ seed data ใน database
SHELF_CELLS = [
    # Row A (grid row 1–2, col 1–4)
    (1,1),(1,2),(1,3),(1,4),(2,1),(2,2),(2,3),(2,4),
    # Row B (grid row 1–2, col 6–9)
    (1,6),(1,7),(1,8),(1,9),(2,6),(2,7),(2,8),(2,9),
    # Row C (grid row 1–2, col 11–14)
    (1,11),(1,12),(1,13),(1,14),(2,11),(2,12),(2,13),(2,14),
    # Row D (grid row 5–6, col 1–4)
    (5,1),(5,2),(5,3),(5,4),(6,1),(6,2),(6,3),(6,4),
    # Row E (grid row 5–6, col 6–9)
    (5,6),(5,7),(5,8),(5,9),(6,6),(6,7),(6,8),(6,9),
    # Row F (grid row 5–6, col 11–14)
    (5,11),(5,12),(5,13),(5,14),(6,11),(6,12),(6,13),(6,14),
    # Row G (grid row 9–10, col 1–4)
    (9,1),(9,2),(9,3),(9,4),(10,1),(10,2),(10,3),(10,4),
    # Row H (grid row 9–10, col 6–9)
    (9,6),(9,7),(9,8),(9,9),(10,6),(10,7),(10,8),(10,9),
    # Row I (grid row 9–10, col 11–14)
    (9,11),(9,12),(9,13),(9,14),(10,11),(10,12),(10,13),(10,14),
]
for r, c in SHELF_CELLS:
    GRID[r][c] = SHELF

# วาง special zones
GRID[0][0] = INBOUND
GRID[0][1] = INBOUND
GRID[11][13] = OUTBOUND
GRID[11][14] = OUTBOUND
GRID[11][0] = CHARGE
GRID[11][1] = CHARGE
GRID[11][2] = CHARGE

def is_walkable(row: int, col: int) -> bool:
    """เช็คว่า AGV เดินผ่าน cell นี้ได้ไหม"""
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return False
    # AGV เดินได้ทุก cell ยกเว้น shelf
    return GRID[row][col] != SHELF

def get_neighbors(row: int, col: int) -> list:
    """คืน list ของ cell ที่อยู่ติดกัน (บน ล่าง ซ้าย ขวา)"""
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = row + dr, col + dc
        if is_walkable(nr, nc):
            neighbors.append((nr, nc))
    return neighbors