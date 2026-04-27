# pathfinder.py — หาเส้นทางสั้นที่สุดบน grid ด้วย BFS
# BFS = Breadth-First Search ค้นหาแบบกว้างก่อน
# รับประกันว่าได้เส้นทางสั้นที่สุดเสมอ

from collections import deque
from simulator.grid import get_neighbors

def bfs(
    start: tuple,       # (row, col) จุดเริ่มต้น
    goal: tuple,        # (row, col) จุดหมาย
    obstacles: list     # [(row, col)] ตำแหน่ง AGV ตัวอื่นที่ต้องหลีกเลี่ยง
) -> list:
    """
    หาเส้นทางสั้นที่สุดจาก start ไป goal
    หลีกเลี่ยง shelf และ AGV ตัวอื่น

    คืน list ของ (row, col) ตั้งแต่ start ถึง goal
    ถ้าหาไม่เจอ คืน [start, goal] แทน (fallback)
    """
    # ถ้าอยู่ที่เดิมแล้ว ไม่ต้องเดิน
    if start == goal:
        return [start]
    
    obstacle_set = set(map(tuple, obstacles))

    # queue เก็บ (current_position, path_so_far)
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (row, col), path = queue.popleft()

        for nr,nc in get_neighbors(row, col):
            if (nr,nc) in visited:
                continue
            #ข้าม cell ที่มี agv อื่นอยู่
            if (nr,nc) in obstacle_set:
                continue

            new_path = path + [(nr,nc)]

            # ถึงจุดหมายแล้ว
            if (nr,nc) == goal:
                return new_path
            
            visited.add((nr,nc))
            queue.append(((nr,nc), new_path))

    # หาเส้นทางไม่เจอ (grid blocked) - คืน fall back
    return [start,goal]