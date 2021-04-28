from fastapi import APIRouter

from api.authorization import setup_jwt
from api.endpoints.auth import auth_router
from api.endpoints.development import development_router
from api.endpoints.users.router import users_router
from utils.configurator import get_config_name

api_router = APIRouter(prefix='/api')

setup_jwt()


api_router.include_router(auth_router)
api_router.include_router(users_router)

if get_config_name() == "development":
    api_router.include_router(development_router)
