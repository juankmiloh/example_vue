from sqlalchemy.sql import text

class IHHRepository:
    def __init__(self, db):
        self.db = db

    def find_declared_disponibility_by_plant(self, date):
        sql = '''SELECT 
                    P.id_planta, 
                    P.planta,
                    A.nombre_agente,
                    SUM(G.ddesp) ddesp
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_liquidacion_grip_acc G
                WHERE
                    G.planta = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                    AND G."año" = ':year'
                    AND G."mas" = ':month'
                    AND G."dia" = ':day'
                ORDER BY
                    ddesp
                DESC'''

        return self.db.engine.execute(
            text(sql), 
            year=str(date.year), 
            month="{:02d}".format(date.month), 
            day="{:02d}".format(date.day)).fetchall()

    def find_declared_disponibility_by_agent(self, date):

        sql = '''SELECT 
                    A.id_agente, 
                    A.nombre_agente, 
                    SUM(G.ddesp) ddesp
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_liquidacion_grip_acc G
                WHERE   
                    G.planta = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                    AND G.fecha = :fecha 
                GROUP BY
                    A.id_agente, 
                    A.nombre_agente
                ORDER BY 
                    ddesp
                DESC'''

        return self.db.engine.execute(text(sql),fecha=date).fetchall()

    def find_real_disponibility_by_plant(self, date):
        sql = '''SELECT 
                    P.id_planta, 
                    P.planta,
                    A.nombre_agente,
                    SUM(G.drea) drea
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_liquidacion_grip_acc G
                WHERE
                    G.planta = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                    AND G."año" = ':year'
                    AND G."mas" = ':month'
                    AND G."dia" = ':day'
                ORDER BY
                    drea
                DESC'''

        return self.db.engine.execute(
            text(sql), 
            year=str(date.year), 
            month="{:02d}".format(date.month), 
            day="{:02d}".format(date.day)).fetchall()

    def find_real_disponibility_by_agent(self, date):

        sql = '''SELECT 
                    A.id_agente, 
                    A.nombre_agente, 
                    SUM(G.drea) drea
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_liquidacion_grip_acc G
                WHERE   
                    G.planta = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                    AND G.fecha = :fecha 
                GROUP BY
                    A.id_agente, 
                    A.nombre_agente
                ORDER BY 
                    "drea"
                DESC'''

        return self.db.engine.execute(text(sql),fecha=date).fetchall()

    def find_generation_by_plant(self, date):
        sql = '''SELECT 
                    P.id_planta, 
                    P.planta,
                    A.nombre_agente,
                    SUM(G.drea) grea
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_liquidacion_grip_acc G
                WHERE
                    G.planta = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                    AND G."año" = ':year'
                    AND G."mas" = ':month'
                    AND G."dia" = ':day'
                ORDER BY
                    grea
                DESC'''

        return self.db.engine.execute(
            text(sql), 
            year=str(date.year), 
            month="{:02d}".format(date.month), 
            day="{:02d}".format(date.day)).fetchall()

    def find_generation_by_agent(self, date):

        sql = '''SELECT 
                    A.id_agente, 
                    A.nombre_agente, 
                    SUM(G.grea) grea
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_liquidacion_grip_acc G
                WHERE   
                    G.planta = P.codigo_planta
                    AND P.codigo_agente = A.codigo_agente
                    AND G.fecha = :fecha 
                GROUP BY
                    A.id_agente, 
                    A.nombre_agente
                ORDER BY 
                    grea
                DESC'''

        return self.db.engine.execute(text(sql),fecha=date).fetchall()

    def find_capacity_by_plant(self, date):
        sql = '''SELECT 
                    P.id_planta, 
                    P.planta,
                    A.nombre_agente,
                    SUM (CI.capacidad_instalada) capacidad_instalada
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_capacidad_instalada CI
                WHERE
                    CI.planta = P.codigo_planta
                    AND CI.agente = A.codigo_agente
                    AND CI.fecha = :date
                ORDER by
                    capacidad_instalada
                DESC'''

        return self.db.engine.execute(text(sql), date=date).fetchall()
        
    def find_capacity_by_agent(self, date):
        sql = '''SELECT 
                    A.id_agente, 
                    A.nombre_agente, 
                    SUM (CI.capacidad_instalada) capacidad_instalada
                FROM
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_capacidad_instalada CI
                WHERE
                    CI.planta = P.codigo_planta
                    AND CI.agente = A.codigo_agente
                    AND CI.fecha = :date
                GROUP BY 
                    A.id_agente,
                    A.nombre_agente
                ORDER by
                    capacidad_instalada
                DESC'''

        return self.db.engine.execute(text(sql), date=date).fetchall()
    
    def find_all_ihh(self, start_date, end_date):
        sql = '''SELECT 
                    id, fecha, dis_rea, fij_pre, gen_rea, cap_ins, enficc, archivo
                FROM
                    energia.hhi_acumulado
                WHERE
                    fecha >= :start_date
                    AND fecha <= :end_date
                ORDER by
                    fecha
                ASC'''

        return self.db.engine.execute(text(sql), start_date=start_date, end_date=end_date).fetchall()
        
