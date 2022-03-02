
import json
import datetime
from flask import request

from src.controller import controller
from src.service import OffertService
from src.repository import OffertRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date

@controller.route(API_ROOT_PATH + 'og', methods=['GET'])
def gop_indicator(offert_service: OffertService, offert_repository: OffertRepository):
    date_ini = request.args.get('fecha_incial', default = datetime.date.today(), type = to_date)
    date_fin = request.args.get('fecha_final', default = datetime.date.today(), type = to_date)
    group = request.args.get('grupo', type = str)
    region = request.args.get('region', type = str)

    result = offert_service.get_offert_by_group(date_ini, date_fin, group, region, offert_repository)
    return json.dumps(result)

