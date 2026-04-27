from pydantic import BaseModel, ConfigDict

class LocationRead(BaseModel):
    """
    ใช้ตอนส่งข้อมูล location กลับไปให้ frontend
    ไม่มี LocationCreate เพราะ location สร้างจาก seed data เท่านั้น
    ไม่ให้ user สร้างเองผ่าน API
    """
    model_config = ConfigDict(from_attributes=True)  
    
    id: int
    code: str    # เช่น "A1", "INBOUND-1"
    zone: str    # shelf, inbound, outbound, charge
    row: int     # ตำแหน่งบน grid
    col: int
