from database.DB_connect import DBConnect



class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from state"

        cursor.execute(query)

        for row in cursor:
            #results.append(row["order_date"])
            continue


        cursor.close()
        conn.close()
        return None