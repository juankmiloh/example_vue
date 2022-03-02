import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import ContratRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class ContratService:

    DEVIATION_THRESHOLD = 5
    DAYS = 5
    DAYS_THRESHOLD = 3
    BY_PLANT = "planta"

    def get_market_power(self, date, contrat_repository: ContratRepository):
        
        data = contrat_repository.find_accumulated_by_agent(date)
        df = pd.DataFrame(data)
        if df.empty:
            return {}

        total = df[1].sum()
        df['percentage'] = df[1] / total * 100
        indicator = self._serialize_df(df)
        indicator['value'] = int(total)
        return indicator
    
    def _serialize_df(self, df):
        indicators = []
        for index, row in df.iterrows():
            indicator = {
                'id': row[0],
                'names': [row[0]],
		        'dates': [row[2].strftime('%Y-%m-%d'), row[3].strftime('%Y-%m-%d')],
                'values': [float(row['percentage']), int(row[1])]
            }
            indicators.append(indicator)
        return add_wrapper(indicators)

    def get_price_discrimination(self, date, contrat_repository: ContratRepository, 
            group_by=[], source=[], market=[], starting_year=[], agent_type=None, role=None, sector=[], modality=[]):
        
        data = contrat_repository.find_accumulated_by_custom_filter(date,
            group_by=group_by, source=source, market=market, starting_year=starting_year, 
            agent_type=agent_type, sector=sector)

        df = pd.DataFrame(data)
        print(df[[4]])
        if df.empty:
            return {}

        indicator = self._format_and_serialize_df(df)
        return indicator

    def _format_and_serialize_df(self, df):
        indicators = []
        for index, row in df.iterrows():
            indicator = {
                'id': int(index),
                'names': [row[0], row[1], row[4], row[7], row[8], row[10]],
		        'dates': [row[5].strftime('%Y-%m-%d'), row[6].strftime('%Y-%m-%d')],
                'values': [float(row[2]), int(row[3]) / 1000, float(row[9]) / 1000]
            }
            indicators.append(indicator)
        return add_wrapper(indicators)

    def get_offert_curve(self, date, contrat_repository: ContratRepository,
            modalidad="Firme", source=[], market=[], starting_year=[], role=None ,agent_type=None, public=False ):        

        data = contrat_repository.find_accumulated_by_price_and_agent(date,  modalidad, 
            source, market, starting_year, role, agent_type)
        
        df = pd.DataFrame(data)
        df[3] = df[3].dt.days

        if df.empty:
            return {}

        indicator = self._serialize_df_oc(df, public)
        return indicator


    def _serialize_df_oc(self, df, public):
        result = {}
        indicators = []
        
        df.columns = ["empresa", "precio", "cantidad", "nDias"]
        df["C*D"] = df["cantidad"] * df["nDias"] 
        df["P*C*D"] = df["precio"] * df["C*D"] 

        data_agrupada = df.groupby(["precio", "empresa"])["cantidad", "C*D", "P*C*D"].sum()
        data = data_agrupada.reset_index().values.tolist()

        index = 1 
        for row in data:
            name = row[1]
            CxD = row[3]
            PxCxD = row[4]
            precio = row[0]
            cantidad = row[2]

            indicator = {
                'id': int(index),
                'names': ["Contrato " + str(index) if public else name],
                'values': [
                    precio,
                    cantidad,
                    CxD,
                    PxCxD
                ]
            }

            indicators.append(indicator)
            index += 1

        return add_wrapper(indicators)
    
    def _price_import_national(self, date, source, contrat_repository: ContratRepository):
        indicators = []

        data = contrat_repository.find_accumulated_by_price_and_agent_and_date(date, source)
        price_import = contrat_repository.get_price_import(date)[0][0]

        df = pd.DataFrame(data)
        if df.empty:
            return {}

        df.columns = ["grupo","fuente", "precio", "cantidad"]
        df["P*C"] = df["precio"] * df["cantidad"] 
        data_agrupada = df.groupby(["grupo"])["precio", "cantidad", "P*C"].sum()
        data = data_agrupada.reset_index()
        data["wAvg"] =  data["P*C"] / data["cantidad"]
        data = data.values.tolist()
        index = 1 
        for row in data:
            grupo = row[0]
            precio = float(row [1])
            cantidad = int (row [2])
            precioPonderado = float(row[4])
            precioImportado = float(price_import)
            indice = float(row[4]) / precioImportado

            indicator = {
                'id': int(index),
                'names': [grupo],
                'values': [
                    precioPonderado,
                    indice
                ]
            }

            indicators.append(indicator)
            index += 1

        return add_wrapper(indicators)