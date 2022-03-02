
import json
import datetime
from flask import request

from src.controller import controller
from src.service import ContratService
from src.repository import ContratRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date

@controller.route(API_ROOT_PATH + 'gpin', methods=['GET'])
def ImportNational(contrat_service: ContratService, contrat_repository: ContratRepository):
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)
    source = request.args.get('fuente', type = str)

    return json.dumps(contrat_service._price_import_national(date, source, contrat_repository))
