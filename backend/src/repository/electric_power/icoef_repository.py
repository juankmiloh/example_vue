import calendar
import datetime

from pypika import Case, Field, Order, Query, Table, Tables
from pypika import functions as fn
from pypika.terms import Function
from sqlalchemy.sql import text


class ICOEFRepository:
    def __init__(self, db):
        self.db = db

    def find_icoef(self, start_date, end_date, period, beta, plants, flip_acc):
        # Obtener todas las tablas necesarias según filtros
        plantas_table = Table('xm_plantas', schema='xm_files')
        sql = Query
        sql = sql.from_(plantas_table)
        sql = sql.select("codigo_planta", "planta")
        if len(plants) > 0:
            sql = sql.where(plantas_table.id_planta.isin(plants))
        plantas = self.db.engine.execute(sql.get_sql()).fetchall()

        grip_table = Table('xm_liquidacion_grip', schema='xm_files')
        sql = Query
        sql = sql.from_(grip_table)
        sql = sql.select("fecha", "planta", "drea", "dpro")
        sql = sql.where((grip_table.fecha <= end_date)
                        & (grip_table.fecha >= start_date))
        sql = sql.orderby(grip_table.fecha, order=Order.desc)
        grip = self.db.engine.execute(sql.get_sql()).fetchall()

        oef_table = Table('xm_obligacion_firme', schema='xm_files')
        sql = Query
        sql = sql.from_(oef_table)
        sql = sql.select("fecha", "submercado", "oefd_kwh-dia", "dcc_kw")
        sql = sql.where((oef_table.fecha <= end_date)
                        & (oef_table.fecha >= start_date))
        sql = sql.orderby(oef_table.fecha, order=Order.desc)
        oef = self.db.engine.execute(sql.get_sql()).fetchall()

        oef_asignada_table = Table('xm_obligacion_firme_asignada',
                                   schema='xm_files')
        sql = Query
        sql = sql.from_(oef_asignada_table)
        sql = sql.select("fecha", "subm", "oef_dia_[kwh-dia]",
                         "oef_mes_[kwh-mes]")
        sql = sql.where((oef_asignada_table.fecha <= end_date)
                        & (oef_asignada_table.fecha >= start_date))
        sql = sql.orderby(oef_asignada_table.fecha, order=Order.desc)
        oef_asignada = self.db.engine.execute(sql.get_sql()).fetchall()
        # La union debe hacerse en pandas por los nombres de las columnas

        return grip, oef, oef_asignada, plantas
