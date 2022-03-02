import datetime
import json

from flask import request

from src.controller import controller
from src.repository import DPRepository
from src.service import DPService
from src.util.constants import API_ROOT_PATH
from src.util.private_decorator import privateDecorator
from src.util.web_util import to_date


@controller.route(API_ROOT_PATH + 'dp', methods=['GET'])
# @privateDecorator
def dp_indicator(dp_service: DPService,
                 dp_repository: DPRepository):
    date = request.args.get(
        'fecha',
        default=datetime.date.today(),
        type=to_date)
    
    end_date = request.args.get(
        'fecha_final',
        default=None,
        type=to_date)
    
    markets_numerator = request.args.getlist('mercados_numerador[]', type=str) or  ["Primario","Secundario"]
    markets_denominator = request.args.getlist('mercados_denominador[]',  type=str) or ["Primario", "Secundario"]
    modalities_numerator = request.args.getlist('modalidades_numerador[]',  type=str) or ["Firme", "Interrumpible"]
    modalities_denominator = request.args.getlist('modalidades_denominador[]', type=str) or ["Firme", "Interrumpible"]
    sectors_numerator = request.args.getlist('sectores_numerador[]', type=str) or ["Térmico","Comercial","Industrial"]
    sectors_denominator = request.args.getlist('sectores_denominador[]', type=str) or ["Térmico","Comercial","Industrial"]
    sources_numerador = request.args.getlist('fuentes_numerador[]', type=str) or ["BALLENA","LISAMA","MANA"]
    sources_denominator = request.args.getlist('fuentes_denominador[]', type=str) or ["BALLENA","LISAMA","MANA"]
    
    return json.dumps(
        dp_service.get_dp(
            date,
            end_date,
            markets_numerator,
            markets_denominator,
            modalities_numerator,
            modalities_denominator,
            sectors_numerator,
            sectors_denominator,
            sources_numerador,
            sources_denominator,
            dp_repository)
    )
