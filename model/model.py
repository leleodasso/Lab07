from networkx.classes import selfloop_edges

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    def getUmiditaAvg(self, mese):
        return MeteoDao.getUmiditaAvg(mese)


    def recursion(self, mese):
        lista_costoGG_Genova=[]
        for el in MeteoDao.getCostoGiornalieroGenova(mese):
            lista_costoGG_Genova.append(el)
        lista_costoGG_Milano=[]
        for el in MeteoDao.getCostoGiornalieroMilano(mese):
            lista_costoGG_Milano.append(el)
        lista_costoGG_Torino=[]
        for el in MeteoDao.getCostoGiornalieroTorino(mese):
            lista_costoGG_Torino.append(el)
        print(lista_costoGG_Genova)
        return lista_costoGG_Milano

