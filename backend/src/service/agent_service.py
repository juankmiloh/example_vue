import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import AgentRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class AgentService:

    def find_all(self, agent_repository: AgentRepository):
        print(agent_repository.find_all())
        return add_wrapper([{'id': item[0], 'text': item[1]} for item in agent_repository.find_all()])
