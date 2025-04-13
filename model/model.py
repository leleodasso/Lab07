from functools import lru_cache
from networkx.classes import selfloop_edges
from database.meteo_dao import MeteoDao


class Model:

    def __init__(self):
        self.lista_percorsi = [] #la lista in cui metto tutti i percorsi (una lista di liste)
        self.costo_minimo = 100000000
        self.flag_tre_consecutivi = 0


    def getUmiditaAvg(self, mese):
        return MeteoDao.getUmiditaAvg(mese)

#------------------------------------------------------------------
    @lru_cache(maxsize=None)
    def calcola_percorsi(self, mese: int):
        lista_costoGG_Genova = []
        for el in MeteoDao.getCostoGiornalieroGenova(mese):
            lista_costoGG_Genova.append(el)         #Localita, Data, Umidita di genova in quel mese
        lista_costoGG_Milano = []
        for el in MeteoDao.getCostoGiornalieroMilano(mese):
            lista_costoGG_Milano.append(el)         #Localita, Data, Umidita di milano in quel mese
        lista_costoGG_Torino = []
        for el in MeteoDao.getCostoGiornalieroTorino(mese):
            lista_costoGG_Torino.append(el)         #Localita, Data, Umidita di torino in quel mese

        self.lista_percorsi = []  # azzero la lista delle soluzioni
        self.costo_minimo = 100000000
        self.flag_tre_consecutivi = 0

        lista_costoGG_Genova = lista_costoGG_Genova[:15]
        lista_costoGG_Milano = lista_costoGG_Milano[:15]
        lista_costoGG_Torino = lista_costoGG_Torino[:15]

        lista_totali = lista_costoGG_Genova+lista_costoGG_Milano+lista_costoGG_Torino
        self._ricorsione([], lista_totali)
        return self.lista_percorsi

    def _ricorsione(self, lista_usati, lista_disponibili_rimanenti, ):
        # condizione terminale: se la lunghezza della lista che contiene i passi del percorso fatti == 15...allora:
        # il percorso è completato, può essere aggiunto alla lista di tutti i percorsi possibile
        if len(lista_usati) == 15:
            costo_attuale = 0
            for elemento in (lista_usati):
                costo_attuale += elemento['Umidita']
            if costo_attuale < self.costo_minimo:
                self.costo_minimo = costo_attuale
                self.lista_percorsi.clear()
                self.lista_percorsi = [lista_usati]  # mantieni solo il miglior percorso
            return
        else:
            for i in range(len(lista_disponibili_rimanenti)):
                costo_attuale = 0
                for elemento in (lista_usati):
                    costo_attuale += elemento['Umidita']

                if costo_attuale >= self.costo_minimo:
                    return
                if len(lista_usati) == 0 or (lista_usati[-1]["Data"].day == (
                        lista_disponibili_rimanenti[i]["Data"].day - 1)):  # condizione che i giorni siano consecutivi
                    if (self.troppi_consecutivi(lista_usati, lista_disponibili_rimanenti[i]) == False):
                        if (self.almeno_tre_consecutivi(lista_usati, lista_disponibili_rimanenti[i]) == True):
                            nuovo_usati = lista_usati + [lista_disponibili_rimanenti[i]]
                            nuovi_rimanenti = lista_disponibili_rimanenti[:i] + lista_disponibili_rimanenti[i + 1:]
                            self._ricorsione(nuovo_usati, nuovi_rimanenti)

    def troppi_consecutivi(self, lista_usati, giorno_aggiunto):
        if len(lista_usati) < 5:
            return False
        elif (lista_usati[-1]["Localita"] ==
              lista_usati[-2]["Localita"] ==
              lista_usati[-3]["Localita"] ==
              lista_usati[-4]["Localita"] ==
              lista_usati[-5]["Localita"] ==
              giorno_aggiunto["Localita"]):
            return True
        return False

    def almeno_tre_consecutivi(self, lista_usati, giorno_aggiunto):
        if len(lista_usati) <= 1:  # se siamo all'inizio return True
            return True
        if lista_usati[-1]["Localita"] == giorno_aggiunto[
            "Localita"]:  # se la citta precedente è uguale a quella attuale
            return True

        conta_consecutivi = 1
        for i in range(len(lista_usati) - 2, -1, -1):
            if lista_usati[i]["Localita"] == lista_usati[-1]["Localita"]:
                conta_consecutivi += 1
            else:
                break

        if conta_consecutivi >= 3:
            return True
        else:
            return False


if __name__ == '__main__':
    model = Model()
    print(model.getUmiditaAvg(2))
    print(model.calcola_percorsi(2))