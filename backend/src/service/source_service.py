import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import SourceRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper


class SourceService:
    def find_all(self, has_not_guajira_costa,
                 source_repository: SourceRepository):
        return add_wrapper([
            item[0]
            for item in source_repository.find_all(has_not_guajira_costa)
        ])

    def find_regions(self, source_repository: SourceRepository):
        regions = source_repository.find_grupo_2()
        return add_wrapper([[item[0], item[1]] for item in regions])

    def find_plants(self, source_repository: SourceRepository):
        plants = source_repository.find_plants()
        return add_wrapper([[item[0], item[1]] for item in plants])

    def find_activos(self, source_repository: SourceRepository):
        activos = source_repository.find_activos()
        return add_wrapper([[item[0], item[1]] for item in activos])

    def find_agents(self, source_repository: SourceRepository):
        agents = source_repository.find_agents()
        return add_wrapper([[item[0], item[1]] for item in agents])

    def find_causes(self, source_repository: SourceRepository):
        causes = source_repository.find_causes()
        return add_wrapper([[item[0], item[1]] for item in causes])

    def find_techs(self, source_repository: SourceRepository):
        techs = source_repository.find_techs()
        return add_wrapper([[item[0], item[1]] for item in techs])

    def find_generation_agentss(self, source_repository: SourceRepository):
        agents = source_repository.find_generation_agents()
        return add_wrapper([[item[0], item[1]] for item in agents])

    def find_generation_plants(self, source_repository: SourceRepository):
        plants = source_repository.find_generation_plants()
        return add_wrapper([[item[0], item[1]] for item in plants])

    def find_agents(self, source_repository: SourceRepository):
        agents = source_repository.find_agents()
        return add_wrapper([[item[0], item[1]] for item in agents])

    def find_sectors(self, source_repository: SourceRepository):
        sectors = source_repository.find_sectors()
        return add_wrapper([item[0] for item in sectors])
