from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_email_password(db: Session, email: str, password: str):
    return db.query(models.User).filter(
        models.User.email == email, 
        models.Users.password == password
    ).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
