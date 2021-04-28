from fastapi import FastAPI
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from api.api import api_router
from database.database import Base, engine
from database.database import with_database


app = FastAPI(title='myFavKeep', description='The famous myFavKeep project!', version='0.1', docs_url='/api/docs',
              redoc_url='/api/redoc', debug=True)

Base.metadata.create_all(bind=engine)


app.include_router(api_router)


@app.on_event("startup")
@with_database
def startup_event(db):
    pass


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": [{'msg': exc.message}]}
    )


@app.exception_handler(IntegrityError)
def integrity_exception_handler(request: Request, exc: IntegrityError):
    # apply some python magic
    value = str(exc.orig)[::-1].split(".")[0][::-1]
    return JSONResponse(
        status_code=409,
        content={"detail": [{"loc": ["body", value],
                             'msg': 'already exists'}]}
    )
