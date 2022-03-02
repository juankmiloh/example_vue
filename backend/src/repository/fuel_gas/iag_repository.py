import calendar
import datetime

from pypika import Order, Query, Table


class IAGRepository:
    def __init__(self, db):
        self.db = db
    def find_iag(self, start_date, end_date, agents, techs, plants, causes):

        # Unir los eventos con las horas de indisponibilidad
        eventos = Table('xm_eventos_generacion', schema='xm_files')
        indisponibilidades = Table('xm_indisponibilidades', schema='energia')
        agentes = Table('xm_agentes_eventos', schema='xm_files')

        sql = Query \
            .from_(eventos) \
            .join(indisponibilidades) \
            .on(eventos.id_xm_eventos_generacion ==
                 indisponibilidades.id_xm_indisponibilidades) \
            .join(agentes) \
            .on(eventos.agenteid == agentes.id) \
            .select(agentes.nombre, 'plantaid', 'plantaid', 'combustible',
                     'causa', 'causaid', 'causadetallada', 'estado',
                     'capacidadefectiva', 'unidadid',
                     indisponibilidades.duracion)
        # Filtros
        if len(agents) > 0:
            sql = sql.where(eventos.agenteid.isin(agents))
        if len(techs) > 0:
            sql = sql.where(eventos.combustible.isin(techs))
        if len(plants) > 0:
            sql = sql.where(eventos.plantaid.isin(plants))
        if len(causes) > 0:
            sql = sql.where(eventos.causaid.isin(causes))

        sql = sql.where(eventos.causa != "Mantenimiento programado")
        
        # Periodo
        sql = sql.where((eventos.fecha <= end_date)
                        & (eventos.fecha >= start_date))
        sql = sql.orderby(eventos.fecha, order=Order.asc)

        data = self.db.engine.execute(sql.get_sql()).fetchall()
        return data
