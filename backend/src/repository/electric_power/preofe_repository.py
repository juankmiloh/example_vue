from sqlalchemy.sql import text

class PreofeRepository:
    def __init__(self, db):
        self.db = db

    def find(self, finicial, ffinal):
        sql = '''SELECT 
                    P.id_planta, 
                    A.nombre_agente, 
                    P.planta,
                    PO.oferta,
                    PO.fecha
                FROM 
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_precios_oferta_diaria PO
                where
                    TRIM(PO.codigo_planta) = TRIM(P.codigo_alternativo)
                AND A.codigo_agente = P.codigo_agente
                AND (
                    PO.fecha = :finicial
                    or PO.fecha = :ffinal
                )
                ORDER BY
                    PO.fecha
                ASC'''

        return self.db.engine.execute(text(sql), finicial=finicial.strftime("%Y-%m-%d"), ffinal =ffinal.strftime("%Y-%m-%d")).fetchall()
        
    def find_by_plant_id(self, idPlanta, finicial, ffinal):
        sql = '''SELECT 
                    P.id_planta, 
                    A.nombre_agente, 
                    P.planta,
                    PO.oferta,
                    PO.fecha
                FROM 
                    xm_files.xm_agentes A, 
                    xm_files.xm_plantas P,
                    xm_files.xm_precios_oferta_diaria PO
                where
                    P.id_planta = :idPlanta
                AND TRIM(PO.codigo_planta) = TRIM(P.codigo_alternativo)
                AND A.codigo_agente = P.codigo_agente
                AND PO.fecha BETWEEN :finicial AND :ffinal
                ORDER BY
                    PO.fecha
                ASC'''

        return self.db.engine.execute(text(sql),
                                    idPlanta = idPlanta,
                                    finicial= finicial.strftime("%Y-%m-%d"), 
                                    ffinal = ffinal.strftime("%Y-%m-%d")
                                ).fetchall()
        
