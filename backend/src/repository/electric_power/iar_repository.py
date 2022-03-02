import calendar
import datetime

from pypika import Query, Table


class IARRepository:
    def __init__(self, db):
        self.db = db

    def find_iar(self, start_date, end_date, to_show, agents, group_by_agent):
        eventos = Table('xm_eventos_transmision', schema='xm_files')
        sql = Query
        sql = sql.from_(eventos)
        sql = sql.select("fecha", "agenteid", "activoid", "activo", "hc",
                         "hid")
        if len(agents) > 0:
            if group_by_agent == "true":
                sql = sql.where(eventos.agenteid.isin(agents))
            else:
                sql = sql.where(eventos.activoid.isin(agents))
        sql = sql.where((eventos.fecha <= end_date)
                        & (eventos.fecha >= start_date))
        data = self.db.engine.execute(sql.get_sql()).fetchall()

        return data
