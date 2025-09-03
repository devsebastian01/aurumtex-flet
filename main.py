import flet as ft
from src.lib.db.db_connection import connection_db
from src.ui.login import login_view
from src.ui.layout import main_layout


def main(page: ft.Page):
    page.title = "Aplicativo Aurumtex S.A.S"
    page.window_width = 1000
    page.window_height = 700
    page.window_resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # función para crear nuevas conexiones
    conn_factory = connection_db

    # primera conexión activa
    connection = conn_factory()

    def on_login_success():
        page.clean()
        main_layout(page, connection, conn_factory)

    login_view(page, on_login_success, connection)


ft.app(target=main)
