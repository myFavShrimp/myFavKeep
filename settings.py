from pydantic import BaseModel

from utils.randomizer import get_random_string


ENV = 'development'  # set to either 'development' or 'production'


# Examples
# db_url = 'postgresql://users:password@postgresserver/db'


# authjwt_cookie_secure - only allow cookies over https
# authjwt_[...]_token_expires - time until token expiration in seconds


class DevelopmentConfig(BaseModel):
    db_url: str = 'sqlite:///db.sqlite'
    host: str = '127.0.0.1'
    port: int = 8000

    debug: bool = True

    authjwt_token_location: set = ('headers', 'cookies')
    authjwt_denylist_enabled: bool = True
    authjwt_refresh_csrf_cookie_path: str = '/api/auth/refresh'

    authjwt_secret_key: str = "secret"
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
    authjwt_access_token_expires: bool = False
    authjwt_refresh_token_expires: bool = False

    authjwt_cookie_samesite: str = 'lax'


class ProductionConfig(BaseModel):
    db_url: str = 'sqlite:///db.sqlite'
    host: str = '0.0.0.0'
    port: int = 80

    debug: bool = False

    authjwt_token_location: set = ('headers', 'cookies')
    authjwt_denylist_enabled: bool = True
    authjwt_refresh_csrf_cookie_path: str = '/api/auth/refresh'

    authjwt_secret_key: str = get_random_string()
    authjwt_cookie_secure: bool = True
    authjwt_cookie_csrf_protect: bool = True
    authjwt_access_token_expires: int = 60
    authjwt_refresh_token_expires: int = 2592000

    authjwt_cookie_samesite: str = 'lax'



