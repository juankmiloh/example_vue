import calendar
import datetime

from pypika import Order, Query, Table, Order


class FPPRepository:
    def __init__(self, db):
        self.db = db

    def find_fpp(
        self,
        start_date,
        end_date,
    ):
        precio_marginal = Table("precio_marginal", schema="energia")
        sql = Query.from_(precio_marginal).select("*")
        sql = sql.where(
            (precio_marginal.fecha <= end_date) & (precio_marginal.fecha >= start_date)
        )
        sql = sql.orderby('fecha', order=Order.asc)
        precio_marginal = self.db.engine.execute(sql.get_sql()).fetchall()

        fijacion_precios = Table("fijacion_precios", schema="energia")
        sql = Query.from_(fijacion_precios).select("*")
        sql = sql.where(
            (fijacion_precios.fecha <= end_date)
            & (fijacion_precios.fecha >= start_date)
        )
        sql = sql.orderby('fecha', order=Order.asc)
        fijacion_precios = self.db.engine.execute(sql.get_sql()).fetchall()

        return precio_marginal, fijacion_precios
