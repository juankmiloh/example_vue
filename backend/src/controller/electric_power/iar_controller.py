import datetime
import json

from flask import request

from src.controller import controller
from src.repository import IARRepository
from src.service import IARService
from src.util.constants import API_ROOT_PATH
from src.util.private_decorator import privateDecorator
from src.util.web_util import to_date


@controller.route(API_ROOT_PATH + 'iar', methods=['GET'])
# @privateDecorator
def iar_indicator(iar_service: IARService, iar_repository: IARRepository):

    start_date = request.args.get('fecha_inicial',
                                  default=datetime.date.today(),
                                  type=to_date)
    end_date = request.args.get('fecha_final',
                                default=datetime.date.today(),
                                type=to_date)

    to_show = request.args.get('resultados', default="10", type=str)

    agents = request.args.getlist('agente[]', type=str) or []

    group_by_agent = request.args.get('agrupar_por_agente',
                                      default="false",
                                      type=str)

    return json.dumps(
        iar_service.get_iar(start_date, end_date, int(to_show), agents,
                            group_by_agent, iar_repository))
