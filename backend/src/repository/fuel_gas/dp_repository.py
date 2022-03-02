from sqlalchemy.sql import text


class DPRepository:
    def __init__(self, db):
        self.db = db

    def find_accumulated_dp(self,
                            date,
                            end_date,
                            markets,
                            modalities,
                            sectors,
                            sources):
        sql = '''
            SELECT
                c.fecha_inicial,
                COUNT(c.precio) AS "cantidad",
                SUM(c.precio) AS "suma_precio",
                c.mercado, 
                c.modalidad,
                f.grupo,
                a.descripcion_sector_consumo
            FROM 
                xm_files.gmg_contratos c
            JOIN
                xm_files.gmg_usuarios_finales a
            ON
	            a.no_operacion = c.no_operacion
            JOIN
                xm_files.gmg_fuentes f
            ON
                UPPER(REGEXP_REPLACE(f.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) = UPPER(REGEXP_REPLACE(c.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', ''))
            WHERE
                c.fecha_inicial <= :fecha
                AND c.fecha_final >= :fecha_final
                AND c.mercado IN :mercados
                AND c.modalidad IN :modalidades
                AND a.descripcion_sector_consumo IN :sectores
                AND f.grupo IN :fuentes
            GROUP BY
                c.fecha_inicial,
                c.id_gmg_contratos,
                c.mercado,
                c.modalidad,
                f.grupo,
                a.descripcion_sector_consumo'''

        return self.db.engine.execute(text(sql),
                                      fecha=date,
                                      fecha_final=date if end_date is None else end_date,
                                      mercados=tuple(markets),
                                      modalidades=tuple(modalities),
                                      sectores=tuple(sectors),
                                      fuentes=tuple(sources)).fetchall()

    def find_accumulated_dp_for_secundaries(self,
                                            date,
                                            end_date,
                                            markets,
                                            modalities,
                                            sectors,
                                            sources):
        sql = '''
            SELECT
                c.fecha_inicial,
                COUNT(c.precio) AS "cantidad",
                SUM(c.precio) AS "suma_precio",
                c.mercado, 
                c.modalidad,
                f.grupo,
                a.descripcion_sector_consumo
            FROM 
                xm_files.gmg_contratos c
            JOIN
                xm_files.gmg_usuarios_finales a
            ON
                a.no_operacion = c.no_operacion
            LEFT OUTER JOIN
                xm_files.gmg_fuentes f
            ON
                UPPER(REGEXP_REPLACE(f.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) = UPPER(REGEXP_REPLACE(c.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', ''))
            WHERE
                c.fecha_inicial <= :fecha
                AND c.fecha_final >= :fecha_final
                AND c.mercado IN :mercados
                AND c.modalidad IN :modalidades
                AND a.descripcion_sector_consumo IN :sectores
                AND (f.grupo IN :fuentes OR f.fuente IS NULL)
            GROUP BY
                c.fecha_inicial,
                c.id_gmg_contratos,
                c.mercado,
                c.modalidad,
                f.grupo,
                a.descripcion_sector_consumo'''

        return self.db.engine.execute(text(sql),
                                    fecha=date,
                                    fecha_final=date if end_date is None else end_date,
                                    mercados=tuple(markets),
                                    modalidades=tuple(modalities),
                                    sectores=tuple(sectors),
                                    fuentes=tuple(sources)).fetchall()
