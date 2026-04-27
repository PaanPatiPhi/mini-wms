from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    สมัครสมาชิกใหม่
    เช็คว่า email ซ้ำไหมก่อน แล้วค่อย hash password แล้วบันทึก
    """
    # เช็ค email ซ้ำ
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),  # hash ก่อนเก็บเสมอ
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login แล้วรับ JWT token กลับมา
    ใช้ OAuth2PasswordRequestForm เพราะ Swagger จะสร้าง login form ให้อัตโนมัติ
    form_data.username คือ email ที่กรอกมา
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # สร้าง token โดยใส่ email และ role ลงไปข้างใน
    token = create_access_token(data={
        "sub": user.email,
        "role": user.role
    })
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def get_me(db: Session = Depends(get_db)):
    """
    ดูข้อมูล user ของตัวเอง
    """
    pass