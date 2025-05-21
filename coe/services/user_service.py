from sqlalchemy.orm import Session
from coe.models.user import User
from coe.schemas.user import CreateUser, UserLogin, UpdateUser

def create_user(user: CreateUser, db: Session) -> User:
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

def login_user(login_cred: UserLogin, db: Session) -> User | None:
    user = db.query(User).filter_by(
        email=login_cred.email,
        password=login_cred.password
    ).first()

    return user

def update_user(user_id: int, user_data: UpdateUser, db: Session) -> bool:
    user = db.query(User).filter_by(id=user_id).first()

    if not user:
        return False

    # Use dict and setattr to dynamically update only non-None fields
    update_fields = user_data.model_dump(exclude_unset=True, exclude={"id"})
    for field, value in update_fields.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user) 

    return True

def remove_user(user_id: int, db: Session) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

        return True
    
    return False
