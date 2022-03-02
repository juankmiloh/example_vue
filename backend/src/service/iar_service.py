import datetime

import pandas as pd
import numpy as np

from ..repository import IARRepository
from ..util.web_util import add_wrapper, to_date


class IARService:
    def get_iar(self, start_date, end_date, to_show, agents, group_by_agent,
                iar_repository: IARRepository):

        if start_date > end_date:
            return []
        # Obtener datos
        data = iar_repository.find_iar(start_date, end_date, to_show, agents,
                                       group_by_agent)
        if len(data) == 0:
            return []

        data = pd.DataFrame(data)
        data.rename(
            {
                0: 'fecha',
                1: 'agenteid',
                2: 'activoid',
                3: 'activo',
                4: 'hc',
                5: 'hid',
            },
            axis=1,
            inplace=True)
        bins = np.arange(np.floor(data.hid.min()),np.ceil(data.hid.max()))
        hist, bin_edges = np.histogram(data.hid[data.hid > 0], density=True, bins=bins)
        
        series = bin_edges
        acumulado = np.cumsum(hist)
        if group_by_agent == "true":
            data = data.groupby(['agenteid']).sum().reset_index()
            data.rename({'agenteid': 'value'}, axis=1, inplace=True)
        else:
            data = data.groupby(['activoid', 'activo']).sum().reset_index()
            data.rename({'activo': 'value'}, axis=1, inplace=True)

        data = data[(data.hc > 0.0) | (data.hid > 0.0)]
        data = data.sort_values(['hc', 'hid'], ascending=False).head(to_show)
        data = data.round(decimals=2)
        series = series.round()
        return self.serialize_df(data, hist, acumulado, series)

    def serialize_df(self, data, hist, acumulado, series):
        indicators = []
        dfn = data
        indicator = {
            'value': dfn.value.values.tolist(),
            'hc': dfn.hc.values.tolist(),
            'hid': dfn.hid.values.tolist(),
            'densidad': dfn.hid.values.tolist(),
            'probabilidad': dfn.hid.values.tolist(),
            'hist': hist.tolist(),
            'acumulado': list(acumulado),
            'series': list(series)
        }
        indicators.append(indicator)

        return add_wrapper(indicators)
