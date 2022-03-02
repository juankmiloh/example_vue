import datetime
import json

from flask import request

from src.controller import controller
from src.repository import ICOEFRepository
from src.service import ICOEFService
from src.util.constants import API_ROOT_PATH
from src.util.private_decorator import privateDecorator
from src.util.web_util import to_date


@controller.route(API_ROOT_PATH + 'icoef', methods=['GET'])
# @privateDecorator
def icoef_indicator(icoef_service: ICOEFService,
                    icoef_repository: ICOEFRepository):

    start_date = request.args.get('fecha_inicial',
                                  default=datetime.date.today(),
                                  type=to_date)
    end_date = request.args.get('fecha_final',
                                default=datetime.date.today(),
                                type=to_date)
    period = request.args.get('periodo',
                              default="Semanal",
                              type=str)

    beta = request.args.get('beta',
                            default="2%",
                            type=str).replace("%", "")

    plants = request.args.getlist('planta[]', type=str) or []

    flip = request.args.get('invertir',
                            default="false",
                            type=str)

    flip_acc = request.args.get('anillado',
                                default="false",
                                type=str)
    
    coverage = request.args.get('covertura',
                                default="false",
                                type=str)

    no_group = request.args.get('no_agrupar',
                                default="false",
                                type=str)

    return json.dumps(
        icoef_service.get_icoef(start_date,
                                end_date,
                                period,
                                int(beta),
                                plants,
                                flip,
                                flip_acc,
                                coverage,
                                no_group,
                                icoef_repository)
    )
