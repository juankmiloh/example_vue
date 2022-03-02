
import json
import datetime
from flask import request

from src.controller import controller
from src.service import ContratService
from src.repository import ContratRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date
from src.util.private_decorator import privateDecorator

@controller.route(API_ROOT_PATH + 'oc', methods=['GET'])
@privateDecorator
def offer_curve_indicator(contrat_service: ContratService, contrat_repository: ContratRepository):
    
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    
    modalidad = request.args.get('modalidad', default="Firme", type=str)

    source = request.args.getlist('fuente[]', type = str)
    market = request.args.getlist('mercado[]', type = str)
    starting_year = request.args.getlist('fecha_inicial[]', type = str)
    role = request.args.get('rol_vendedor', default = None, type = str)
    agent_type = request.args.get('tipo_agente', default = None, type = str) 

    result = contrat_service.get_offert_curve(date, contrat_repository,
        modalidad, source, market, starting_year, role, agent_type)

    return json.dumps(result)

@controller.route(API_ROOT_PATH + 'ocpbl', methods=['GET'])
def offer_curve_indicator_public(contrat_service: ContratService, contrat_repository: ContratRepository):
    
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    
    modalidad = request.args.get('modalidad', default="Firme", type=str)

    market = request.args.getlist('mercado[]', type = str)
    starting_year = request.args.getlist('fecha_inicial[]', type = str)
    role = request.args.get('rol_vendedor', default = None, type = str)
    agent_type = "vendedores"

    result = contrat_service.get_offert_curve(date, contrat_repository,
        modalidad=modalidad, market=market, starting_year=starting_year, role=role, agent_type=agent_type, public=True)
 
    return json.dumps(result)