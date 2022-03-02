import pandas as pd
import datetime
from flask import abort
from ..repository import IHHRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class IHHService:

    IIH_THRESHOLD = 1800
    MS_THRESHOLDS = [25, 30]
    MEASURE_ALL = "ihh"
    CAPACITY_MEASURE = "capacidad"
    GENERATION_MEASURE = "generacion"
    REAL_DIPONIBILITY_MEASURE = "realDisponibility"
    DECLARED_DIPONIBILITY_MEASURE = "declaredDisponibility"

    def get_market_share(self, date, start_date, end_date, ihh_repository: IHHRepository, measure = "capacidad", central_dipatch = False):

        if measure == self.CAPACITY_MEASURE:
            data = ihh_repository.find_capacity_by_agent(date)
        elif measure == self.GENERATION_MEASURE:
            data = ihh_repository.find_generation_by_agent(date) 
        elif measure == self.REAL_DIPONIBILITY_MEASURE:
            data = ihh_repository.find_real_disponibility_by_agent(date)
        elif measure == self.DECLARED_DIPONIBILITY_MEASURE:
            data = ihh_repository.find_declared_disponibility_by_agent(date)
        elif measure == self.MEASURE_ALL:
            data = ihh_repository.find_all_ihh(start_date, end_date)
            df = pd.DataFrame(data)
            df.fillna(0, inplace=True)
            indicators = []
            for index, row in df.iterrows():
                indicator = {
                    'id': row[0],
                    'date': str(row[1]).split("T")[0],
                    'dis_rea': row[2],
                    'fij_pre': row[3],
                    'gen_rea': row[4],
                    'cap_ins': row[5],
                    'enficc': row[6],
                }
                indicators.append(indicator)
            return add_wrapper(indicators)
        else:
            abort(400)
        df = pd.DataFrame(data)
        if df.empty:
            return {}

        df['market_share'] = df[2] * 100 / df[2].sum()
        df['market_share'].fillna(0, inplace=True)
        df.loc[df['market_share'] < self.MS_THRESHOLDS[0], 'status'] = 0
        df.loc[df['market_share'] > self.MS_THRESHOLDS[0], 'status'] = 1
        df.loc[df['market_share'] > self.MS_THRESHOLDS[1], 'status'] = 2

        indicator = self._serialize_df(df)
        indicator['value'] = float((df['market_share']**2).sum())
        indicator['status'] = indicator['value'] > self.IIH_THRESHOLD
        return indicator

    def find_capacity_by_plant(self, date, ihh_repository: IHHRepository, measure = "capacidad"):

        if (measure == self.CAPACITY_MEASURE):
            data = ihh_repository.find_capacity_by_plant(date)
        elif (measure == self.GENERATION_MEASURE):
            data = ihh_repository.find_generation_by_plant(date)
        elif measure == self.REAL_DIPONIBILITY_MEASURE:
            data = ihh_repository.find_real_disponibility_by_plant(date)
        elif measure == self.DECLARED_DIPONIBILITY_MEASURE:
            data = ihh_repository.find_declared_disponibility_by_plant(date)
        else:
            return {}

        indicator = self.serialice_data(data)
        return indicator
        
    def _serialize_df(self, df):
        indicators = []
        for index, row in df.iterrows():
            indicator = {
                'id': row[0],
                'names': [row[1]],
                'values': [float(row['market_share'])],
                'status': int(row['status'])
            }
            indicators.append(indicator)
        return add_wrapper(indicators)

