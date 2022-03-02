from sqlalchemy.sql import text

class InventoryRepository:
    def __init__(self, db):
        self.db = db


    def find_total_by_date_range(self, start_date, end_date):
        sql = '''
                SELECT 
                    I.fecha,  
                    sum(I.cantidad)
                FROM xm_files.gmg_inventarios_planta I
                WHERE
                    I.fecha BETWEEN :start_date ::DATE AND :end_date ::DATE AND
                    I.planta = 'Total' 
                group BY
                    I.fecha
                ORDER BY
                    I.fecha ASC
            '''
        return self.db.engine.execute(text(sql),start_date = start_date, end_date = end_date).fetchall()

    def find_by_date_range(self, start_date, end_date):
        sql = '''
                SELECT 
                    I.planta,
                    I.fecha,  
                    I.cantidad
                FROM xm_files.gmg_inventarios_planta I
                WHERE
                    I.fecha between :start_date ::DATE and :end_date ::DATE
                ORDER BY
                    I.fecha ASC,
                    I.planta ASC
            '''
        return self.db.engine.execute(text(sql),start_date = start_date, end_date = end_date).fetchall()
    
    def find_by_date_range_in_consumo(self, start_date, end_date):
        sql = '''
                SELECT 
                    INITCAP(trim(both ' E.S.P.' from a.nombre_agente) || '.') planta,
                    c.dia,
                    sum(c.gani)
                FROM 
                    xm_files.xm_consumo c,
                    xm_files.xm_plantas p,
                    xm_files.xm_agentes a
                where
                    c.recurso = p.codigo_planta
                and p.codigo_agente = a.codigo_agente
                and (
                        p.codigo_agente = 'TCIG' or p.codigo_agente = 'TMFG' or p.codigo_agente = 'TBSG'
                    )
                and c.dia > :start_date
                and c.dia <= :end_date
                group by c.dia,a.nombre_agente
            '''
        return self.db.engine.execute(text(sql),start_date = start_date, end_date = end_date).fetchall()

    def find_inyected_by_date_range(self, start_date, end_date):
        sql = '''
                SELECT 
                    OF.fecha, 
                    SUM(OF.oferta) / 1000
                FROM xm_files.gmg_oferta OF
                WHERE 
                    OF.fecha BETWEEN :start_date ::DATE AND :end_date ::DATE AND
                    OF.operador = 'CALAMARI LNG S.A E.S.P'
                GROUP BY
                    OF.fecha
                ORDER BY 
                    OF.fecha ASC;
            '''

        return self.db.engine.execute(text(sql),start_date = start_date, end_date = end_date).fetchall()

    def get_operational_values(self):
        sql = '''
                SELECT 
                    planta, 
                    maximo_operativo,
                    minimo_operativo
                FROM xm_files.gmg_inventarios_total_planta
            '''

        return self.db.engine.execute(text(sql)).fetchall()