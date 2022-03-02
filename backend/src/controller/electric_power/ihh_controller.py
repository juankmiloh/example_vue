
import json
import datetime
from flask import request

from src.controller import controller
from src.service import IHHService
from src.repository import IHHRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date, to_bool

@controller.route(API_ROOT_PATH + 'ihh', methods=['GET'])
def ihh_indicator(ihh_service: IHHService, ihh_repository: IHHRepository):
    
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    measure = request.args.get('medida', default = None, type = str)
    central_dipatch = request.args.get('central_dipatch', default = None, type = to_bool)
    start_date = request.args.get('fecha_inicial', default = datetime.date.today(), type = to_date)
    end_date = request.args.get('fecha_final', default = datetime.date.today(), type = to_date)

    result = ihh_service.get_market_share(date, start_date, end_date, ihh_repository, measure, central_dipatch)
    return json.dumps(result)