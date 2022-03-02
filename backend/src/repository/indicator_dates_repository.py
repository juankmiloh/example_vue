from sqlalchemy.sql import text

class IndicatorDateRepository:
    def __init__(self, db):
        self.db = db

    def get_valid_range_by_tables(self, tables):
        sql ='''SELECT MIN(fecha_final),
                        MAX(fecha_inicial)
                FROM
                (
                    SELECT  
                        tabla,
                        fecha_final,
                        fecha_inicial 
                    FROM  
                        xm_files.xm_info_tablas
                ) as a
                WHERE
                    tabla in (\'''' + "','".join(tables) + '\')'
        return self.db.engine.execute(text(sql)).fetchall()
    
    def get_valid_range_for_ihh(self):
        sql ='''SELECT 
                    MAX(e.fecha),
                    MIN(e.fecha)
                FROM
                    energia.hhi_acumulado e'''
        return self.db.engine.execute(text(sql)).fetchall()

    def get_valid_range_for_iar(self):
        sql ='''SELECT 
                    MAX(e.fecha),
                    MIN(e.fecha)
                FROM
                    xm_files.xm_eventos_transmision e'''
        return self.db.engine.execute(text(sql)).fetchall()

    def get_valid_range_for_pivotal(self):
        sql ='''SELECT 
                    MAX(t.fecha),
                    MIN(t.fecha)
                FROM
                    xm_files.xm_transacciones_mem t
                WHERE
                    t.dmnd is not null
                '''
        data_range = self.db.engine.execute(text(sql)).fetchall()
        sql ='''SELECT 
                    MAX(g.fecha),
                    MIN(g.fecha)
                FROM
                    xm_files.xm_liquidacion_grip g
                WHERE
                    g.drea is not null
                '''
        data_range_2 = self.db.engine.execute(text(sql)).fetchall()
        data_range[0] = (
            data_range[0][0] if data_range[0][0] < data_range_2[0][0].date() else data_range_2[0][0],
            data_range[0][1] if data_range[0][1] > data_range_2[0][1].date() else data_range_2[0][1]
        )
        return data_range

    def get_valid_range_for_iag(self):
        sql ='''SELECT 
                    MAX(e.fecha),
                    MIN(e.fecha)
                FROM
                    xm_files.xm_eventos_generacion e'''
        return self.db.engine.execute(text(sql)).fetchall()


    def get_dmnd_last_date(self):
        sql = '''
            SELECT 
                MAX(tm.fecha) 
            FROM 
                xm_transacciones_mem tm 
            WHERE 
                tm.dmnd is not null 
            '''
        return self.db.engine.execute(text(sql)).fetchall()
    
    def get_dp_last_date(self):
        sql = '''
            SELECT 
                MAX(c.fecha_suscripcion) 
            FROM 
                xm_files.gmg_contratos c
            WHERE 
                c.modalidad is not null AND
                c.mercado is not null AND
                c.no_operacion is not null AND
                c.fuente is not null
            '''
        return self.db.engine.execute(text(sql)).fetchall()
    
    
        
