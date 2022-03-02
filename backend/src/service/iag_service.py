import datetime

import pandas as pd
import numpy as np

from ..repository import IAGRepository
from ..util.web_util import add_wrapper, to_date


class IAGService:
    def get_iag(self, start_date, end_date, agents, techs, plants, causes,
                time_medians_to_show, top_times_to_show,
                iag_repository: IAGRepository):

        if start_date > end_date:
            return []

        data = []
        # Obtener datos según parametros
        data = iag_repository.find_iag(start_date, end_date, agents, techs,
                                       plants, causes)

        if len(data) == 0:
            return []
        data = pd.DataFrame(data)
        columns = {
            0: 'agenteid',
            1: 'planta',
            2: 'plantaid',
            3: 'combustible',
            4: 'causa',
            5: 'causaid',
            6: 'causadetallada',
            7: 'estado',
            8: 'capacidadefectiva',
            9: 'unidadid',
            10: 'duracion'
        }
        data.rename(columns, axis=1, inplace=True)

        # Obtener estadisticas
        group_columns = [
            'agenteid',
            'planta',
            'plantaid',
            'combustible',
            'causa',
            'causadetallada',
            'capacidadefectiva',
        ]
        grouppers = {'duracion': ['mean', 'size']}
        data = data.groupby(group_columns).agg(grouppers)
        data = data.reset_index().round(2)
        data.columns = ["_".join(x) for x in data.columns.ravel()]

        data = data.groupby('causa_')

        # Guardar solo los valores más altos
        tops = []
        for name, group in data:
            top_times = group.sort_values(['duracion_mean'],
                                          ascending=1).head(time_medians_to_show)
            top_counts = group.sort_values(['duracion_size'],
                                           ascending=1).head(top_times_to_show)
            top = pd.concat(
                (top_times,
                 top_counts)).drop_duplicates().reset_index(drop=True)
            tops.append((name, top))
        return self.serialize_df(tops)

    def serialize_df(self, data):
        indicator = []
        for name, group in data:
            indicator.append({
                'names':
                name,
                'values':
                group.reset_index().iloc[:,1:].values.tolist()
            })
        return add_wrapper(indicator)
