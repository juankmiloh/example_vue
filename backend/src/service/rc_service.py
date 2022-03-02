import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import RCRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper


class RCService:
    def get_regasification_cost(self, start_date, end_date, rc_repository: RCRepository):
        indicators = []
        data = rc_repository.find_regasification_cost_by_date_range(
            start_date, end_date)

        print('start_date', start_date,'end_date', end_date)
        df = pd.DataFrame(data)
        return self._serialize_df(df)

    def _serialize_df(self, df):
        indicators = []
        index = pd.date_range(df[4].min(), df[4].max(), freq='MS')
        dfd = pd.DataFrame(index=index)
        nits = df[0].unique()
        for nit in nits:
            dfn = df[df[0] == nit]
            name = dfn[1].iloc[0]  
            dfn[5] = dfn[4].dt.daysinmonth           
            dfn[4] = dfn[4].dt.floor('d')
            dfn.set_index(4, inplace=True)
            dfn = dfn.combine_first(dfd).fillna(0)
            dfn[2] = dfn[2] / dfn[5] 
            dfn.fillna(0, inplace=True)
            indicator = {'id':str(nit),
                         'names':str(name),
                         'dates': [x.strftime('%Y-%m-%d') for x in dfn.index],
                         'values': [float(x) for x in dfn[2]],
                         'values2': [float(x) for x in dfn[3]]}
            indicators.append(indicator)
        return add_wrapper(indicators)
