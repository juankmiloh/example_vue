import datetime
import json

from flask import request

from src.controller import controller
from src.repository import RCRepository
from src.service import RCService
from src.util.constants import API_ROOT_PATH
from src.util.private_decorator import privateDecorator
from src.util.web_util import to_date


@controller.route(API_ROOT_PATH + 'rc', methods=['GET'])
# @privateDecorator
def rc_indicator(rc_service: RCService,
                 contrat_repository: RCRepository):
    start_date = request.args.get('fecha_inicial',
                                  default=datetime.date.today(),
                                  type=to_date)
    end_date = request.args.get('fecha_final',
                                default=datetime.date.today(),
                                type=to_date)
    return json.dumps(
        rc_service.get_regasification_cost(start_date,
                                           end_date,
                                           contrat_repository)
    )
