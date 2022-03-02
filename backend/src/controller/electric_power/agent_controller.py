
import json
import datetime
from flask import request

from src.controller import controller
from src.service import AgentService
from src.repository import AgentRepository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date

@controller.route(API_ROOT_PATH + 'agentes', methods=['GET'])
def agents(agent_service: AgentService, agent_repository: AgentRepository):
    return json.dumps(agent_service.find_all(agent_repository))

