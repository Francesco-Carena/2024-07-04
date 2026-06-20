from database.DB_connect import DBConnect
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct year(datetime) AS anno from sighting s """

        cursor.execute(query)

        for row in cursor:
            results.append(row["anno"])

        results.sort(reverse=True)
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getShapes(anno):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape
                    from sighting s 
                    where year(s.datetime)=%s"""

        cursor.execute(query, (anno,))

        for row in cursor:
            results.append(row["shape"])

        results.sort()
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getSightings(anno, forma):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from sighting s 
                    where year(s.datetime)=%s and s.shape = %s"""

        cursor.execute(query, (anno,forma))

        for row in cursor:
            results.append(Sighting(**row))

        cursor.close()
        conn.close()
        return results