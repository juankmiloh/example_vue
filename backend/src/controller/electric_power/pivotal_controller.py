
import json
import datetime
from flask import request

from src.controller import controller
from src.service import PivotalService
from src.repository import TRSDRepository
from src.repository import GRIPRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date

@controller.route(API_ROOT_PATH + 'pivotal', methods=['GET'])
def pivotal_indicator(pivotal_service: PivotalService, trsd_repository: TRSDRepository, grip_repository: GRIPRepository):
    
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    n_pivots = request.args.get('pivotes', default = 1, type = int)
    result = pivotal_service.get_pivotal(date, n_pivots, trsd_repository, grip_repository)
    return json.dumps(result)
