from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import schema, response_helper
from api.endpoints.users.me.router import me_router
from api.endpoints.users.user_id.router import user_id_router
from database.operations import user as user_ops
from api.authorization import jwt_authorization
from database.database import get_db


users_router = APIRouter(prefix='/users', tags=['Users'])

users_router.include_router(me_router)
users_router.include_router(user_id_router)


@users_router.post('/', response_model=schema.ReadUser, status_code=201,
                   responses=response_helper.response_409 | response_helper.response_403)
def post_user(user: schema.CreateUser,
              current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    if resp := response_helper.needs_admin(current_user):
        return resp
    if user_ops.is_username_taken(db, user.username):
        raise IntegrityError('', '', 'username')

    return user_ops.create(db, user)


@users_router.get('/', response_model=schema.PageWithUsers,
                  responses=response_helper.response_404)
def get_page_with_users(current_user: jwt_authorization = Depends(), db: Session = Depends(get_db)):
    if resp := response_helper.needs_admin(current_user):
        return resp

    users = user_ops.read_many(db)

    if resp := response_helper.is_item_empty(users):
        return resp

    return users
