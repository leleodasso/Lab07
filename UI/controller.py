import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        mese = self._view.dd_mese.value

        if mese is None or mese == "":
            self._view.create_alert("Inserire mese")
            return
        mese = int(mese)

        lista_temp = []
        for el in self._model.getUmiditaAvg(mese):
            lista_temp.append(el)

        self._view.lst_result.controls.append(ft.Text(f"L'umidità media del mese selezionato è:\n"
                                                      f"{lista_temp[0]["Localita"]}: {lista_temp[0]["avg(s.Umidita)"]}\n"
                                                      f"{lista_temp[1]["Localita"]}: {lista_temp[1]["avg(s.Umidita)"]}\n"
                                                      f"{lista_temp[2]["Localita"]}: {lista_temp[2]["avg(s.Umidita)"]}"))
        self._view.update_page()


    def handle_sequenza(self, e):
        mese = self._view.dd_mese.value

        if mese is None or mese == "":
            self._view.create_alert("Inserire mese")
            return

        mese = int(mese)
        self._model.calcola_percorsi(mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {self._model.costo_minimo} ed è:\n"))
        lista_temp = []
        for percorso in self._model.lista_percorsi:
            for el in percorso:
                print(f"{el}\n")
                riga = f"[{el["Localita"]} - {el["Data"]}] Umidità = {el["Umidita"]}"
                self._view.lst_result.controls.append(ft.Text(riga))


        self._view.update_page()
        pass

    def read_mese(self, e):
        self._mese = int(e.control.value)

