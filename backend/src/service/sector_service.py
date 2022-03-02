import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import SectorRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class SectorService:

    def find_all(self, sector_repository: SectorRepository):
        return add_wrapper([item[0] for item in sector_repository.find_all()])
