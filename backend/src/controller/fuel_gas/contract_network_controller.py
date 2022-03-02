import json
import datetime
from flask import request

from src.controller import controller
from src.service import ContractNetworkService
from src.repository import ContractNetworkRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date

@controller.route(API_ROOT_PATH + 'contract_network', methods=['GET'])
def contract_network_indicator(contract_network_service: ContractNetworkService, contract_network_repository: ContractNetworkRepository):

    start_date = request.args.get('fecha_inicial', default=datetime.date.today(), type=to_date)
    end_date = request.args.get('fecha_final', default=datetime.date.today(), type=to_date)
    agent = request.args.get('agente', default=None, type=str)
    modality = request.args.get('modalidad', default='Firme', type=str)

    print('start_date:', start_date)
    print('end_date:', end_date)

    result = contract_network_service.get_graph(start_date, end_date, modality, agent, contract_network_repository)
    return json.dumps(result)
