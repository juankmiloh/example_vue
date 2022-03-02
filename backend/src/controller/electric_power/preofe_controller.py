
import json
import datetime
from flask import abort, current_app
from flask import request

from src.controller import controller
from src.service import PreofeService
from src.repository import PreofeRepository
from src.util import constants 
from src.util.web_util import to_date
from src.util.web_util import get_last_month
from src.util.private_decorator import isPublic

@controller.route(constants.API_ROOT_PATH + 'preofe', methods=['GET'])
def index(preofe_service: PreofeService, preofe_repository: PreofeRepository):
    idplanta = request.args.get("id", default = None, type = int)
    ffinal = request.args.get("ffinal", default = datetime.date.today(), type = to_date)

    if isPublic():
        last_month = get_last_month(5)
        if last_month < ffinal:
            ffinal = last_month

    finicial = request.args.get("finicial", 
                                default = ffinal - datetime.timedelta(days = 1), 
                                type = to_date)

    result =  preofe_service.get_indicator(idplanta, finicial, ffinal, preofe_repository)
    return json.dumps(result)