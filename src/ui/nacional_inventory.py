import flet as ft


def nacional_inventory_view():
    return ft.Column([
    ft.Text("Consultar Inventario", size=20, weight=ft.FontWeight.BOLD),
    ft.ElevatedButton("Actualizar")
    ])