from sqlalchemy.sql import text

class TRSDRepository:
    def __init__(self, db):
        self.db = db

    def find_by_plant(self, date):
        sql = '''SELECT
                    PO.submercado,
                    P.planta, 
                    A.nombre_agente, 
                    COUNT(*) frecuencia
                from
                    xm_files.xm_precios_oferta PO
                    LEFT JOIN xm_files.xm_transacciones_mem T
                    ON (T."hora" = PO."hora" and T.fecha = PO.fecha and PO.precio_oferta = T.mpon),
                    xm_files.xm_agentes A,
                    xm_files.xm_plantas P
                WHERE 
                    EXTRACT(MONTH from PO.fecha) = :month 
                    AND EXTRACT(YEAR FROM T.fecha) = :year 
                    AND EXTRACT(YEAR FROM PO.fecha) = :year 
                    AND EXTRACT(DAY FROM PO.fecha) IN ( SELECT * FROM GENERATE_SERIES(1, 31) )
                AND PO.precio_oferta > 0
                AND PO.submercado = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                GROUP BY 
                    PO.submercado,
                    P.planta,
                    A.nombre_agente
                ORDER BY 
                    FRECUENCIA"
                    DESC'''

        return self.db.engine.execute(text(sql),
                                      month=date.month, 
                                      year=date.year).fetchall()

    def find_by_agent(self, date):
        sql = '''SELECT
                    A.codigo_agente,
                    A.nombre_agente, 
                    COUNT(*) frecuencia
                from
                    xm_files.xm_precios_oferta PO
                    LEFT JOIN xm_files.xm_transacciones_mem T
                    ON (T."hora" = PO."hora" and T.fecha = PO.fecha and PO.precio_oferta = T.mpon),
                    xm_files.xm_agentes A,
                    xm_files.xm_plantas P
                WHERE 
                    EXTRACT(MONTH from PO.fecha) = :month 
                    AND EXTRACT(YEAR FROM T.fecha) = :year 
                    AND EXTRACT(YEAR FROM PO.fecha) = :year 
                    AND EXTRACT(DAY FROM PO.fecha) IN ( SELECT * FROM GENERATE_SERIES(1, 31) )
                AND PO.precio_oferta > 0
                AND PO.submercado = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                GROUP BY 
                    A.codigo_agente,
                    A.nombre_agente
                ORDER BY 
                    frecuencia
                    DESC'''

        return self.db.engine.execute(text(sql),
                                      month=date.month, 
                                      year=date.year).fetchall()

    def find_stock_prices_by_year(self, years):

        sql = '''SELECT
                    EXTRACT(YEAR FROM T.fecha) AS year,
                    to_char(T.fecha,'mm/dd') AS month_day,
                    AVG(T.pbna) avg_pbna, 
                    MAX(T.pbna) max_pbna
                from
                    xm_files.xm_transacciones_mem T
                WHERE 
                    EXTRACT(YEAR FROM T.fecha) IN :years
                GROUP BY 
                    year,
                    month_day
                ORDER BY
                    year DESC,
                    month_day ASC'''

        return self.db.engine.execute(text(sql),
                                      years=tuple(years)).fetchall()  


    def find_demand_by_day(self, date):

        sql = '''SELECT 
                    D.hora,
                    D.dmnd
                FROM
                    xm_files.xm_transacciones_mem D
                WHERE
                    D.fecha = :date
                ORDER BY 
                    D.hora
                '''

        return self.db.engine.execute(text(sql), date=date).fetchall()