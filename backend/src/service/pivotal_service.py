import pandas as pd
import numpy as np
from itertools import combinations
import datetime
from flask import abort
from ..repository import TRSDRepository
from ..repository import GRIPRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper
from src.util.private_decorator import isPublic

class PivotalService:

    THRESHOLD = 1

    def get_pivotal(self, date, n_pivots, trsd_repository: TRSDRepository, grip_repository: GRIPRepository):
        
        total_demand = trsd_repository.find_demand_by_day(date)
        df_tde = pd.DataFrame(total_demand)
        df_tde.columns = ['hour', 'dmnd']

        total_disponibility = grip_repository.find_total_disponibility(date)
        df_tdi = pd.DataFrame(total_disponibility)
        df_tdi.columns = ['hour', 't_drea']

        disponibility_by_agent = grip_repository.find_disponibility_by_agent(date)
        df_adi = pd.DataFrame(disponibility_by_agent)
        df_adi.columns = ['hour', 'a_code', 'a_name', 'a_drea']

        if n_pivots > 1:

            codes = df_adi['a_code'].unique()
            tuples = list(combinations(np.arange(len(codes)), n_pivots))
            indices = codes[tuples]

            pivots = range(0, n_pivots)
            dft = pd.DataFrame()
            for i in range(1, 25):
                dfd = df_adi[df_adi['hour'] == i].set_index('a_code')
                drea_list = [ dfd.loc[list(indices[:,j])]['a_drea'].reset_index() for j in pivots]
                dfc = pd.concat(drea_list, axis=1)
                columns = []
                for j in pivots:
                    columns += ['code_{}'.format(j), 'drea_{}'.format(j)]
                dfc.columns = columns
                dfc['a_code'] = dfc['code_{}'.format(0)]
                for j in pivots[1:]:
                    dfc['a_code'] += '+' + dfc['code_{}'.format(j)]
                dfc['a_name'] = dfc['a_code']
                dfc['a_drea'] = 0
                for j in pivots:
                    dfc['a_drea'] += dfc['drea_{}'.format(j)]
                dfc['hour'] = i
                dft = pd.concat([dft, dfc])
            df_adi = dft

        dft = pd.merge(df_adi, pd.merge(df_tde, df_tdi, on='hour'), on='hour')
        dft['pivotal'] = (dft['t_drea'].astype(float) - dft['a_drea'].astype(float)) / dft['dmnd'].astype(float)
        dft = dft.groupby(['a_code', 'a_name'])['hour', 'pivotal'].agg(pd.Series.tolist)
        dft['min'] = dft['pivotal'].apply(min)
        dft.sort_values(by=['min'], ascending=True, inplace=True)

        return self._serialize_df(dft, n_pivots)
    
    def _serialize_df(self, df, n_pivots):
        indicators = []

        public = isPublic()
        general_index = 1
        for index, row in df.iterrows():
            if public:
                code = 'Grupo ' + str(general_index) if n_pivots > 1 else 'Agente ' + str(general_index)
                names = [code, code, float(row['min'])]
                id_ = code
                general_index += 1
            else:
                names = [index[0], index[1], float(row['min'])]
                id_ = index[0]
            indicator = {
                'id': id_,
                'names': names,
                'dates': [int(h) for h in row['hour']],
                'values':[float(p) for p in row['pivotal']]
            }
            indicators.append(indicator)
        return add_wrapper(indicators)