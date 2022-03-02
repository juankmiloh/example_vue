import pandas as pd
import datetime
from flask import abort
from ..repository import GRIPRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper
from ..util.web_util import get_last_month
from ..util.private_decorator import isPublic

class IndicatorDateService:

    TABLES_INDICATORS = {
        "daggi": ["gmg_inventarios_planta"],
        "dp": ["gmg_contratos"],
        "fpp": ["xm_desempate"],
        "gmg": ["gmg_contratos"],
        "gmg_inventory": ["gmg_inventarios_planta"],
        "gmg_og": ["gmg_oferta"],
        "gpgr": ["xm_liquidacion_grip_acc"],
        "iag": ["xm_eventos_generacion"],
        "iar": ["xm_eventos_transmision"],
        "icoef": ["xm_obligacion_firme"],
        "ihh": ["hhi"],
        "ihh_capacity": ["xm_capacidad_instalada"],
        "ihh_generation": ["xm_liquidacion_grip_acc"],
        "pivotal": ["xm_liquidacion_grip", "xm_transacciones_mem"],
        "pivotal3d":["xm_indices_pivotales"],
        "preofe": ["xm_precios_oferta_diaria"],
        "rc": ["gmg_costos_regasificacion"],
        "trsd": ["xm_transacciones_mem", "xm_precios_oferta"]
    }

    def dates_by_rules(self, indicador, dates, indicator_dates_repository):

        if indicador == "preofe":
            if isPublic():
                last_month = get_last_month(5)
                if last_month < dates[0][0]:
                    return [[last_month, dates[0][1]]]

        if indicador == "pivotal":
            last_date = indicator_dates_repository.get_valid_range_for_pivotal()
            return [[last_date[0][0], dates[0][1]]]
        
        if indicador == "dp":
            last_date = indicator_dates_repository.get_dp_last_date()
            return [[last_date[0][0], dates[0][1]]]
        
        if indicador == "ihh":
            last_date = indicator_dates_repository.get_valid_range_for_ihh()
            return [[last_date[0][0], last_date[0][1]]]

        if indicador == "iar":
            last_date = indicator_dates_repository.get_valid_range_for_iar()
            return [[last_date[0][0], last_date[0][1]]]

        if indicador == "iag":
            last_date = indicator_dates_repository.get_valid_range_for_iag()
            return [[last_date[0][0], last_date[0][1]]]

        return dates

    def get_dates_by_indicator(self, indicador, indicator_dates_repository):
        if not indicador in self.TABLES_INDICATORS.keys():
            return None

        dates = indicator_dates_repository.get_valid_range_by_tables(self.TABLES_INDICATORS[indicador])

        return self.dates_by_rules(indicador, dates, indicator_dates_repository)
        
