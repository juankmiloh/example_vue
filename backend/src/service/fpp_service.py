import datetime

import pandas as pd
import numpy as np

from ..repository import FPPRepository
from ..util.web_util import add_wrapper, to_date


class FPPService:
    def get_fpp(self, start_date, end_date, agrupar_por_planta, fpp_repository: FPPRepository):
        # Obtener datos según parametros

        precio_marginal, fijacion_precios = fpp_repository.find_fpp(
            start_date,
            end_date
        )

        if len(precio_marginal) == 0:
            return []

        return self.serialize_df(fijacion_precios, precio_marginal, agrupar_por_planta)

    def serialize_df(self, data, marginal, agrupar_por_planta):
        indicator = []
        scatter = []

        if not agrupar_por_planta:
            data_df = pd.DataFrame(data)
            data_df = data_df.groupby([5, 1], as_index=False).agg({
                0: 'first', 
                2: 'first', 
                3: 'sum',
                4: 'sum',
                6: 'first',
                7: 'first',
                8: 'first'})
            data_df = data_df[[0,1,2,3,4,5,6,7,8]]
            data_df = data_df.values.tolist()
            data = data_df
            
            marginal_df = pd.DataFrame(marginal)
            marginal_df = marginal_df.groupby([6, 1, 2], as_index=False).agg({
                0: 'first', 
                3: 'first',
                4: 'first',
                5: 'sum',
                7: 'first'})
            marginal_df = marginal_df[[0,1,2,3,4,5,6,7]]
            marginal_df = marginal_df.sort_values(by=[1])
            marginal_df = marginal_df.values.tolist()
            marginal = marginal_df

        for planta in data:
            planta = planta[1:]
            indicator.append(
                {
                    "names": planta[6] if agrupar_por_planta else planta[5],
                    "values": [
                        str(planta[0]),
                        planta[1],
                        planta[2],
                        planta[3],
                        planta[4],
                        planta[5],
                        planta[6],
                    ],
                }
            )
        for scat in marginal:
            scat = scat[1:]
            scatter.append(
                {
                    "names": scat[2] if agrupar_por_planta else scat[5],
                    "values": [
                        str(scat[0]),
                        scat[1],
                        scat[2] if agrupar_por_planta else scat[5],
                        scat[3],
                        scat[4],
                        scat[5],
                        scat[2],
                    ],
                }
            )
        wrapped = add_wrapper(indicator)
        wrapped["scatter"] = scatter

        return wrapped
