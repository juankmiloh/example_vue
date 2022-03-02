import json
import datetime
from flask import request

from src.controller import controller
from src.service import SourceService
from src.repository import SourceRepository
from src.util.constants import API_ROOT_PATH
from src.util.web_util import to_date
from src.util.private_decorator import privateDecorator


@controller.route(API_ROOT_PATH + 'fuentes', methods=['GET'])
#@privateDecorator
def sources(source_service: SourceService,
            source_repository: SourceRepository):
    has_not_guajira_costa = request.args.get('no_guajira_costa',
                                             default=False,
                                             type=bool)
    return json.dumps(
        source_service.find_all(has_not_guajira_costa, source_repository))

@controller.route(API_ROOT_PATH + 'sectores', methods=['GET'])
def sectors(source_service: SourceService,
            source_repository: SourceRepository):
    return json.dumps(source_service.find_sectors(source_repository))

@controller.route(API_ROOT_PATH + 'regiones', methods=['GET'])
def regions(source_service: SourceService,
            source_repository: SourceRepository):
    return json.dumps(source_service.find_regions(source_repository))


@controller.route(API_ROOT_PATH + 'plantas', methods=['GET'])
def plants(source_service: SourceService, source_repository: SourceRepository):
    return json.dumps(source_service.find_plants(source_repository))


@controller.route(API_ROOT_PATH + 'activos', methods=['GET'])
def activos(source_service: SourceService,
            source_repository: SourceRepository):
    return json.dumps(source_service.find_activos(source_repository))


@controller.route(API_ROOT_PATH + 'agents', methods=['GET'])
def agentes(source_service: SourceService,
            source_repository: SourceRepository):
    return json.dumps(source_service.find_agents(source_repository))


@controller.route(API_ROOT_PATH + 'causas', methods=['GET'])
def causas(source_service: SourceService, source_repository: SourceRepository):
    return json.dumps(source_service.find_causes(source_repository))


@controller.route(API_ROOT_PATH + 'tecnologias', methods=['GET'])
def tecnologias(source_service: SourceService,
                source_repository: SourceRepository):
    return json.dumps(source_service.find_techs(source_repository))


@controller.route(API_ROOT_PATH + 'agentes-generacion', methods=['GET'])
def agentes_generacion(source_service: SourceService,
                       source_repository: SourceRepository):
    return json.dumps(
        source_service.find_generation_agentss(source_repository))


@controller.route(API_ROOT_PATH + 'plantas-generacion', methods=['GET'])
def plantas_generacion(source_service: SourceService,
                       source_repository: SourceRepository):
    return json.dumps(source_service.find_generation_plants(source_repository))
