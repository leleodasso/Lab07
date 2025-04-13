from database.DB_connect import DBConnect



class MeteoDao():



    @staticmethod
    def getUmiditaAvg(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, avg(s.Umidita) 
                        FROM situazione s 
                        where month(s.`Data`)="%s"
                        group by s.Localita;
                        """
            cursor.execute(query, (mese,))

            result = cursor.fetchall()

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getCostoGiornalieroGenova(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.`Data`  ,s.Umidita
                        FROM situazione s 
                        where month(s.`Data`)="%s" and s.Localita ='Genova' 
                           """
            cursor.execute(query, (mese,))

            result = cursor.fetchall()

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getCostoGiornalieroMilano(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.`Data`  ,s.Umidita
                           FROM situazione s 
                           where month(s.`Data`)="%s" and s.Localita ='Milano' 
                              """
            cursor.execute(query, (mese,))

            result = cursor.fetchall()

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getCostoGiornalieroTorino(mese):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.`Data`  ,s.Umidita
                           FROM situazione s 
                           where month(s.`Data`)="%s" and s.Localita ='Torino' 
                              """
            cursor.execute(query, (mese,))

            result = cursor.fetchall()

            cursor.close()
            cnx.close()
        return result



if __name__ == '__main__':
    meteo = MeteoDao()
    print(meteo.get_all_situazioni())
    print("-------------")
    print(meteo.getUmiditaAvg(1))
    print(meteo.getCostoGiornalieroGenova(1))
    print(meteo.getCostoGiornalieroMilano(1))
    print(meteo.getCostoGiornalieroTorino(1))