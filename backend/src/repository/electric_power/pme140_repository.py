from sqlalchemy.sql import text

class PME140Repository:

    def __init__(self, db):
        self.db = db

    def find_by_year(self, year):
        sql = '''SELECT
                    to_char(RP.fecha,'yyyy/mm') AS month,
                    RP.pe, 
                    RP.pea, 
                    RP.pme
                FROM
                    xm_files.xm_referencia_precios RP
                WHERE 
                    EXTRACT(YEAR FROM RP.fecha) = :year
                ORDER BY
                    month
                ASC'''
        return self.db.engine.execute((text(sql)), year=year).fetchall()
        