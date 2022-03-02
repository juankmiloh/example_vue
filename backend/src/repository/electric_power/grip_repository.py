from sqlalchemy.sql import text

class GRIPRepository:
    def __init__(self, db):
        self.db = db

    def find_accumulated_by_plant_id(self, start_date, end_date, pant_id):
        sql = '''SELECT 
                    P.codigo_planta,
                    P.planta,
                    A.nombre_agente,
                    L.fecha,
                    SUM (L.grea) acc_grea,
                    SUM (L.gpro) acc_gpro
                from
                    xm_files.xm_plantas P
                    left join xm_files.xm_agentes A
                    ON (P.codigo_agente = A.codigo_agente)
                    LEFT JOIN xm_files.xm_liquidacion_grip_acc L
                    ON (P.codigo_planta = L.planta)
                WHERE 
                    L.fecha BETWEEN :start_date AND :end_date
                    AND P.despachado_centralmente = 1
                    AND P.codigo_planta = :pant_id
                GROUP BY 
                    L.fecha,
                    P.codigo_planta,
                    P.planta,
                    A.nombre_agente
                order by 
                    A.nombre_agente,
                    P.planta'''

        return self.db.engine.execute(text(sql),
                                      start_date=start_date, 
                                      end_date=end_date,
                                      pant_id=pant_id).fetchall()
                                      
    def find_accumulated_by_plant(self, start_date, end_date):
        sql = '''SELECT 
                    P.codigo_planta,
                    P.planta,
                    A.nombre_agente,
                    L.fecha,
                    SUM (L.grea) acc_grea,
                    SUM (L.gpro) acc_gpro
                from
                    xm_files.xm_plantas P
                    left join xm_files.xm_agentes A
                    ON (P.codigo_agente = A.codigo_agente)
                    LEFT JOIN xm_files.xm_liquidacion_grip_acc L
                    ON (P.codigo_planta = L.planta)
                WHERE 
                    L.fecha BETWEEN :start_date AND :end_date
                    AND P.despachado_centralmente = 1
                GROUP BY 
                    L.fecha,
                    P.planta,
                    P.codigo_planta,
                    A.nombre_agente
                order by 
                    A.nombre_agente,
                    P.planta,
                    P.codigo_planta'''

        return self.db.engine.execute(text(sql),
                                      start_date=start_date, 
                                      end_date=end_date).fetchall()
                                      
    def find_accumulated_by_agent_id(self, start_date, end_date, agent_id):

        sql = '''SELECT 
                    A.codigo_agente,
                    A.nombre_agente,
                    A.codigo_agente,
                    L.fecha,
                    SUM (L.grea) acc_grea,
                    SUM (L.gpro) acc_gpro
                from
                    xm_files.xm_plantas P
                    left join xm_files.xm_agentes A
                    ON (P.codigo_agente = A.codigo_agente)
                    LEFT JOIN xm_files.xm_liquidacion_grip_acc L
                    ON (P.codigo_planta = L.planta)
                WHERE 
                    L.fecha BETWEEN :start_date AND :end_date
                    AND P.despachado_centralmente = 1
                    AND P.codigo_agente = :agent_id
                GROUP BY 
                    L.fecha,
                    A.codigo_agente,
                    A.nombre_agente
                order by 
                    A.nombre_agente'''

        return self.db.engine.execute(text(sql),
                                      start_date=start_date, 
                                      end_date=end_date,
                                      agent_id=agent_id).fetchall()

    def find_accumulated_by_agent(self, start_date, end_date):
        sql = '''SELECT 
                    A.codigo_agente,
                    A.nombre_agente,
                    A.codigo_agente,
                    L.fecha,
                    SUM (L.grea) acc_grea,
                    SUM (L.gpro) acc_gpro
                from
                    xm_files.xm_plantas P
                    left join xm_files.xm_agentes A
                    ON (P.codigo_agente = A.codigo_agente)
                    LEFT JOIN xm_files.xm_liquidacion_grip_acc L
                    ON (P.codigo_planta = L.planta)
                WHERE 
                    L.fecha BETWEEN :start_date AND :end_date
                    AND P.despachado_centralmente = 1
                    AND L.grea is not null
                    AND L.gpro is not null
                GROUP BY 
                    L.fecha,
                    A.codigo_agente,
                    A.nombre_agente
                order by 
                    A.nombre_agente'''

        return self.db.engine.execute(text(sql),
                                      start_date=start_date, 
                                      end_date=end_date).fetchall()

    def find_accumulated(self, start_date, end_date):
        sql = '''SELECT 
                    L.fecha,
                    SUM (L.grea) acc_grea,
                    SUM (L.gpro) acc_gpro
                from
                    xm_files.xm_plantas P
                    LEFT JOIN xm_files.xm_liquidacion_grip_acc L
                    ON (P.codigo_planta = L.planta)
                WHERE 
                    L.fecha BETWEEN :start_date AND :end_date
                    AND P.despachado_centralmente = 1
                GROUP BY 
                    L.fecha'''

        return self.db.engine.execute(text(sql),
                                      start_date=start_date, 
                                      end_date=end_date).fetchall()


    def find_disponibility_by_agent(self, date):

        sql = '''
            SELECT 
                L.hora,
                A.codigo_agente,
                A.nombre_agente,
                SUM(L.drea::float) acc_drea
            FROM
                xm_files.xm_plantas P
                left join xm_files.xm_agentes A
                ON (P.codigo_agente = A.codigo_agente)
                LEFT JOIN xm_files.xm_liquidacion_grip L
                ON (P.codigo_planta = L.planta)
            WHERE 
                L.fecha = :date
                AND P.despachado_centralmente = 1
                AND L.drea is not null
            GROUP BY 
                L.hora,
                A.codigo_agente,
                A.nombre_agente
            ORDER BY 
                L.hora'''

        return self.db.engine.execute(text(sql), date=date).fetchall()

    def find_total_disponibility(self, date):
        sql = '''
            SELECT 
                L.hora,
                SUM(L.drea::float) acc_drea
            FROM
                xm_files.xm_plantas P
                left join xm_files.xm_agentes A
                ON (P.codigo_agente = A.codigo_agente)
                LEFT JOIN xm_files.xm_liquidacion_grip L
                ON (P.codigo_planta = L.planta)
            WHERE 
                L.fecha = :date
                AND P.despachado_centralmente = 1
                AND L.drea is not null
            GROUP BY 
                L.hora
            ORDER BY 
                L.hora'''
            
        return self.db.engine.execute(text(sql), date=date).fetchall()
