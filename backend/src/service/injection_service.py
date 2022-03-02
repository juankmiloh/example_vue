import pandas as pd
import numpy as np
import datetime
from flask import abort
from ..repository import InventoryRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class InjectionService:

    def get_by_date_range(self, start_date, end_date, inventory_repository: InventoryRepository):

        data = inventory_repository.find_inyected_by_date_range(start_date, end_date)
        df = pd.DataFrame(data)
        df.set_index(0, inplace=True)
        index = pd.date_range(df.index[0], df.index.max())
        df2 = pd.DataFrame(index=index)
        df = df.combine_first(df2).fillna(0)

        if df.empty:
            return {}

        indicator = self._serialize_df(df)
        return indicator
    
    def _serialize_df(self, df):
        
        indicator = {'id':'injection',  
                'names': [x.strftime('%Y-%m-%d') for x in df.index], 
                'dates': [x.strftime('%Y-%m-%d') for x in df.index],  
                'values':  [float(x) for x in df[1]]}
        return add_wrapper([indicator])
