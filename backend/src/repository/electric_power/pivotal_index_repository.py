from sqlalchemy.sql import text

class PivotalIndexRepository:
    def __init__(self, db):
        self.db = db

    def find_by_date_range_and_agent(self, agent_code, start_date, end_date):
        sql = '''SELECT 
                    codigo, nombre, min, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", fecha, archivo, id
                from
                    xm_files.xm_indices_pivotales I
                WHERE 
                    I.fecha BETWEEN :start_date AND :end_date AND codigo = :agent_code
                order by 
                    I.fecha'''

        print(start_date, end_date, agent_code)

        return self.db.engine.execute(text(sql),
                                      start_date=start_date, 
                                      end_date=end_date,
                                      agent_code=agent_code).fetchall()