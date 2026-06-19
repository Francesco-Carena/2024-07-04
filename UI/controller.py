import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDCategory(self):
        categories=self._model.getCategories()
        for category in categories:
            self._view._ddcategory.options.append(ft.dropdown.Option(category))

    def handleCreaGrafo(self, e):
        category=self._view._ddcategory.value
        if category is None:
            self._view.create_alert("Seleziona una categoria")
            self._view.update_page()
            return
        startDate=self._view._dp1.value
        endDate=self._view._dp2.value
        if startDate is None or endDate is None:
            self._view.create_alert("Seleziona una data di partenza e fine")
            self._view.update_page()
            return
        if startDate > endDate:
            self._view.create_alert("L'inizio deve avvenire prima della fine")
            self._view.update_page()
            return

        self._model.createGraph(category, startDate, endDate)

        nodi, archi= self._model.getInfoGraph()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        self._view.txt_result.controls.append(ft.Text(f"Date selezionate: {startDate} : {endDate}"))
        self._view.txt_result.controls.append(ft.Text(f"Il numero di  nodi:{nodi}, numero archi: {archi}"))

        allNodi=self._model.getAllNodes()
        for n in allNodi:
            self._view._ddProdStart.options.append(ft.dropdown.Option(data=n, key=n.product_id, text=n.product_name))
            self._view._ddProdEnd.options.append(ft.dropdown.Option(data=n, key=n.product_id, text=n.product_name))


        self._view.update_page()

    def handleBestProdotti(self, e):
        if self._model._graph is None:
            self._view.create_alert("Creare prima il grafo")
            self._view.update_page()
            return
        prodotti=self._model.bestProducts()


        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
        for p in prodotti:
            self._view.txt_result.controls.append(ft.Text(f"{p[0]}: {p[1]}"))

        self._view.update_page()

    def handleCercaCammino(self, e):
        if self._model._graph is None:
            self._view.create_alert("Creare prima il grafo")
            self._view.update_page()
            return
        lunghezza=self._view._txtInLun.value
        if lunghezza is None:
            self._view.create_alert("Impostare lunghezza cammino")
            self._view.update_page()
            return
        source=self._view._ddProdStart.value
        dest=self._view._ddProdEnd.value
        if source is None or dest is None:
            self._view.create_alert("Selezionare partenza e arrivo")
            self._view.update_page()
            return

        cammino, costo=self._model.getCammino(source, dest, lunghezza)
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Cammino migliore trovato! Costo: {costo}"))
        for n in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))

        self._view.update_page()






    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)