import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import InventoryRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class InventoryService:

    def get_by_date_range(self, start_date, end_date, public, inventory_repository: InventoryRepository):
        companies = []
        last_values = {}

        data = inventory_repository.find_by_date_range(start_date, end_date)
        df = pd.DataFrame(data)

        if df.empty:
            return {}
        
        last_date = df[1].max()
        last_date_values = df[df[1] == last_date]
        
        for index, row in last_date_values.iterrows():
            last_values[row[0]] = row[2]
            companies.append(row[0])
        companies.remove("Total")

        data_consumo = inventory_repository.find_by_date_range_in_consumo(last_date, end_date)
        total = 0
        if data_consumo:
            aux_date = data_consumo[0][1]
        aux_company = []
        for consumo in data_consumo:
            if aux_date != consumo[1]:
                last_values["Total"] -= float(total)
                df = df.append({0 :  "Total",  1: aux_date, 2:last_values["Total"]} , ignore_index=True)
                total = 0
                aux_date = consumo[1]
                compnies_without_data = list(set(companies) - set(aux_company))
                for company in compnies_without_data:
                    df = df.append({0 :  company,  1: aux_date, 2: last_values[company]} , ignore_index=True)
                aux_company=[]

            total += consumo[2]
            last_values[consumo[0]] -= float(consumo[2])
            aux_company.append(consumo[0])
            df = df.append({0:consumo[0], 1:consumo[1], 2:last_values[consumo[0]]}, ignore_index=True)

        if not public:
            ov_df = pd.DataFrame(inventory_repository.get_operational_values()) 
            ov_df = ov_df.append({0:'Total', 1:ov_df[1].sum(), 2:ov_df[2].sum()}, ignore_index=True)

        indicator = self._serialize_df(df, public, ov_df)
        return indicator
    
    def _serialize_df(self, df, public, ov_df):

        ov = {}
        for index, row in ov_df.iterrows():
            ov[row[0]] = {'max':int(row[1]), 'min':int(row[2])}

        df = df.groupby(0).agg(lambda x: x.tolist())
        indicators = []
        for index, row in df.iterrows():
            if (not public or str(index) == "Total"):
                indicator = {
                    'id':str(index), 
                    'names': [x.strftime('%Y-%m-%d') for x in row[1]], 
                    'dates': [x.strftime('%Y-%m-%d') for x in row[1]],  
                    'values': [float(x) for x in row[2]],
                    'operational_values': ov[str(index)]
                }
                indicators.append(indicator)
        
        return add_wrapper(indicators)
