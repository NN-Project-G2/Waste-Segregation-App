from sqlalchemy.orm import Session
import json
import jwt
from datetime import datetime, timezone, timedelta

import models, schemas


TOKEN_SECRET = "8DC532EA3EF962CBEE599BC781234"


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


def generate_token(user_email, user_id, scope='access'):
    if scope == 'refresh':
        exp_time = datetime.now(tz=timezone.utc) + timedelta(hours=24)
    else:
        exp_time = datetime.now(tz=timezone.utc) + timedelta(hours=24)

    return jwt.encode(
        {
            "email": user_email,
            "userid": user_id,
            "scope": scope,
            "exp": exp_time
        },
        TOKEN_SECRET,
        algorithm="HS256"
    )


def verify_token(access_token):
    try:
        user_data = jwt.decode(access_token, TOKEN_SECRET, algorithms=["HS256"])
        if user_data['scope'] == 'access':
            return True, {"email": user_data['email'], "userId": user_data['userid']}
        else:
            return False, None
    except jwt.ExpiredSignatureError:
        return False, None


def verify_refresh_token(refresh_token):
    try:
        token_data = jwt.decode(refresh_token, TOKEN_SECRET, algorithms=["HS256"])

        if token_data['scope'] == 'refresh':
            access_token = generate_token(token_data['email'], token_data['userid'])
            refresh_token = generate_token(token_data['email'], token_data['userid'], 'refresh')

            return True, {
                "accessToken": access_token,
                "refreshToken": refresh_token
            }
        else:
            return False, None
    except jwt.ExpiredSignatureError:
        return False, None
