
import json
import datetime
from flask import request

from src.controller import controller
from src.service import GRIPService
from src.repository import GRIPRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date

@controller.route(API_ROOT_PATH + 'gpgr', methods=['GET'])
def grip_indicator(grip_service: GRIPService, grip_repository: GRIPRepository):
    
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    group = request.args.get('grupo', default = None, type = str)
    id = request.args.get('id', default = None, type = str)
    if (group is not None):
        result = grip_service.get_deviation_by_group(date, grip_repository, group, id)
    else:
        result = grip_service.get_deviation(date, grip_repository)
    return json.dumps(result)
