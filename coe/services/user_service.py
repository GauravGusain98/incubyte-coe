from sqlalchemy.orm import Session
from coe.models.user import User
from coe.schemas.user import UserCreate

def create_user(user: UserCreate, db: Session) -> User:
    db_user = User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user