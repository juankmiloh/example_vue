import json
import datetime
from flask import request

from src.controller import controller
from src.service import DaggiService
from src.repository import DaggiRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date, to_bool

@controller.route(API_ROOT_PATH + 'daggi', methods=['GET'])
def daggi_indicator(daggi_service: DaggiService, daggi_repository: DaggiRepository):
    
    #Dia de inicio
    start_date = request.args.get('fecha', default = datetime.date.today(), type = to_date)

    #Para expansiones futuras del indicador
    end_date = request.args.get('fecha_final', default = start_date, type = to_date)

    print(start_date, end_date)

    #Si se calcula con la OEF
    utilizar_oef = request.args.get('utilizar_oef', default = None, type = to_bool)

    #Si se calcula como complemento al gas nacional
    utilizar_gn = request.args.get('utilizar_gn', default = None, type = to_bool)

    #Porcentaje de capacidad
    percentage_capacity = request.args.getlist('porcentaje[]', type = float)

    if (not percentage_capacity):
        percentage_capacity = None

    result = daggi_service.get_fuction_days(start_date, end_date, percentage_capacity, 
    utilizar_oef, utilizar_gn, daggi_repository)

    return json.dumps(result)

@controller.route(API_ROOT_PATH + 'daggi_percentage', methods=['GET'])
def daggi_percentage(daggi_service: DaggiService, daggi_repository: DaggiRepository):
    
    #Dia de inicio
    date = request.args.get('fecha', default = datetime.date.today(), type = to_date)

    #Dias promedios
    days = request.args.get('dias', default = 7, type = int)

    #Si se calcula con la OEF
    utilizar_oef = request.args.get('utilizar_oef', default = None, type = to_bool)

    #Si se calcula como complemento al gas nacional
    utilizar_gn = request.args.get('utilizar_gn', default = None, type = to_bool)

    #Llamamos al servicio
    result = daggi_service.get_percentage_capacity(date, days, utilizar_oef, utilizar_gn, daggi_repository)

    return json.dumps(result)