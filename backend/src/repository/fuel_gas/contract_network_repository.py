from sqlalchemy.sql import text
import pandas as pd

class ContractNetworkRepository:
    def __init__(self, db):
        self.db = db

    def find_contracts_by_date(self, start_date, end_date, modality):
        '''
        sql = """SELECT 
                    U.nombre_usuario_final,
                    U.codigo_sector_consumo,
                    U.descripcion_sector_consumo,
                    U.id_gmg_usuarios_finales,
                    C.nombre_comprador,
                    C.codigo_comprador,
                    C.nombre_vendedor,
                    C.codigo_vendedor, 
                    C.cantidad, 
                    C.precio,
                    C.fecha_inicial, 
                    C.fecha_final,
                    mercado
                FROM 
                    xm_files.gmg_contratos C
                INNER JOIN
                    xm_files.gmg_usuarios_finales U
                ON
                    (C.id_registro = U.id_registro OR C.no_operacion = U.no_operacion)
                WHERE
                    (
                        (C.fecha_inicial <= :start_date AND C.fecha_final >= :end_date)
                        OR (C.fecha_inicial BETWEEN :start_date AND :end_date)
                        OR (C.fecha_final BETWEEN :start_date AND :end_date)
                    )
                    AND U.descripcion_sector_consumo = :consumer_sector
                """ 
        '''

        sql = """SELECT 
                    C.numero_contrato,
                    U.nombre_usuario_final,
                    U.codigo_sector_consumo,
                    U.descripcion_sector_consumo,
                    U.id_gmg_usuarios_finales,
                    C.nombre_comprador,
                    C.codigo_comprador,
                    C.nombre_vendedor,
                    C.codigo_vendedor, 
                    sum(C.cantidad) as cantidad, 
                    sum(C.precio*C.cantidad)/sum(C.cantidad) AS precio,
                    min(C.fecha_inicial) AS fecha_inicial, 
                    max(C.fecha_final) AS fecha_final,
                    mercado
                FROM 
                    xm_files.gmg_contratos C
                INNER JOIN
                    xm_files.gmg_usuarios_finales U
                ON
                    (C.id_registro = U.id_registro OR C.no_operacion = U.no_operacion)
                WHERE
                    (
                        (C.fecha_inicial <= :start_date AND C.fecha_final >= :end_date)
                        OR (C.fecha_inicial BETWEEN :start_date AND :end_date)
                        OR (C.fecha_final BETWEEN :start_date AND :end_date)
                    )
                    AND U.descripcion_sector_consumo = :consumer_sector
                    AND UPPER(C.modalidad) = UPPER(:modality)
                GROUP BY
                    C.numero_contrato,
                    U.nombre_usuario_final,
                    U.codigo_sector_consumo,
                    U.descripcion_sector_consumo,
                    U.id_gmg_usuarios_finales,
                    C.nombre_comprador,
                    C.codigo_comprador,
                    C.nombre_vendedor,
                    C.codigo_vendedor,
                    mercado
                """

        return pd.read_sql_query(
            text(sql), con=self.db.engine, 
            params={'start_date':start_date, 'end_date':end_date,
                    'consumer_sector':'Generación Térmica',
                    'modality':modality
                })

