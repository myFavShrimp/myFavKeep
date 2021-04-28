from sqlalchemy import func
from sqlalchemy.orm import Session

from api import schema
from database.models import User
from database.operations import read_list, read_item, clean_dict
from database.utils.crypt import encode_pw, check_pw


def auth(db: Session, login: schema.LoginUser):
    """
    :return: user.id if the login is correct, False if not
    """
    db_user = db.query(User).filter_by(username=login.username).first()
    if db_user and check_pw(login.password, db_user.password_hash):
        return db_user.id
    return False


def create(db: Session, user: schema.CreateUser):
    password_hash = encode_pw(user.password)
    db_user = User(username=user.username, password_hash=password_hash, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_by_id(db: Session, user: schema.UserId):
    query = db.query(User).filter_by(id=user.id)
    return read_item(query)


def read_many(db: Session):
    query = db.query(User)
    return read_list(query)


def update(db: Session, user_id: int, user: schema.UpdateUser):
    db_user_query = db.query(User).filter_by(id=user_id)

    updated_data = user.dict()
    if password := user.password:
        del updated_data['password']
        updated_data['password_hash'] = encode_pw(password)

    updated_data = clean_dict(updated_data)
    db_user_query.update(updated_data)

    db_user = db.query(User).filter_by(id=user_id).first()

    db.commit()
    return db_user


def delete_by_id(db: Session, user_id: int):
    db.query(User).filter(User.id == user_id).delete()
    db.commit()


def is_username_taken(db: Session, username: str, user_id: int = 0):
    """
    Case insensitive check, if the username is already taken
    :param db:
    :param username:
    :param user_id: if a user checks, his database entry can be ignored
    e.g. to enable him to change the spelling of his username
    :return: bool, True if the name is already taken
    """
    if user_id:
        if user := db.query(User).filter(func.lower(User.username) == func.lower(username)).first():
            if not user.id == user_id:
                return True
    elif db.query(User).filter(func.lower(User.username) == func.lower(username)).first():
        return True
    return False
