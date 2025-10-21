import pygeoapi.api.environmental_data_retrieval as edr_api
from pygeoapi.flask_app import api_
from quart import request, Blueprint

from util import *

edr = Blueprint('edr', __name__)


@edr.route('/collections/<path:collection_id>/position')
@edr.route('/collections/<path:collection_id>/area')
@edr.route('/collections/<path:collection_id>/cube')
@edr.route('/collections/<path:collection_id>/radius')
@edr.route('/collections/<path:collection_id>/trajectory')
@edr.route('/collections/<path:collection_id>/corridor')
@edr.route('/collections/<path:collection_id>/locations/<location_id>')  # noqa
@edr.route('/collections/<path:collection_id>/locations')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/position')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/area')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/cube')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/radius')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/trajectory')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/corridor')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/locations/<location_id>')  # noqa
@edr.route('/collections/<path:collection_id>/instances/<instance_id>/locations')  # noqa
async def get_collection_edr_query(collection_id, instance_id=None, location_id=None):
    """
    OGC EDR API endpoints

    :param collection_id: collection identifier
    :param instance_id: instance identifier
    :param location_id: location id of a /locations/<location_id> query

    :returns: HTTP response
    """
    if location_id:
        query_type = 'locations'
    else:
        query_type = request.path.split('/')[-1]

    return await to_response(edr_api.get_collection_edr_query(
        api_, await AsyncAPIRequest.from_request(request),
        collection_id,
        instance_id, query_type,
        location_id))
