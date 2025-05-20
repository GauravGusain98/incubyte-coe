from sqlalchemy.orm import Session
from coe.models.user import User
from coe.schemas.user import UserCreate, UserLogin, RemoveUser

def create_user(user: UserCreate, db: Session) -> User:
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email, 
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(loginCred: UserLogin, db: Session) -> User | None:
    user = db.query(User).filter_by(
        email=loginCred.email,
        password=loginCred.password
    ).first()

    return user

def remove_user(user_data: RemoveUser, db: Session) -> None:
    user = db.query(User).filter(User.id == user_data.id).first()
    if user:
        db.delete(user)
        db.commit()

        return True
    
    return False
