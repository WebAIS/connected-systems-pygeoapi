import pygeoapi.api.coverages as coverages_api
from pygeoapi.flask_app import api_
from quart import request, Blueprint

from util import *

coverage = Blueprint('coverage', __name__)


@coverage.route('/collections/<path:collection_id>/coverage')
async def collection_coverage(collection_id):
    """
    OGC API - Coverages coverage endpoint

    :param collection_id: collection identifier

    :returns: HTTP response
    """
    return await to_response(coverages_api.get_collection_coverage(api_, await AsyncAPIRequest.from_request(request), collection_id))
