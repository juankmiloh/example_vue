
import json
import datetime
from flask import request

from src.controller import controller
from src.service import TRSDService
from src.repository import TRSDRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date

@controller.route(API_ROOT_PATH + 'trsd', methods=['GET'])
def icfp_indicator(trsd_service: TRSDService, icfp_repository: TRSDRepository):
    
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    result = trsd_service.get_concentration_index(date, icfp_repository)
    return json.dumps(result)