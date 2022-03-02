from sqlalchemy.sql import text

class SourceRepository:
    def __init__(self, db):
        self.db = db

    def find_all(self, has_not_guajira_costa = True):
        sql = '''
            select 
                distinct grupo 
            from xm_files.gmg_fuentes
        '''
        if not has_not_guajira_costa:
            sql += '''
                where
                    grupo not in ('Guajira Total')
                union
                select 'Guajira Costa'
            ''' 
        sql +=  ''' 
                order by grupo asc
            '''

        return self.db.engine.execute(text(sql),).fetchall()
    
    def find_grupo_2(self):
        sql = '''
            select 
                distinct grupo, grupo_2 
            from xm_files.gmg_fuentes
            order by grupo_2 asc
        '''

        return self.db.engine.execute(text(sql),).fetchall()
    
    
    def find_plants(self):
        sql = '''
            select 
                id_planta,
                planta
            from 
                xm_files.xm_plantas
            order 
                by planta asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()

    def find_activos(self):
        sql = '''
            select 
                DISTINCT activoid,
                activo
            from 
                xm_files.xm_eventos_transmision
            order 
                by activo asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()

    def find_agents(self):
        sql = '''
            select 
                DISTINCT agenteid,
                agenteid
            from 
                xm_files.xm_eventos_transmision
            order 
                by agenteid asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()

    def find_causes(self):
        sql = '''
            select 
                DISTINCT causaid,
                causa
            from 
                xm_files.xm_eventos_generacion
            order 
                by causaid asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()

    def find_techs(self):
        sql = '''
            select 
                DISTINCT combustible,
                combustible
            from 
                xm_files.xm_eventos_generacion
            order 
                by combustible asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()

    def find_generation_agents(self):
        sql = '''
            select 
                DISTINCT id,
                nombre
                
            from 
                xm_files.xm_agentes_eventos
            order 
                by nombre asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()

    def find_generation_plants(self):
        sql = '''
            select 
                DISTINCT plantaid,
                plantaid
            from 
                xm_files.xm_eventos_generacion
            order 
                by plantaid asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()

    def find_sectors(self):
        sql = '''
            select 
                DISTINCT descripcion_sector_consumo,
                descripcion_sector_consumo
            from 
                xm_files.gmg_usuarios_finales
            where
                descripcion_sector_consumo IS NOT NULL
            order 
                by descripcion_sector_consumo asc
        '''
        return self.db.engine.execute(text(sql),).fetchall()
