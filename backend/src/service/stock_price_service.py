import pandas as pd, numpy as np, datetime
from flask import abort
from ..repository import PME140Repository
from ..repository import TRSDRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class StockPriceService:

    def get_references(self, year, pme140_repository: PME140Repository):
        data = pme140_repository.find_by_year(year)
        df = pd.DataFrame(data)
        if df.empty:
            return {}
        else:
            df = pd.DataFrame(data)
            df[0] = pd.to_datetime(df[0], format='%Y/%m')
            print(df)
            df.drop_duplicates(subset=0, keep='last', inplace=True)
            df.loc[:,'date'] = df[0]
            df = df.set_index('date')
            print(df)
            start_date = df.index.min() - pd.DateOffset(day=1)
            end_date = df.index.max() + pd.DateOffset(day=31)
            dates = pd.date_range(start_date, end_date, freq='D')
            dates.name = 'date'
            df = df.reindex(dates, method='ffill')
            return self._serialize_df_references(df)

    def _serialize_df_references(self, df):
        indicators = []
        indicators.append({'id':'pe',  
                'names':df.index.values.tolist(), 
                'dates':df.index.values.tolist(),
                'values':[float(x) for x in df[1].values.tolist()]})
        indicators.append({'id':'pea',  
                'names':df.index.values.tolist(), 
                'dates':df.index.values.tolist(),
                'values':[float(x) for x in df[2].values.tolist()]})
        indicators.append({'id':'pme',  
                'names':df.index.values.tolist(), 
                'dates':df.index.values.tolist(),
                'values':[float(x) for x in df[3].values.tolist()]})

        return add_wrapper(indicators)

    def get_prices(self, years, trsd_repository: TRSDRepository):
        data = trsd_repository.find_stock_prices_by_year(years=years)
        df = pd.DataFrame(data)
        if df.empty:
            return {}
        return self._serialize_df(df)

    def _serialize_df(self, df):
        df = df.groupby(0).agg(lambda x: x.tolist())
        df = df.sort_index(ascending=0)
        indicators = []

        first = True
        for index, row in df.iterrows():
            indicator = {'id':'Promedio ' +str(int(index)), 
                        'names': row[1], 
                        'dates': row[1], 
                        'values':[float(x) for x in row[2]]}
            indicators.append(indicator)
            if first:
                indicator = {'id':'Máximo ' + str(int(index)), 
                            'names': row[1], 
                            'dates': row[1],
                            'values':[float(x) for x in row[3]]}
                indicators.append(indicator)
                first = False
        return add_wrapper(indicators)
