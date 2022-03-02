import datetime
import json

from flask import request

from src.controller import controller
from src.repository import FPPRepository
from src.service import FPPService
from src.util.constants import API_ROOT_PATH
from src.util.private_decorator import privateDecorator
from src.util.web_util import to_date, to_bool


@controller.route(API_ROOT_PATH + "fpp", methods=["GET"])
# @privateDecorator
def fpp_indicator(fpp_service: FPPService, fpp_repository: FPPRepository):
    start_date = request.args.get(
        "fecha_inicial", default=datetime.date.today(), type=to_date
    )
    end_date = request.args.get(
        "fecha_final", default=datetime.date.today(), type=to_date
    )
    agrupar_por_planta = request.args.get('agrupar_por_planta', default=True, type=to_bool)
    return json.dumps(fpp_service.get_fpp(start_date, end_date, agrupar_por_planta, fpp_repository))
