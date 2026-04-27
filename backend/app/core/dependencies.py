from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.core.security import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> User:
    """
    dependency ที่ใช้ protect routes
    FastAPI จะเรียก finction นี้ก่อนทุก endoint ที่ใช้มัน
    ถ้า token ไม่ถูกต้องจะ return 401 
    """
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        header={"WWW-Authenticate":"Bearer"},
    )
    payload = decode_token(token)
    if payload in None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:

    """
    Dependnecy เฉพาะ admin ใช้กับ endpoint ที่ sensitive เช่นลบข้อมูล
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user