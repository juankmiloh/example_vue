import pandas as pd
import datetime
from flask import abort
from ..repository import TRSDRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class TRSDService:

    IIH_THRESHOLD = 1800
    TOP = 5

    def get_concentration_index(self, date, trsd_repository: TRSDRepository):
        print("---->>>>>>>>>>>>>")
        data = trsd_repository.find_by_agent(date)
        df = pd.DataFrame(data)
        if df.empty:
            return {}

        df['percentage'] = df[2] * 100 / df[2].sum()
        value = float((df['percentage']**2).sum())
        status = value > self.IIH_THRESHOLD
        df['status'] = 0
        if status:
            df.loc[df['percentage'] >= df['percentage'][self.TOP - 1], 'status'] = 1

        indicator = self._serialize_df(df)
        indicator['value'] = value
        indicator['status'] = status

        return indicator

    def find_capacity_by_plant(self, date, trsd_repository: TRSDRepository):

        data = trsd_repository.find_by_plant(date)
        return self.serialice_data(data)
        
    def _serialize_df(self, df):
        indicators = []
        for index, row in df.iterrows():
            indicator = {
                'id': row[0],
                'names': [row[1]],
                'values': [float(row['percentage'])],
                'status': int(row['status'])
            }
            indicators.append(indicator)
        return add_wrapper(indicators)

