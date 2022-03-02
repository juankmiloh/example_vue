import datetime
import itertools

import numpy as np
import pandas as pd
from flask import abort

from ..repository import DPRepository
from ..util.web_util import add_wrapper, to_date


class DPService:
    def get_dp(self,
               date,
               end_date,
               markets_numerator,
               markets_denominator,
               modalities_numerator,
               modalities_denominator,
               sectors_numerator,
               sectors_denominator,
               sources_numerador,
               sources_denominator,
               dp_repository: DPRepository):
        
        dates = [date]
        indexes = []
        if end_date:
            end_date = end_date + pd.offsets.MonthEnd()
            dates = pd.date_range(date, end_date, freq="MS").tolist()

        for date in dates:
            if "Secundario" in markets_numerator:
                data_numerator = dp_repository.find_accumulated_dp_for_secundaries(
                    date,
                    end_date,
                    markets_numerator,
                    modalities_numerator,
                    sectors_numerator,
                    sources_numerador)
            else:
                data_numerator = dp_repository.find_accumulated_dp(
                    date,
                    end_date,
                    markets_numerator,
                    modalities_numerator,
                    sectors_numerator,
                    sources_numerador)

            if "Secundario" in markets_denominator:
                data_denominator = dp_repository.find_accumulated_dp_for_secundaries(
                    date,
                    end_date,
                    markets_denominator,
                    modalities_denominator,
                    sectors_denominator,
                    sources_denominator)
            else:
                data_denominator = dp_repository.find_accumulated_dp(
                    date,
                    end_date,
                    markets_denominator,
                    modalities_denominator,
                    sectors_denominator,
                    sources_denominator)
            
            index = None
            weigthed_avg_numerator = 0
            weigthed_avg_denominator = 0
            if data_numerator and data_denominator:
                
                df_numerador = pd.DataFrame(data_numerator)
                
                df_numerador['weigthed_avg'] = (df_numerador[2])
                weigthed_avg_numerator = df_numerador['weigthed_avg'].sum() / df_numerador['weigthed_avg'].count() 
                
                df_denominador = pd.DataFrame(data_denominator) 
                
                df_denominador['weigthed_avg'] = (df_denominador[2])
                weigthed_avg_denominator = df_denominador['weigthed_avg'].sum()  / df_denominador['weigthed_avg'].count() 
                
                if weigthed_avg_denominator > 0:
                    index = weigthed_avg_numerator / weigthed_avg_denominator
                if not index or not weigthed_avg_denominator or not weigthed_avg_numerator:
                    pass
                else:
                    indexes.append([date, round(index, 3), round(weigthed_avg_numerator, 3), round(weigthed_avg_denominator, 3)]) 
                
        if len(indexes) == 0:
            return add_wrapper([])
        else:
            return self.serialize_df(indexes)

    def serialize_df(self, indexes):
        indicator = []
        for index in indexes:
            indicator.append({
                'date': index[0].strftime("%Y-%m"),
                'index': index[1],
                'weigthed_avg_numerator': index[2],
                'weigthed_avg_denominator': index[3]
            })
        return add_wrapper(indicator)

    def get_combinations(self, items):
        # Make all possible combinations
        combinations = []
        for lenght in range(0, len(items) + 1):
            for subset in itertools.combinations(items, lenght):
                combinations.append(subset)
        return combinations
