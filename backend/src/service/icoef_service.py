import datetime

import numpy as np
import pandas as pd
from flask import abort

from ..repository import ICOEFRepository
from ..util.web_util import add_wrapper, to_date


class ICOEFService:
    def get_icoef(self, start_date, end_date, period, beta, plants, flip,
                  flip_acc, coverage, no_group, icoef_repository: ICOEFRepository):

        if start_date > end_date:
            return []

        # Asegurarse que todas las fechas inicien y terminen en el día correcto
        if period == "Semanal":
            if start_date.weekday() == 5:
                start_date = start_date + \
                    pd.offsets.Week(weekday=5) - pd.offsets.Week(weekday=5)
            else:
                start_date = start_date + \
                    pd.offsets.Week(weekday=5) - \
                    pd.offsets.Week(weekday=5) + pd.offsets.Day()
            end_date = end_date - pd.offsets.Day() + pd.offsets.Week(weekday=5)
        elif period == "Mensual":
            end_date = end_date + pd.offsets.MonthEnd()
        elif period == "Anual":
            end_date = end_date + pd.offsets.YearEnd()
        else:
            pass
        
        # Siempre se deben incluir ambas proelectricas
        if '80' in plants or '210' in plants:
            plants.append('80')
            plants.append('210')
            plants = list(set(plants))
    
        # Obtener información según filtros
        grip, oef, oef_asignada, plantas = icoef_repository.find_icoef(
            start_date, end_date, period, beta, plants, flip_acc)

        if len(grip) == 0 or len(oef) == 0 or len(oef_asignada) == 0 or len(
                plantas) == 0:
            return []

        grip = pd.DataFrame(grip)
        oef = pd.DataFrame(oef)
        oef_asignada = pd.DataFrame(oef_asignada)
        plantas = pd.DataFrame(plantas)

        # Cambio de nombre de las columnas de los archivos OEF y OEF asignada
        oef.rename({3: 'dcc_kw'}, axis=1, inplace=True)
        oef_asignada.rename({3: 'OEF'}, axis=1, inplace=True)
        grip.rename({2: 'drea'}, axis=1, inplace=True)
        plantas.rename({0: 'codigo', 1: 'planta'}, axis=1, inplace=True)

        # m corresponde al número de dias del mes de estudio
        m = pd.Period(str(start_date)).days_in_month  #if flip_acc == "true" else 1
        # Como el análises va sobre la OEF asignada, se divide por el mes de estudio porque se utiliza la OEF mensual.
        #La OEF diaria del archivo corresponde con la OEF ajustada.
        oef_asignada['OEF'] = oef_asignada['OEF'].divide(m)

        # Manejo de datos del archivo GRIP
        grip = grip.groupby([0, 1])['drea'].sum()

        # Organización de datos entre las tres bases de datos que se necesitan.
        icoef = oef.merge(oef_asignada, left_on=[0, 1], right_on=[0, 1])
        icoef = icoef.merge(grip, left_on=[0, 1], right_on=[0, 1])
        icoef = icoef.merge(plantas, left_on=[1], right_on=['codigo'])

        #Cáluclo del indicador ICOEF: compara la disponibilidad real con la OEF asignada
        if flip_acc == "true":
            col_anillado = 'dcc_kw'
        else:
            col_anillado = 'drea'

        icoef2 = icoef.copy()
        icoef3 = icoef2.copy()
        icoef2["icoef"] = icoef2['drea'] < icoef2['OEF'] * (1 - beta / 100.0)
        icoef2["icoefas"] = icoef2['dcc_kw'] < icoef2['OEF'] * (1 -
                                                                beta / 100.0)
        
        icoef = icoef[icoef[col_anillado] < icoef['OEF'] * (1 - beta / 100.0)]

        
        icoef[0] = icoef[0].apply(lambda x: 'PRG1' if x == 'PRG2' else x)
        icoef['planta'] = icoef['planta'].apply(
            lambda x: 'PROELECTRICA 1' if x == 'PROELECTRICA 2' else x)

        icoef2[0] = icoef2[0].apply(lambda x: 'PRG1' if x == 'PRG2' else x)
        icoef2['planta'] = icoef2['planta'].apply(
            lambda x: 'PROELECTRICA 1' if x == 'PROELECTRICA 2' else x)
        
        if period == "Semanal":
            frequency = 'W-SAT'  # semanal
        elif period == "Mensual":
            frequency = 'M'  # mensual 'MS'
        elif period == "Anual":
            frequency = 'A'  # mensual 'MS'
        else:
            frequency = 'D'

        if no_group == "true":
            frequency = 'A'

        icoef3 = icoef3[icoef3['dcc_kw'] < icoef3['OEF'] * (1 - beta / 100.0)] #fix
        icoef3['cobertura'] = icoef3['dcc_kw'].div(icoef3['OEF']) * 100
        icoef3 = icoef3.groupby([1]).agg({'cobertura': 'mean'}).reset_index()
        icoef3['cobertura'] = icoef3['cobertura'].round(2)

        icoef2 = icoef2.groupby(
            [1, 'planta', pd.Grouper(key=0,
                                    freq=frequency)]).sum().reset_index()

        icoef = icoef.groupby([1, 'planta',
                            pd.Grouper(key=0, freq=frequency)
                            ]).size().reset_index(name='comparacion')           

        if coverage != "true":
            icoef2 = icoef2[(icoef2.icoef > 0.0) | (icoef2.icoefas > 0.0)]
        icoef2.sort_values('icoef', inplace=True, ascending=False)
        icoef.sort_values('comparacion', inplace=True, ascending=False)

        icoef.rename({'planta': 4}, axis=1, inplace=True)

        if coverage != "true":
            icoef = icoef[icoef.comparacion != 0]

        if icoef3.empty or icoef2.empty:
            return []

        icoef3 = icoef2.merge(icoef3, on=1, how='left').fillna(100)
        icoef3 = icoef3[['planta', 0, 'icoef', 'icoefas', 'cobertura']].copy()
        icoef3.sort_values([0, 'icoef'], inplace=True, ascending=[True, False])
        if flip_acc == "true":
            icoef3['comparacion'] = icoef3['icoefas']
        else:
            icoef3['comparacion'] = icoef3['icoef']
        icoef3.rename({'planta': 4}, axis=1, inplace=True)

        return self._serialize_df(icoef3, flip)

    def _serialize_df(self, df, flip):
        indicators = []
        if flip == "true":
            dates = df[0].unique()
            for date in dates:
                dfn = df[df[0] == date]
                indicator = {
                    'names': str(date).split("T")[0],
                    'dates': dfn[4].values.tolist(),
                    'values': dfn['comparacion'].values.tolist(),
                    'icoef': dfn['icoef'].values.tolist(),
                    'icoefas': dfn['icoefas'].values.tolist(),
                    'cobertura': dfn['cobertura'].values.tolist()
                }
                indicators.append(indicator)
        else:
            plants = df[4].unique()
            for plant in plants:
                dfn = df[df[4] == plant]
                indicator = {
                    'names': str(plant),
                    'dates': [str(x).split("T")[0] for x in dfn[0].values],
                    'values': dfn['comparacion'].values.tolist(),
                    'icoef': dfn['icoef'].values.tolist(),
                    'icoefas': dfn['icoefas'].values.tolist(),
                    'cobertura': dfn['cobertura'].values.tolist()
                }
                indicators.append(indicator)
        return add_wrapper(indicators)
