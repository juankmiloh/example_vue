
import json
import datetime
from flask import request
from . import controller

from ..service import IndicatorDateService
from ..repository import IndicatorDateRepository

from ..util.constants import API_ROOT_PATH, TIME_ZONE_CODE
from ..util.web_util import to_date

@controller.route(API_ROOT_PATH + 'indicador', methods=['GET'])
def indicator_dates(indicator_dates_service: IndicatorDateService, indicator_dates_repository: IndicatorDateRepository):
    
    indicador = request.args.get('nombre', default = None, type = str)

    result =  indicator_dates_service.get_dates_by_indicator(indicador, indicator_dates_repository)
    fecha_final = [date[0] for date in result][0]
    fecha_inicial = [date[1] for date in result][0]
    
    return json.dumps([fecha_inicial.strftime("%Y-%m-%d") + TIME_ZONE_CODE, fecha_final.strftime("%Y-%m-%d") + TIME_ZONE_CODE])
