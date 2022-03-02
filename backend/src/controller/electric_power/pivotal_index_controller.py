
import json
import datetime
from flask import request

from src.controller import controller
from src.service import PivotalIndexService
from src.repository import PivotalIndexRepository
from src.util import constants 
from src.util.web_util import to_date

@controller.route(constants.API_ROOT_PATH + 'pivotal3d', methods=['GET'])
def pivotal3d_indicator(pivotal_index_service: PivotalIndexService, pivotal_index_repository: PivotalIndexRepository):
    agent_code = request.args.get("id", default = None, type = str)
    ffinal = request.args.get("ffinal", default = datetime.date.today(), type = to_date)
    finicial = request.args.get("finicial", 
                                default = ffinal - datetime.timedelta(days = 7),
                                type = to_date)

    result =  pivotal_index_service.get_indicator(agent_code, finicial, ffinal, pivotal_index_repository)
    return json.dumps(result)