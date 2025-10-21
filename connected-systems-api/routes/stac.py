import pygeoapi.api.stac as stac_api
from pygeoapi.flask_app import api_
from quart import Blueprint, request

from util import *

stac = Blueprint('stac', __name__)


@stac.route('/stac')
async def stac_catalog_root():
    """
    STAC root endpoint

    :returns: HTTP response
    """
    return await to_response(stac_api.get_stac_root(api_, await AsyncAPIRequest.from_request(request)))


@stac.route('/stac/<path:path>')
async def stac_catalog_path(path):
    """
    STAC path endpoint

    :param path: path

    :returns: HTTP response
    """
    return await to_response(stac_api.get_stac_path(api_, await AsyncAPIRequest.from_request(request), path))
