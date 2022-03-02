import pandas as pd
from ..repository import PivotalIndexRepository

class PivotalIndexService:

    def get_indicator(self, agent_code, initial_date, final_date, pivotal_index_repository: PivotalIndexRepository):

        data = pivotal_index_repository.find_by_date_range_and_agent(agent_code, initial_date, final_date)
        df = pd.DataFrame(data)
        if df.empty:
            return {}
        df.fillna(0, inplace=True)
        indicator_data = self.serialize_data(df, data)
        result = {'items': indicator_data}
        result['total'] = len(indicator_data)

        return result 

    def serialize_data(self, df, data):
        values = []
        for i in range(len(df)):
            for h in range(3, 27):
                values.append([h - 2, i, df[h][i]])
        indicador = {
            'index': str(df[1][0]),
            'names': [x.strftime('%Y-%m-%d') for x in df[27].tolist()],
            'values': values,
            'dates': [x.strftime('%Y-%m-%d') for x in df[27].tolist()], 
            'table': df.loc[:, 2:26].values.tolist()
            }
        return [indicador]

