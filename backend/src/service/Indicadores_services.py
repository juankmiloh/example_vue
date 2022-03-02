from ..repository import PreofeRepository

class IndicadoresServices:
    def getIndicador(self, initial_date, final_date, preofe_repository: PreofeRepository):
        data = preofe_repository.getData(initial_date,final_date)

        result = {'items': [self.serialice_data(dict(row)) for row in data]}
        result ['total'] = len(data)

        return result
    
    def serialice_data(self, row):
        delta = row["MAX_DELTA"]
        oferta = row["MAX_OFERTA"]

        delta_t = row["DELTA_T"]
        delta_pw = row["DELTA_PW"]
        trend_value = 0 if deltaPW == 0 else delta_t / delta_pw

        status = 2 if delta >=  oferta * 0.2 else 1 if delta >=  oferta * 0.1 and  delta <  oferta * 0.2 else 0
        trend = 2 if trend_value > 0 else 1 if trend_value < 0 else 0 
        return {
            'index': row["ID_PLANTA"],
            'names': [row["NOMBRE_AGENTE"], row["PLANTA"]],
            'values': [row["MAX_OFERTA"], row["MAX_DELTA"]],
            'status': status,
            'trend': trend
        }

