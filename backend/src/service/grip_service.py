import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import GRIPRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class GRIPService:

    DEVIATION_THRESHOLD = 5
    DAYS = 30
    DAYS_THRESHOLD = 3
    BY_PLANT = "planta"
    BY_AGENT = "agente"

    def get_deviation(self, end_date, grip_repository: GRIPRepository):
        
        star_date = end_date - datetime.timedelta(days=self.DAYS)
        data = grip_repository.find_accumulated(star_date, end_date)
        df = pd.DataFrame(data)
        if df.empty:
            return {}

        df['deviation'] = (df[2] - df[1]).abs() / df[2] * 100
        df['status'] = df['deviation'] > self.DEVIATION_THRESHOLD

        value = int(df['status'].astype(int).sum())
        if value == 0:
            status = 0
        elif value > 0 and value <= self.DAYS_THRESHOLD:
            status = 1
        else:
            status = 2

        indicator = self._serialize_df(df)
        indicator['value'] = value
        indicator['status'] = status 
        return indicator
    
    def _serialize_df(self, df):
        indicators = []
        for index, row in df.iterrows():
            indicator = {
                'id': row[0].strftime('%Y-%m-%d'),
                'names': [row[1]],
		        'dates': [row[0].strftime('%Y-%m-%d')],
                'values': [float(row['deviation'])],
                'status': int(row['status'])
            }
            indicators.append(indicator)
        return add_wrapper(indicators)

    def get_deviation_by_group(self, end_date, grip_repository: GRIPRepository, group = None, id = None):

        data = []
        if (group == self.BY_PLANT):
            if (id is not None):
                star_date = end_date - datetime.timedelta(days=self.DAYS)
                data = grip_repository.find_accumulated_by_plant_id(star_date, end_date, id)
            else:
                data = grip_repository.find_accumulated_by_plant(end_date, end_date)
        elif (group == self.BY_AGENT):
            if (id is not None):
                star_date = end_date - datetime.timedelta(days=self.DAYS)
                data = grip_repository.find_accumulated_by_agent_id(star_date, end_date, id)
            else:
                data = grip_repository.find_accumulated_by_agent(end_date, end_date)
        else:
            abort(400)

        df = pd.DataFrame(data)
        if df.empty:
            return {}

        df['deviation'] = (df[5] - df[4]).abs() / df[5] * 100
        df['status'] = df['deviation'] > self.DEVIATION_THRESHOLD

        indicator = self._transform_and_serialize_df(df)          
        return indicator

    def _transform_and_serialize_df(self, df):
        df.fillna(0, inplace=True)
        df.replace([np.inf, -np.inf], 0, inplace=True)
        df = df.groupby([2,0,1]).agg(pd.Series.tolist)
        #df.sort_index(inplace=True)
        indicators = []
        for index, row in df.iterrows():
            indicator = {
                'id': index[1],
                'names': [index[2], index[1]],
		        'dates': [date.strftime('%Y-%m-%d') for date in row[3]],
                'values': row['deviation'],
                'status': [ int(i) for i in row['status']]
            }
            indicators.append(indicator)
        return add_wrapper(indicators)