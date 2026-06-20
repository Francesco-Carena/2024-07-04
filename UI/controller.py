import datetime

import flet as ft



class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYears(self):
        anni=self._model.getAllYears()
        for anno in anni:
            self._view._ddyears.options.append(ft.dropdown.Option(anno))

    def fillDDShapes(self,e):
        self._view._ddshapes.options.clear()
        anno=int(self._view._ddyears.value)
        shapes=self._model.getShapes(anno)
        for shape in shapes:
            self._view._ddshapes.options.append(ft.dropdown.Option(shape))
        self._view.update_page()


    def handleCreaGrafo(self, e):
        anno=int(self._view._ddyears.value)
        if anno is None:
            self._view.create_alert("Selezionare un anno prima di creare il grafo")
            self._view.update_page()
            return

        forma=self._view._ddshapes.value
        if forma is None:
            self._view.create_alert("Selezionare una forma prima di creare il grafo")
            self._view.update_page()
            return

        self._model.createGraph(anno, forma)

        self._view.txt_result.clean()
        nnodi, narchi=self._model.getGraphDetails()
        numero_componenti, componente_maggiore= self._model.getDettagliComponenti()
        self._view.txt_result.controls.append(ft.Text("Grafo creato correttamente!"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nnodi} nodi e {narchi} archi"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {numero_componenti} componenti debolmente connesse"))
        self._view.txt_result.controls.append(ft.Text(f"la componente connessa maggiore ha {len(componente_maggiore)} nodi"))
        for node in componente_maggiore:
            self._view.txt_result.controls.append(ft.Text(node))

        self._view.update_page()


    def handlePath(self, e):
        anno=int(self._view._ddyears.value)
        if anno is None:
            self._view.create_alert("Selezionare un anno prima di creare il grafo")
            self._view.update_page()
            return

        forma=self._view._ddshapes.value
        if forma is None:
            self._view.create_alert("Selezionare una forma prima di creare il grafo")
            self._view.update_page()
            return

        punteggio, percorso= self._model.searchPath()

        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"Percorso migliore trovato!"))
        self._view.txt_result.controls.append(ft.Text(f"Il percorso migliore ha punteggio pari a {punteggio} ed è composto dai nodi:"))
        for node in percorso:
            self._view.txt_result.controls.append(ft.Text(node))

        self._view.update_page()