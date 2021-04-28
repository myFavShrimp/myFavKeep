import uvicorn

from app import app
from utils.configurator import get_config

uvicorn.run(app, host=get_config().host, port=get_config().port, debug=get_config().debug)
