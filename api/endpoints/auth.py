from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from api import schema, response_helper
from database.database import get_db
from database.operations.user import auth
from api.authorization import jwt_authorization

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/login', response_model=schema.Login, status_code=200,
                  responses=response_helper.response_401)
def post_login(login: schema.LoginUser,
               Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    login = auth(db, login)
    if not login:
        return JSONResponse(status_code=401, content={'detail': [{'msg': 'Login not correct'}]})
    access_token = Authorize.create_access_token(subject=login)
    refresh_token = Authorize.create_refresh_token(subject=login)
    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@auth_router.post('/refresh', response_model=schema.Refresh, status_code=200)
def post_refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()
    subject = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=subject)
    Authorize.set_access_cookies(access_token)
    return {'access_token': access_token}


@auth_router.post('/logout', status_code=205, description='Removes all cookies from the browser',
                  responses=response_helper.response_401)
def post_logout(Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    Authorize.unset_refresh_cookies()
    Authorize.unset_access_cookies()
