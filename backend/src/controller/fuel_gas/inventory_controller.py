
import json
import datetime
from flask import request

from src.controller import controller
from src.service import InventoryService
from src.repository import InventoryRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date
from src.util.private_decorator import isPublic


@controller.route(API_ROOT_PATH + 'gmg-inventory', methods=['GET'])
def inventories(inventory_service: InventoryService, inventory_repository: InventoryRepository):

    start_date = request.args.get('fecha_inicial', default = datetime.date.today(), type = to_date)
    stop_date = request.args.get('fecha_final', default = datetime.date.today(), type = to_date)
    return json.dumps(inventory_service.get_by_date_range(start_date, stop_date, isPublic(), inventory_repository))
