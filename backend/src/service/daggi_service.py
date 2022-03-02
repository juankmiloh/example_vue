import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import DaggiRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class DaggiService:

    def get_fuction_days(self, start_date, end_date, percentage_capacity,
    utilizar_oef, utilizar_gn, daggi_repository: DaggiRepository):

        #Información refrente a los inventarios
        data_inventory = daggi_repository.find_inventory_by_date(start_date, end_date)

        #Información referente a la capacidad total
        data_capacity = daggi_repository.find_total_inventory(utilizar_oef)

        #Transformamos a dataframes
        df_inventory = pd.DataFrame(data_inventory, columns=['fecha','planta','cantidad'])
        df_capacity = pd.DataFrame(data_capacity, columns=['fecha','planta','capacidad'])

        df_percentage = pd.DataFrame(sorted(df_inventory['planta'].unique()), columns=['planta'])

        if percentage_capacity is None:
            df_percentage['porcentaje'] = 1
        else:
            df_percentage['porcentaje'] = percentage_capacity

        # Al no presentar consumo el porcentaje de producción es 0
        df_percentage = df_percentage.fillna(0)
        
        #Realizamos una fusión
        df_result = pd.merge(df_inventory, df_capacity, on=['planta'], how='inner')
        df_result = pd.merge(df_result, df_percentage, on=['planta'], how='left')

        #Realizamos el calculo aritmetico
        if ((df_result['capacidad'].astype('float64')*df_result['porcentaje'])!=0).any():
            df_result['dias'] = df_result['cantidad']/ (df_result['capacidad'].astype('float64')*df_result['porcentaje'])
        else:
            df_result['dias'] = 100

        df_result = df_result.replace(np.inf, 100)

        #En caso de estar vacio
        if df_result.empty:
            return {}

        indicator = self._serialize_df(df_result)

        return indicator

    def _serialize_df(self, df):
        
        indicator = {'id':'daggi',  
                'names': [str(x) for x in df['planta']], 
                'dates': [x.strftime('%Y-%m-%d') for x in df['fecha_x']],  
                'values':  [float(x) for x in df['dias']]}
        return add_wrapper([indicator])

    def get_percentage_capacity(self, date, days, utilizar_oef, utilizar_gn, daggi_repository: DaggiRepository):

        #Información refrente a los inventarios
        data_percentage = daggi_repository.find_consuption_percentage(date, days, utilizar_oef)

        #Transformamos a dataframes
        df_percentage = pd.DataFrame(data_percentage, 
                                    columns=['nombre_agente', 'porcentaje', 'porcentaje_compl', 'promedio_gasn'])

        #Organizamos por la columnas de nombre de agente
        df_percentage.sort_values(by=['nombre_agente'], inplace=True)
        df_percentage.fillna(0, inplace=True)

        #En caso de retornar vacio
        if df_percentage.empty:
            return {}

        #Serializamos para rest
        indicator = self._serialize_df_percentage(df_percentage, utilizar_gn)

        return indicator

    def _serialize_df_percentage(self, df, utilizar_gn):
        
        indicator = {'id':'daggi_percentage',  
                'names': [str(x) for x in df['nombre_agente']], 
                'values':  [round(float(x), 2) for x in df['porcentaje_compl' if utilizar_gn else 'porcentaje']]}
        return add_wrapper([indicator])