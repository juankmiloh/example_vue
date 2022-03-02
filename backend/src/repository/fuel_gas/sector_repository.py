from sqlalchemy.sql import text


class SectorRepository:
    def __init__(self, db):
        self.db = db

    def find_all(self):
        sql = '''
            SELECT
                distinct descripcion_sector_consumo
            FROM 
                xm_files.gmg_usuarios_finales
            WHERE
                descripcion_sector_consumo IS NOT NULL
        '''
        return self.db.engine.execute(text(sql)).fetchall()
