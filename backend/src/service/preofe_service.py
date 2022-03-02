import pandas as pd
from ..repository import PreofeRepository

class PreofeService:

    def get_indicator(self, plant_id, initial_date, final_date, preofe_repository: PreofeRepository):
        if plant_id is None:
            data = preofe_repository.find(initial_date, final_date)
        else: 
            data = preofe_repository.find_by_plant_id(plant_id, initial_date, final_date)

        indicator_data = self.serialize_data(data)
        result = {'items': indicator_data}
        result ['total'] = len(indicator_data)
        return result 


    def serialize_data(self, data):
        indicadores = [] 
        df_data = pd.DataFrame(data)
        plantas = df_data[2].unique() if len(df_data) > 0 else []

        for plata in plantas:
            dfplanta = df_data[df_data[2] == plata]

            oferta_inicial = float(dfplanta[3].iloc[0])
            oferta_final = float(dfplanta[3].iloc[len(dfplanta[3]) -1 ])
            
            trend = oferta_final - oferta_inicial

            idicadorPlanta = {
                'index': int (dfplanta[0].unique()[0]),
                'names': [dfplanta[1].unique()[0], dfplanta[2].unique()[0]],
                'values': [ float(value) for value in dfplanta[3] ],
                'dates': [ str(date) for date in dfplanta[4] ],
                'status': 0 if trend == 0 else 2 if abs(trend)/oferta_inicial * 100 > 20 else 1 if abs(trend)/oferta_inicial * 100 > 10 and  abs(trend)/oferta_inicial * 100 < 20 else 0,
                'trend': 2 if trend > 0 else 1 if trend < 0 else 0   
                            }

            indicadores.append(idicadorPlanta)
            
        return indicadores

