from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import schema, response_helper
from database.operations import user as user_ops
from database.database import get_db


development_router = APIRouter(prefix='/dev', tags=['Dev'])


@development_router.post('/', response_model=schema.ReadUser, status_code=201,
                         responses=response_helper.response_409)
def post_user(user: schema.CreateUser,
              db: Session = Depends(get_db)):
    if user_ops.is_username_taken(db, user.username):
        raise IntegrityError('', '', 'username')
    return user_ops.create(db, user)


@development_router.get('/', response_model=schema.PageWithUsers,
                        responses=response_helper.response_404)
def get_page_with_users(db: Session = Depends(get_db)):
    users = user_ops.read_many(db)
    if resp := response_helper.is_item_empty(users):
        return resp
    return users

