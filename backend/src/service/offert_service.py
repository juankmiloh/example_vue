import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import OffertRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class OffertService:

    def get_offert_by_group(self, date_ini, date_fin, group, region, offert_repository: OffertRepository):
        
        data = offert_repository.find_offert_by_group(date_ini, date_fin, group)
        df = pd.DataFrame(data)

        if group == "Guajira Total" and region == "Costa":
            df[1] = df[1] - pd.DataFrame(offert_repository.find_offert_by_group(date_ini, date_fin, "Guajira Interior"))[1]

        # Remover valores engativos por decimales
        #df[1] = df[1].clip(lower=0)

        if df.empty:
            return {}

        return self._format_and_serialize_df(df)

    def _format_and_serialize_df(self, df):
        indicators = []
        for index, row in df.iterrows():
            indicator = {
                'id': int(index),
		        'dates': [row[0].strftime('%Y-%m-%d')],
                'values': [float(row[1])]
            }
            indicators.append(indicator)
        return add_wrapper(indicators)
    
    def get_offert_groups(self, offert_repository: OffertRepository):        
        data = offert_repository.get_groups()
        return add_wrapper([item[0] for item in data])
