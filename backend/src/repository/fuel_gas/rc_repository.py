from sqlalchemy.sql import text


class RCRepository:
    def __init__(self, db):
        self.db = db

    def find_regasification_cost_by_date_range(self, start_date, end_date):
        sql = '''SELECT 
                    f.nit,
                    f.nombre_agente,
                    C.cantidad,
                    C.valor_unidad_ponderado,
                    C.fecha
                FROM
                    xm_files.gmg_costos_regasificacion C 
                JOIN 
                    xm_files.xm_agentes f on 
                    f.nit = C.nit
                WHERE
                    c.fecha <= :end_date
                    AND c.fecha >= :start_date
                ORDER BY
                    c.fecha ASC'''

        return self.db.engine.execute(text(sql), start_date=start_date, end_date=end_date).fetchall()
    
    def find_plants(self):
        sql = '''
            SELECT 
                distinct f.nombre_agente,
                f.nit
            FROM 
                xm_files.gmg_costos_regasificacion C 
            JOIN 
                xm_files.xm_agentes f on 
                f.nit = C.nit
            ORDER BY 
                f.nombre_agente asc
        '''

        return self.db.engine.execute(text(sql),).fetchall()
