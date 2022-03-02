import datetime
import json

from flask import request

from src.controller import controller
from src.repository import IAGRepository
from src.service import IAGService
from src.util.constants import API_ROOT_PATH
from src.util.private_decorator import privateDecorator
from src.util.web_util import to_date


@controller.route(API_ROOT_PATH + 'iag', methods=['GET'])
# @privateDecorator
def iag_indicator(iag_service: IAGService, iag_repository: IAGRepository):

    start_date = request.args.get('fecha_inicial',
                                  default=datetime.date.today(),
                                  type=to_date)
    end_date = request.args.get('fecha_final',
                                default=datetime.date.today(),
                                type=to_date)

    agents = request.args.getlist('agentes[]', type=str) or []
    techs = request.args.getlist('tecnologias[]', type=str) or []
    plants = request.args.getlist('plantas[]', type=str) or []
    causes = request.args.getlist('causas[]', type=str) or []

    time_medians_to_show = request.args.get('medias_a_mostrar',
                                            default="10",
                                            type=str)
    top_times_to_show = request.args.get('top_a_mostrar',
                                         default="10",
                                         type=str)

    return json.dumps(
        iag_service.get_iag(start_date, end_date, agents, techs, plants,
                            causes, int(time_medians_to_show),
                            int(top_times_to_show), iag_repository))