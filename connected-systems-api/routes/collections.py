from http import HTTPStatus

import pygeoapi.api as core_api
import pygeoapi.api.itemtypes as itemtypes_api
import pygeoapi.api.tiles as tiles_api
from pygeoapi.flask_app import api_, CONFIG
from pygeoapi.util import filter_dict_by_key_value
from quart import request, Blueprint

from api import csapi_
from util import *

collections = Blueprint('collections', __name__)


@collections.route('/collections')
@collections.route('/collections/<path:collection_id>')
async def all_collections(collection_id: str = None):
    request.collection = None
    """
    OGC API collections endpoint

    :param collection_id: collection identifier

    :returns: HTTP response
    """

    req = await AsyncAPIRequest.from_request(request)
    format = req._get_format(request.headers)

    if collection_id:
        if collection_id in filter_dict_by_key_value(CONFIG['resources'], 'type', 'collection'):
            # The collection is defined in 'resources'
            response = core_api.describe_collections(api_, req, collection_id)
        else:
            # The collection is dynamic via csapi
            print(f"HEERE {format}")
            response = await csapi_.get_collections(request,
                                                    ({}, HTTPStatus.NOT_FOUND, ""),
                                                    format,
                                                    collection_id)
    else:
        # Overwrite original request format with json so we can modify response later on and add CSAPI-entities

        request.args['f'] = "json"
        response = core_api.describe_collections(api_, await AsyncAPIRequest.from_request(request))

        # Add CSAPI-Collections to response
        print(f"original format {format}")
        response = await csapi_.get_collections(request, response, format)

    return await to_response(response)


@collections.route('/collections/<path:collection_id>/items')
@collections.route('/collections/<path:collection_id>/items/<path:item_id>')
async def collection_items(collection_id: str, item_id: str = None):
    request.collection = None

    # Resource is configured via 'resources'
    if collection_id in filter_dict_by_key_value(CONFIG['resources'], 'type', 'collection'):
        if item_id:
            response = itemtypes_api.get_collection_item(api_, await AsyncAPIRequest.from_request(request), collection_id, item_id)
        else:
            response = itemtypes_api.get_collection_items(api_, await AsyncAPIRequest.from_request(request), collection_id)
    else:
        # Resource is dynamic via csapi
        response = await csapi_.get_collection_items(request, collection_id, item_id)
    return await to_response(response)


@collections.route('/collections/<path:collection_id>/schema')
async def collection_schema(collection_id):
    """
    OGC API - collections schema endpoint

    :param collection_id: collection identifier

    :returns: HTTP response
    """
    return await to_response(core_api.get_collection_schema(api_, await AsyncAPIRequest.from_request(request), collection_id))


@collections.route('/collections/<path:collection_id>/queryables')
async def collection_queryables(collection_id=None):
    """
    OGC API collections queryables endpoint

    :param collection_id: collection identifier

    :returns: HTTP response
    """
    return await to_response(itemtypes_api.get_collection_queryables(api_, await AsyncAPIRequest.from_request(request), collection_id))


@collections.route('/collections/<path:collection_id>/tiles')
async def get_collection_tiles(collection_id=None):
    """
    OGC open api collections tiles access point

    :param collection_id: collection identifier

    :returns: HTTP response
    """
    return await to_response(tiles_api.get_collection_tiles(api_, await AsyncAPIRequest.from_request(request), collection_id))


@collections.route('/collections/<path:collection_id>/tiles/<tileMatrixSetId>')
@collections.route('/collections/<path:collection_id>/tiles/<tileMatrixSetId>/metadata')  # noqa
async def get_collection_tiles_metadata2(collection_id=None, tileMatrixSetId=None):
    """
    OGC open api collection tiles service metadata

    :param collection_id: collection identifier
    :param tileMatrixSetId: identifier of tile matrix set

    :returns: HTTP response
    """
    return await to_response(tiles_api.get_collection_tiles_metadata(api_, await AsyncAPIRequest.from_request(request), collection_id, tileMatrixSetId))


@collections.route('/collections/<path:collection_id>/tiles/\
<tileMatrixSetId>/<tileMatrix>/<tileRow>/<tileCol>')
async def get_collection_tiles_data(collection_id=None, tileMatrixSetId=None,
                                    tileMatrix=None, tileRow=None, tileCol=None):
    """
    OGC open api collection tiles service data

    :param collection_id: collection identifier
    :param tileMatrixSetId: identifier of tile matrix set
    :param tileMatrix: identifier of {z} matrix index
    :param tileRow: identifier of {y} matrix index
    :param tileCol: identifier of {x} matrix index

    :returns: HTTP response
    """
    return await to_response(tiles_api.get_collection_tiles_data(
        api_, await AsyncAPIRequest.from_request(request),
        collection_id, tileMatrixSetId, tileMatrix, tileRow, tileCol))


@collections.route('/collections/<collection_id>/map')
@collections.route('/collections/<collection_id>/styles/<style_id>/map')
async def collection_map(collection_id, style_id=None):
    """
    OGC API - Maps map render endpoint

    :param collection_id: collection identifier
    :param style_id: style identifier

    :returns: HTTP response
    """

    headers, status_code, content = api_.get_collection_map(
        request, collection_id, style_id)

    response = make_response(content, status_code)

    if headers:
        response.headers = headers

    return response
