from sqlalchemy.sql import text

class DaggiRepository:
    def __init__(self, db):
        self.db = db

    #No utilizado por cambios del indicador
    def find_installed_capacity_agent_by_date(self, start_date, end_date):
        sql=''' SELECT 
                    C.fecha AS fecha,
                    P.codigo_agente,
                    SUM(capacidad_instalada) AS capacidad
                FROM 
                    xm_files.xm_capacidad_instalada C,
					xm_files.xm_plantas P
                WHERE 
                    C.fecha BETWEEN :start_date AND :end_date
                    AND C.planta = P.codigo_planta
                GROUP BY
                    C.fecha,
                    P.codigo_agente; '''
        return self.db.engine.execute(text(sql), start_date=start_date, end_date=end_date).fetchall()

    #No utilizado por cambios del indicador
    def find_grea_agent_by_date(self, start_date, end_date):
        sql = ''' SELECT 
                    G.fecha AS fecha,
                    P.codigo_agente,
                    SUM(G.grea) AS capacidad
                FROM 
                    xm_files.xm_liquidacion_grip_acc G,
					xm_files.xm_plantas P
                WHERE
                    G.fecha BETWEEN :start_date AND :end_date
                    AND G.planta = P.codigo_planta
                GROUP BY
                    G.fecha,
                    P.codigo_agente'''
        return self.db.engine.execute(text(sql), start_date=start_date, end_date=end_date).fetchall()

    def find_inventory_by_date(self, start_date, end_date):
        sql = '''SELECT 
                    I.fecha,
                    I.planta,  
                    I.cantidad
                FROM 
					xm_files.gmg_inventarios_planta I
                WHERE
                    I.fecha between :start_date and :end_date
                    AND planta <> 'Total'
                ORDER BY
                    I.fecha ASC,
                    I.planta ASC'''
        return self.db.engine.execute(text(sql), start_date=start_date, end_date=end_date).fetchall()

    def find_total_inventory(self, utilizar_oef):
        sql = '''SELECT 
                    fecha, 
                    planta, 
                    SUM({})
                FROM 
                    xm_files.gmg_inventarios_total_planta
                WHERE id_gmg_inventarios_total_planta IN (SELECT 
                        MAX(id_gmg_inventarios_total_planta) 
                    FROM 
                        xm_files.gmg_inventarios_total_planta 
                    GROUP BY 
                        planta)
                GROUP BY 
                    fecha, 
                    planta
                ORDER BY 
                    fecha DESC,
                    planta ASC;'''.format("obligacion_energia_firme" if utilizar_oef else "cantidad")
        return self.db.engine.execute(text(sql)).fetchall()

    def find_consuption_percentage(self, date, days, utilizar_oef):
        sql = '''SELECT
                    A2.nombre,
                    A.promedio_gani / 1000 / I.{total} AS porcentaje_gani,
                    (I.{total} - A.promedio_gasn / 1000) / I.{total} AS porcentaje_gani_compl,
                    A.promedio_gasn / 1000 AS promedio_gasn
                FROM
                    xm_files.gmg_inventarios_total_planta I
                    LEFT JOIN  general.agente A2 ON ( A2.nombre LIKE '%' || UPPER(I.planta) || '%') AND A2.codigo <> 'TCDG'
                    LEFT JOIN 
                    -- PROMEDIO TOTAL DIARIO
                    (SELECT 
                        A.nombre,
                        A.codigo,
                        SUM(A.gani)/:days as promedio_gani,
                        SUM(A.gasn)/:days as promedio_gasn
                    FROM
                        -- SUMA DIARIA
                        (SELECT 
                            A.nombre, 
                            A.codigo, 
                            C.dia, 
                            SUM(COALESCE(C.gani, 0)) AS gani,
                            SUM(COALESCE(C.gasn, 0) + COALESCE(C.crec, 0)) as gasn
                        FROM 
                            xm_files.xm_consumo C
                            LEFT JOIN general.planta P ON (C.recurso = P.codigo)
                            LEFT JOIN general.agente A ON (P.id_agente = A.id)
                        WHERE C.dia > (:date - interval ':days day') 
                            AND C.dia <= :date 
                            AND A.codigo IN ('TBSG','TMFG','TCIG')
                        GROUP BY 
                            C.dia, 
                            A.nombre, 
                            A.codigo) A
                    GROUP BY
                        A.nombre,
                        A.codigo) A
                    ON ( A.nombre LIKE '%' || UPPER(I.planta) || '%') 
                ORDER BY
                    A2.nombre DESC '''.replace("{total}", "obligacion_energia_firme" if utilizar_oef else "cantidad")
        return self.db.engine.execute(text(sql), date=date, days=days,).fetchall()
