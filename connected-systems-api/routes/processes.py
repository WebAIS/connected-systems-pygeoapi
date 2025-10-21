import pygeoapi.api.processes as processes_api
from pygeoapi.flask_app import api_
from quart import Blueprint, request

from util import to_response, AsyncAPIRequest

oapip = Blueprint('oapip', __name__)


@oapip.route('/processes')
@oapip.route('/processes/<process_id>')
async def get_processes(process_id=None):
    """
    OGC API - Processes description endpoint

    :param process_id: process identifier

    :returns: HTTP response
    """
    return await to_response(processes_api.describe_processes(api_, await AsyncAPIRequest.from_request(request), process_id))


@oapip.route('/jobs')
@oapip.route('/jobs/<job_id>', methods=['GET', 'DELETE'])
async def get_jobs(job_id=None):
    """
    OGC API - Processes jobs endpoint

    :param job_id: job identifier

    :returns: HTTP response
    """

    if job_id is None:
        return await to_response(processes_api.get_jobs(api_, await AsyncAPIRequest.from_request(request)))
    else:
        if request.method == 'DELETE':  # dismiss job
            return await to_response(processes_api.delete_job(api_, await AsyncAPIRequest.from_request(request), job_id))
        else:  # Return status of a specific job
            return await to_response(processes_api.get_jobs(api_, await AsyncAPIRequest.from_request(request), job_id))


@oapip.route('/processes/<process_id>/execution', methods=['POST'])
async def execute_process_jobs(process_id):
    """
    OGC API - Processes execution endpoint

    :param process_id: process identifier

    :returns: HTTP response
    """
    return await to_response(processes_api.execute_process(api_, await AsyncAPIRequest.from_request(request), process_id))


@oapip.route('/jobs/<job_id>/results',
             methods=['GET'])
async def get_job_result(job_id=None):
    """
    OGC API - Processes job result endpoint

    :param job_id: job identifier

    :returns: HTTP response
    """
    return await to_response(processes_api.get_job_result(api_, await AsyncAPIRequest.from_request(request), job_id))
