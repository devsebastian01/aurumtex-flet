import flet as ft
from src.ui.register_container import register_container_view
from src.ui.register_invoice import register_invoice_view
from src.ui.import_inventory import import_inventory_view
from src.ui.consult_invoice import consult_invoice_view

def main_layout(page: ft.Page, connection_db, conn_factory):
    content = ft.Container(
        expand=True,
        bgcolor="white",
        border_radius=15,  # bordes redondeados del área de contenido
        padding=20,
    )

    def menu_click(e):
        opt = e.control.data
        if opt == "inventory_national":
            content.content = import_inventory_view(connection_db)
        elif opt == "inventory_imported":
            content.content = import_inventory_view(connection_db)
        elif opt == "register_container":
            content.content = register_container_view(connection_db)
        elif opt == "register_invoice":
            # pasamos conn_factory para reintentos
            content.content = register_invoice_view(connection_db, conn_factory)
        elif opt == "consult_invoices":
            content.content = consult_invoice_view()
        elif opt == "logout":
            page.clean()
            from src.ui.login import login_view
            login_view(page, lambda: main_layout(page, connection_db, conn_factory))
            return 
        page.update()

    # Menú principal
    menu_items = ft.Column(
        [
            ft.Text("Aurumtex S.A.S", size=20, weight=ft.FontWeight.BOLD, color="white"),
            ft.Divider(color="white54"),
            #ft.TextButton("Inventario Nacional", data="inventory_national", on_click=menu_click, style=ft.ButtonStyle(color="white")),
            ft.TextButton("Registrar Contenedor", data="register_container", on_click=menu_click, style=ft.ButtonStyle(color="white")),
            ft.TextButton("Registrar Factura", data="register_invoice", on_click=menu_click, style=ft.ButtonStyle(color="white")),
            ft.TextButton("Inventario Contenedores", data="inventory_imported", on_click=menu_click, style=ft.ButtonStyle(color="white")),
            #ft.TextButton("Consultar Facturas", data="consult_invoices", on_click=menu_click, style=ft.ButtonStyle(color="white")),
        ],
        spacing=10,
    )

    # Botón cerrar sesión
    logout_btn = ft.TextButton(
        "Cerrar sesión",
        icon="logout",
        data="logout",
        on_click=menu_click,
        style=ft.ButtonStyle(color="white"),
    )

    # Sidebar con bordes redondeados
    sidebar = ft.Container(
        content=ft.Column(
            [
                menu_items,
                logout_btn,
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        width=250,
        bgcolor="#1e3a8a",
        padding=15,
        border_radius=15,  # bordes redondeados del sidebar
    )

    # Layout principal
    page.clean()
    page.add(
        ft.Container(
            content=ft.Row(
                [
                    sidebar,
                    content,
                ],
                expand=True,
            ),
            expand=True,
            padding=10,   # espacio para que se noten los bordes
            bgcolor="#f0f2f5",  # fondo gris claro detrás del layout
        )
    )
