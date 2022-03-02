
import json
import datetime
from flask import request

from src.controller import controller
from src.service import ContratService
from src.repository import ContratRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date
from src.util.private_decorator import  privateDecorator

@controller.route(API_ROOT_PATH + 'gpd', methods=['GET'])
@privateDecorator
def gpd_indicator(contrat_service: ContratService, contrat_repository: ContratRepository):
    
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    group_by = request.args.getlist('agrupar[]', type = str)
    source = request.args.getlist('fuente[]', type = str)
    market = request.args.getlist('mercado[]', type = str)
    starting_year = request.args.getlist('fecha_inicial[]', type = str)
    role = request.args.get('rol_vendedor', default = None, type = str)
    agent_type = request.args.get('tipo_agente', default = None, type = str) 
    sector = request.args.getlist('sector[]', type = str)
    modality = request.args.getlist('modalidad[]', type = str)

    result = contrat_service.get_price_discrimination(date, contrat_repository,
        group_by=group_by, source=source, market=market, starting_year=starting_year, 
        agent_type=agent_type, role=role, sector=sector, modality=modality)
    return json.dumps(result)
