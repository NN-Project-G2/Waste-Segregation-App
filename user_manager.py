from sqlalchemy.orm import Session
import json

import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, 
        password=user.password, 
        secret_question_answer=user.secret_question_answer
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_email_password(db: Session, email: str, password: str):
    return db.query(models.User).filter(
        models.User.email == email, 
        models.User.password == password
    ).first()


def get_user_by_email_secret_qtn_ans(db: Session, email: str, secret_qtn_ans: str):
    return db.query(models.User).filter(
        models.User.email == email, 
        models.User.secret_question_answer == secret_qtn_ans
    ).first()


def update_password(db: Session, email: str, password: str):
    db.query(models.User).filter(models.User.email == email).update(
        {
            'password': password
        }
    )
    db.commit()
    return True
