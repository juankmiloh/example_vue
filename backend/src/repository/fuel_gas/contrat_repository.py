import datetime
import calendar
from sqlalchemy.sql import text
from pypika import functions as fn
from pypika.terms import Function
from pypika import Query, Table, Field, Order, Case

SHOPPER = "comprador"
SELLER = "vendedor"
PRICE = "precio"
PRODUCT = "Suministro de Gas"

class StringAgg(Function):
    def __init__(self, input1, input2):
        super(StringAgg, self).__init__('string_agg' , input1, input2)

class DatePart(Function):
    def __init__(self, input1, input2):
        super(DatePart, self).__init__('date_part', input1, input2)

class Upper(Function):
    def __init__(self, input1):
        super(Upper, self).__init__('upper', input1)

class ContratRepository:
    def __init__(self, db):
        self.db = db

    def find_accumulated_by_agent(self, date):
        sql = '''SELECT 
                    C.nombre_vendedor,
                    sum(C.cantidad) "CANTIDAD",
                    min(C.fecha_inicial),
                    max(C.fecha_final)
                from
                    xm_files.gmg_contratos C
                WHERE 
                    :date BETWEEN C.fecha_inicial AND C.fecha_final
                    AND C.rol_vendedor = 'PRODUCTOR-COMERCIALIZADOR'
                    AND C.producto = 'Suministro de Gas'
                GROUP BY 
                    C.nombre_vendedor
                order by 
                    "CANTIDAD"
                DESC
                    '''

        return self.db.engine.execute(text(sql),
                                      date=date).fetchall()

    def find_accumulated_by_price_modality_and_shopper(self, date):
        sql = '''SELECT 
                    C.nombre_vendedor,
                    C.nombre_comprador,
                    C.precio,
                    sum(C.cantidad) "CANTIDAD",
                    C.modalidad_homologado,
                    min(C.fecha_inicial),
                    max(C.fecha_final)
                from
                    xm_files.gmg_contratos C
                WHERE 
                    :date BETWEEN C.fecha_inicial AND C.fecha_final
                GROUP BY 
                    C.nombre_vendedor,
                    C.nombre_comprador,
                    C.precio,
                    C.modalidad_homologado
                order by 
                    C.nombre_vendedor'''

        return self.db.engine.execute(text(sql),
                                      date=date).fetchall()

    def find_accumulated_by_price_and_modality(self, date):
        sql = '''SELECT 
                    C.nombre_vendedor,
                    string_agg(C.nombre_comprador, '; ') "COMPRADORES", 
                    C.precio,
                    sum(C.cantidad) "CANTIDAD",
                    C.modalidad_homologado,
                    min(C.fecha_inicial),
                    max(C.fecha_final)
                from
                    xm_files.gmg_contratos C
                WHERE 
                    :date BETWEEN C.fecha_inicial AND C.fecha_final
                GROUP BY 
                    C.nombre_vendedor,
                    C.precio,
                    C.modalidad_homologado
                order by 
                    C.nombre_vendedor'''

        return self.db.engine.execute(text(sql),
                                      date=date).fetchall()

    def find_accumulated_by_price_and_agent(self, date, modalida, source=[], 
                    market=[], starting_year=[], role=None, agent_type=None):

        init_date = datetime.date(date.year,date.month, 1)
        end_date = datetime.date(date.year,date.month, calendar.monthrange(date.year,date.month)[1])
       
        F = Table('gmg_fuentes', schema = 'xm_files')
        C = Table('gmg_contratos', schema = 'xm_files')
        sql = Query

        if agent_type != SHOPPER:
            sql = sql.select(C.nombre_vendedor)
            
            # sql = sql.groupby(C.precio)
            # sql = sql.groupby(C.nombre_vendedor)
        else:
            sql = sql.select(C.nombre_comprador)

        #     sql = sql.groupby(C.precio)
        #     sql = sql.groupby(C.nombre_comprador)


        sql = sql.select(
            C.precio,
            C.cantidad,
            Case()
                .when(C.fecha_final < end_date, C.fecha_final)
                .else_(end_date) -
            Case()
                .when(C.fecha_inicial >  init_date, C.fecha_inicial)
                .else_(init_date)
        )

        sql = sql.from_(C) 
        sql = sql.from_(F) 
        sql = sql.orderby(C.precio, order=Order.asc)
        sql = sql.where(C.modalidad_homologado == modalida)
        sql = sql.where(C.producto == PRODUCT)


        if source:
            sql = sql.where(Upper(C.fuente) == Upper(F.fuente))
            sql = sql.where(F.grupo.isin(source))
            
        if market:
            sql = sql.where(C.mercado.isin(market))
        
        if starting_year:
            sql = sql.where(DatePart('year', C.fecha_inicial).isin(starting_year))

        # if role is not None:
        #     sql = sql.where(C.rol_vendedor == role)
        
        sql = sql.where((C.fecha_inicial <= init_date) & (C.fecha_final >= init_date))
        
        print(sql.get_sql())
        return self.db.engine.execute(sql.get_sql()).fetchall()

    def find_accumulated_by_custom_filter(self, date, group_by=[], 
            source=[], market=[], starting_year=[], agent_type=None, role=None, sector=[], modality=[]):

        C = Table('gmg_contratos', schema = 'xm_files')
        U = Table('gmg_usuarios_finales', schema = 'xm_files')
        sql = Query

        if agent_type != SHOPPER:
            sql = sql.select(C.nombre_vendedor)
            if PRICE in group_by:
                sql = sql.select(StringAgg(C.nombre_comprador, '; '))
            else:
                sql = sql.select(C.nombre_comprador)
        else:
            sql = sql.select(C.nombre_comprador)
            if PRICE in group_by:
                sql = sql.select(StringAgg(C.nombre_vendedor, '; '))
            else:
                sql = sql.select(C.nombre_vendedor)

        
        
        

        sql = sql.select(
            C.precio,
            fn.Sum(C.cantidad),
            C.modalidad_homologado,
            fn.Min(C.fecha_inicial),
            fn.Max(C.fecha_final),
            C.fuente,
            C.mercado,
            fn.Sum(C.cantidad))

        
        sql = sql.from_(C)
        sql = sql.groupby(
            C.precio,
            C.fuente,
            C.mercado,
            C.modalidad_homologado)

        sql = sql.join(U).on_field('no_operacion', 'id_registro')
        sql = sql.select(
            U.descripcion_sector_consumo)
        sql = sql.groupby(
            U.descripcion_sector_consumo)

        if sector:
            sql = sql.where(
                U.descripcion_sector_consumo.isin(sector))
        if modality:
            sql = sql.where(
                C.modalidad.isin(modality))

        if agent_type != SHOPPER:
            sql = sql.groupby(C.nombre_vendedor)
            if PRICE not in group_by:
                sql = sql.groupby(C.nombre_comprador)
        else:
            sql = sql.groupby(C.nombre_comprador)
            if PRICE not in group_by:
                sql = sql.groupby(C.nombre_vendedor)
        
        if agent_type != SHOPPER:
            sql = sql.orderby(C.nombre_vendedor, order=Order.asc)
        else:
            sql = sql.orderby(C.nombre_comprador, order=Order.asc)
        sql = sql.where((C.fecha_inicial <= date) & (C.fecha_final >= date))
        sql = sql.where(C.producto == PRODUCT)
        
        if source:
            sql = sql.where(C.fuente.isin(source))
            
        if market:
            sql = sql.where(C.mercado.isin(market))
        
        if starting_year:
            sql = sql.where(DatePart('year', C.fecha_inicial).isin(starting_year))

        if role is not None:
            sql = sql.where(C.rol_vendedor == role)

        return self.db.engine.execute(sql.get_sql()).fetchall()

    def find_accumulated_by_price_and_agent_and_date (self, date, group):
        sql = '''SELECT 
                    f.grupo,
                    C.fuente, 
                    C.precio, 
                    C.cantidad
                FROM
                    xm_files.gmg_contratos C 
                JOIN 
                    xm_files.gmg_fuentes f on 
                    upper(REGEXP_REPLACE(f.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) = upper(REGEXP_REPLACE(C.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', ''))
                WHERE 
                    upper(C.modalidad_homologado)= 'FIRME' 
                    AND upper (C.mercado) = 'PRIMARIO'
                    AND  f.grupo = :group
                    AND :date BETWEEN C.fecha_inicial AND C.fecha_final
                ORDER BY 
                    C.precio ASC'''

        return self.db.engine.execute(text(sql), date=date, group=group).fetchall()
    
    def get_price_import (self, date):
        sql = '''SELECT 
                    PI.precio_pago
                FROM
                    xm_files.gmg_precios_importacion PI
                WHERE 
                    :date >= PI.fecha_subasta
                ORDER BY 
                    PI.fecha_subasta DESC
                LIMIT 1'''

        return self.db.engine.execute(text(sql), date=date).fetchall()