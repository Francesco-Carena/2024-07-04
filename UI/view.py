import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Esame del 10/07/2025 - Turno A"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 600
        self._page.window_width = 1000
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Esame del 10/07/2025 - Turno A", color="green", size=24)
        self._page.controls.append(self._title)

        self._ddyears = ft.Dropdown(label="Anni", width=200, on_change=self._controller.fillDDShapes)
        self._controller.fillDDYears()
        self._ddshapes = ft.Dropdown(label="Forme", width=200)


        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._btnPath = ft.ElevatedButton(text="Cerca percorso", on_click=self._controller.handlePath)


        row1 = ft.Row([self._ddyears, self._ddshapes, self._btnCreaGrafo, self._btnPath],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        """row2 = ft.Row([self._txtInLun, self._ddProdStart, self._ddProdEnd, self._btnCercaCammino],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)"""

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
