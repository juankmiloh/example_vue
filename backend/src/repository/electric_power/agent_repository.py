from sqlalchemy.sql import text

class AgentRepository:
    def __init__(self, db):
        self.db = db

    def find_all(self):
        sql = '''
            SELECT 
                codigo_agente,
                nombre_agente
            FROM 
                xm_files.xm_agentes
        '''
        return self.db.engine.execute(text(sql)).fetchall()
