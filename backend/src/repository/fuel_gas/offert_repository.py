from sqlalchemy.sql import text

class OffertRepository:
    def __init__(self, db):
        self.db = db

    def find_offert_by_group(self, date_ini, date_fin, group):
        sql = '''
                select 
                    o.fecha,  
                    sum(o.oferta)/1000 
                from xm_files.gmg_oferta o
                    join xm_files.gmg_fuentes f on upper(REGEXP_REPLACE(f.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) = upper(REGEXP_REPLACE(o.campo, '[ñáéíóúüÑÁÉÍÓÚÜ]', ''))
                where
                    f.grupo = :grupo
                and o.fecha between :fechaini ::DATE and :fechafin ::DATE
                group by o.fecha, f.grupo
                union
                select
                    gt.fecha, gt.oferta - gi.oferta oferta
                from 
                    (	
                        select o1.fecha,  sum(o1.oferta)/1000 oferta
                        from xm_files.gmg_oferta o1
                        join xm_files.gmg_fuentes f1 on upper(REGEXP_REPLACE(f1.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) = upper(REGEXP_REPLACE(o1.campo, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) 
                        where f1.grupo = 'Guajira Total'
                        group by o1.fecha, f1.grupo
                    ) gt,
                    (	
                        select o2.fecha,  sum(o2.oferta)/1000 oferta
                        from xm_files.gmg_oferta o2
                        join xm_files.gmg_fuentes f2 on upper(REGEXP_REPLACE(f2.fuente, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) = upper(REGEXP_REPLACE(o2.campo, '[ñáéíóúüÑÁÉÍÓÚÜ]', '')) 
                        where f2.grupo = 'Guajira Interior'
                        group by o2.fecha, f2.grupo
                    ) gi
                where
                gt.fecha = gi.fecha
                and 'Guajira Costa' in (:grupo)
                and	 gt.fecha between :fechaini ::DATE and :fechafin ::DATE

            '''

        return self.db.engine.execute(text(sql),fechaini = date_ini, fechafin = date_fin, grupo = group).fetchall()
