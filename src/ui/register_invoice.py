import flet as ft
from src.lib.invoices import register_invoice, retry_failed
from src.utils.handle_bd import (
    get_list_import_rolls,
    get_uuid_client_by_nit,
)

def register_invoice_view(connection_db, conn_factory):
    rolls_cache = {r["uuid"]: r for r in get_list_import_rolls(connection_db)}
    barcode_list: list[str] = []
    barcode_input: ft.TextField | None = None
    barcode_error_text: ft.Text | None = None
    barcode_list_column: ft.Column | None = None
    barcode_modal: ft.AlertDialog | None = None
    barcode_total_text: ft.Text | None = None

    def update_barcode_list(page: ft.Page):
        barcode_list_column.controls.clear()
        barcode_total_text.value = f"Códigos agregados ({len(barcode_list)}):"
        for code in barcode_list:
            roll = rolls_cache.get(code)
            info_roll = f"{roll['roll']} | {roll['color']}" if roll else "No encontrado"
            barcode_list_column.controls.append(
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(info_roll, expand=True),
                        ft.IconButton(
                            icon="delete",
                            icon_color="red",
                            tooltip="Eliminar",
                            on_click=lambda e, c=code: remove_barcode(c, page),
                        ),
                    ],
                )
            )
        page.update()

    def remove_barcode(code: str, page: ft.Page):
        if code in barcode_list:
            barcode_list.remove(code)
            update_barcode_list(page)

    def on_submit_barcode_input(e):
        code = barcode_input.value.strip()
        if code == "":
            return

        if code in barcode_list:
            barcode_error_text.value = "⚠️ Rollo ya agregado"
            barcode_error_text.visible = True
        else:
            roll = rolls_cache.get(code)
            if roll is None:
                barcode_error_text.value = "⚠️ Rollo no encontrado"
                barcode_error_text.visible = True
            elif roll["checked"]:
                barcode_error_text.value = "⚠️ Rollo no disponible"
                barcode_error_text.visible = True
            else:
                barcode_list.append(code)
                barcode_error_text.visible = False

        barcode_input.value = ""
        barcode_input.focus()
        update_barcode_list(e.page)
        e.page.update()

    def open_barcode_modal(e):
        nit = nit_input.value.strip()
        if nit == "":
            nit_error_text.visible = True
            e.page.update()
            return
        nit = str(nit)

        uuid_client = get_uuid_client_by_nit(
            nit_client_search=nit, connection_db=connection_db
        )
        if not uuid_client:
            nit_error_text.value = "Nit no registrado"
            nit_error_text.visible = True
            e.page.update()
            return

        nit_error_text.visible = False
        barcode_input.value = ""
        barcode_list.clear()
        barcode_list_column.controls.clear()
        barcode_error_text.visible = False
        barcode_total_text.value = "Códigos agregados (0):"
        barcode_modal.open = True
        e.page.update()

    def cancel_invoice(e):
        barcode_modal.open = False
        barcode_list.clear()
        barcode_list_column.controls.clear()
        barcode_total_text.value = "Códigos agregados (0):"
        e.page.update()

    def register_inv(e):
        barcode_modal.open = False
        nit = nit_input.value.strip()
        register_invoice(
            barcode_list=barcode_list,
            client_nit=nit,
            connection_db=connection_db,
            conn_factory=conn_factory,
        )
        barcode_list.clear()
        barcode_list_column.controls.clear()
        barcode_total_text.value = "Códigos agregados (0):"
        e.page.update()

    def retry_invoices(e):
        retry_failed(connection_db, conn_factory=conn_factory)
        e.page.snack_bar = ft.SnackBar(ft.Text("Se reintentó registrar facturas pendientes"))
        e.page.snack_bar.open = True
        e.page.update()

    # input y lista para modal
    barcode_input = ft.TextField(
        hint_text="Escanee código de barras...",
        autofocus=True,
        on_submit=on_submit_barcode_input,
    )
    barcode_error_text = ft.Text(value="", color="red", visible=False)
    barcode_list_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
    barcode_total_text = ft.Text("Códigos agregados (0):", weight="bold")

    barcode_modal = ft.AlertDialog(
        modal=True,
        content=ft.Container(
            width=400,
            height=350,
            padding=10,
            content=ft.Column(
                controls=[barcode_input, barcode_error_text, barcode_total_text, barcode_list_column],
                expand=True,
            ),
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cancel_invoice),
            ft.TextButton("Registrar", on_click=register_inv),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    barcode_modal.open = False

    nit_input = ft.TextField(label="NIT Cliente", expand=True, color="black")
    nit_error_text = ft.Text(
        value="⚠️ Debe ingresar un NIT antes de facturar",
        color="red",
        visible=False,
    )

    return ft.Column(
        controls=[
            ft.Text("Registrar Factura", size=20, weight=ft.FontWeight.BOLD, color="black"),
            ft.Column(
                controls=[
                    nit_input,
                    nit_error_text,
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(
                                "Facturar", bgcolor="green", color="white", on_click=open_barcode_modal
                            ),
                            ft.ElevatedButton(
                                "Reintentar pendientes",
                                bgcolor="orange",
                                color="white",
                                on_click=retry_invoices,
                            ),
                        ],
                        spacing=10,
                    ),
                ],
                spacing=10,
                width=400,
            ),
            barcode_modal,
        ]
    )
