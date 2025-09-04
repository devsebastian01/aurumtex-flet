import flet as ft
from src.lib.db.repositories.roll_repository import get_list_import_rolls

def import_inventory_view(connection_db):
    
    all_inventory_data = []
    inventory_data = []

    # Variables globales para el modal
    edit_modal = None
    item_input = None
    roll_input = None
    color_input = None
    siigo_code_input = None
    mts_input = None
    kg_input = None
    container_input = None
    current_record = None

    # 🔹 Contenedor dinámico que primero muestra "Cargando..."
    content_area = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    loading_indicator = ft.Column(
        controls=[
            ft.ProgressRing(),
            ft.Text("Cargando datos...", size=16, color="black"),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    content_area.controls.append(loading_indicator)

    # 🔹 Filtros
    filters = {
        "uuid": ft.TextField(label="UUID", width=100, on_change=lambda e: apply_filters(e.page), color="black"),
        "item": ft.TextField(label="Item", width=120, on_change=lambda e: apply_filters(e.page), color="black"),
        "roll": ft.TextField(label="Roll", width=80, on_change=lambda e: apply_filters(e.page), color="black"),
        "color": ft.TextField(label="Color", width=120, on_change=lambda e: apply_filters(e.page), color="black"),
        "siigo_code": ft.TextField(label="Siigo Code", width=120, on_change=lambda e: apply_filters(e.page), color="black"),
        "mts": ft.TextField(label="Mts", width=80, on_change=lambda e: apply_filters(e.page), color="black"),
        "kg": ft.TextField(label="Kg", width=80, on_change=lambda e: apply_filters(e.page), color="black"),
        "container": ft.TextField(label="Container", width=120, on_change=lambda e: apply_filters(e.page), color="black"),
        "checked": ft.TextField(label="Estado", width=100, on_change=lambda e: apply_filters(e.page), color="black"),
    }

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("UUID", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Item", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Roll", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Color", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Siigo Code", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Mts", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Kg", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Container", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Estado", color="black", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Acciones", color="black", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
    )

    def render_table(page: ft.Page):
        table.rows.clear()
        for record in inventory_data:
            checked = "Facturado" if record["checked"] else "Sin facturar"
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(record["uuid"], color="black")),
                        ft.DataCell(ft.Text(record["item"], color="black")),
                        ft.DataCell(ft.Text(str(record["roll"]), color="black")),
                        ft.DataCell(ft.Text(record["color"], color="black")),
                        ft.DataCell(ft.Text(record["siigo_code"], color="black")),
                        ft.DataCell(ft.Text(str(record["mts"]), color="black")),
                        ft.DataCell(ft.Text(str(record["kg"]), color="black")),
                        ft.DataCell(ft.Text(record["container"], color="black")),
                        ft.DataCell(ft.Text(str(checked), color="black")),
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon="delete",
                                        icon_color="red",
                                        tooltip="Eliminar",
                                        on_click=lambda e, uuid=record["uuid"]: delete_roll(e, uuid),
                                    ),
                                    ft.IconButton(
                                        icon="edit",
                                        icon_color="blue",
                                        tooltip="Editar",
                                        on_click=lambda e, rec=record: open_edit_modal(e, rec),
                                    ),
                                    
                                ]
                            )
                        ),
                    ]
                )
            )
        page.update()

    def apply_filters(page: ft.Page):
        nonlocal inventory_data
        inventory_data = []
        for rec in all_inventory_data:
            match = True
            for key, field in filters.items():
                if field.value and str(rec.get(key, "")).lower().find(field.value.lower()) == -1:
                    match = False
                    break
            if match:
                inventory_data.append(rec)
        render_table(page)

    def delete_roll(e, uuid: str):
        nonlocal all_inventory_data, inventory_data
        all_inventory_data = [r for r in all_inventory_data if r["uuid"] != uuid]
        inventory_data = [r for r in inventory_data if r["uuid"] != uuid]
        render_table(e.page)
        e.page.snack_bar = ft.SnackBar(ft.Text(f"Registro {uuid} eliminado"))
        e.page.snack_bar.open = True
        e.page.update()

    def open_edit_modal(e, record):
        nonlocal current_record
        current_record = record
        item_input.value = record["item"]
        roll_input.value = str(record["roll"])
        color_input.value = record["color"]
        siigo_code_input.value = record["siigo_code"]
        mts_input.value = str(record["mts"])
        kg_input.value = str(record["kg"])
        container_input.value = record["container"]
        edit_modal.open = True
        e.page.update()

    def cancel_edit(e):
        edit_modal.open = False
        e.page.update()

    def confirm_update(e):
        nonlocal inventory_data, current_record
        for i, item in enumerate(inventory_data):
            if item["uuid"] == current_record["uuid"]:
                inventory_data[i].update({
                    "item": item_input.value,
                    "roll": int(roll_input.value) if roll_input.value.isdigit() else current_record["roll"],
                    "color": color_input.value,
                    "siigo_code": siigo_code_input.value,
                    "mts": float(mts_input.value) if mts_input.value.replace('.', '').isdigit() else current_record["mts"],
                    "kg": float(kg_input.value) if kg_input.value.replace('.', '').isdigit() else current_record["kg"],
                    "container": container_input.value,
                })
                break
        render_table(e.page)
        e.page.snack_bar = ft.SnackBar(ft.Text(f"Registro {current_record['uuid']} actualizado"))
        e.page.snack_bar.open = True
        edit_modal.open = False
        e.page.update()

    # Inputs modal
    item_input = ft.TextField(label="Item", color="black")
    roll_input = ft.TextField(label="Roll", color="black")
    color_input = ft.TextField(label="Color", color="black")
    siigo_code_input = ft.TextField(label="Siigo Code", color="black")
    mts_input = ft.TextField(label="Mts", color="black")
    kg_input = ft.TextField(label="Kg", color="black")
    container_input = ft.TextField(label="Container", color="black")

    # Modal
    edit_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar registro", color="black"),
        bgcolor="white",
        content=ft.Container(
            width=400,
            height=400,
            padding=10,
            content=ft.Column(
                controls=[
                    item_input,
                    roll_input,
                    color_input,
                    siigo_code_input,
                    mts_input,
                    kg_input,
                    container_input,
                ],
                scroll=ft.ScrollMode.AUTO,
            ),
        ),
        actions=[
            ft.TextButton("Cancelar", on_click=cancel_edit),
            ft.TextButton("Actualizar", on_click=confirm_update),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    edit_modal.open = False

    # 🔹 Carga de datos
    async def load_data():
        
        nonlocal all_inventory_data, inventory_data
        all_inventory_data = get_list_import_rolls(connection_db = connection_db)
        inventory_data = all_inventory_data.copy()

        content_area.controls.clear()
        content_area.controls.append(
            ft.Container(
                content=ft.ListView(
                    controls=[table],
                    expand=True,
                ),
                expand=True,
                border=ft.border.all(1, "black"),
                border_radius=10,
                padding=10,
                height=450,
            )
        )
        render_table(layout.page)
        layout.page.update()

    layout = ft.Column(
        controls=[
            ft.Text("Inventario Contenedores", size=22, weight=ft.FontWeight.BOLD, color="black"),
            ft.Container(
                content=ft.Row(controls=list(filters.values()), scroll=ft.ScrollMode.AUTO),
                padding=10,
            ),
            content_area,
            edit_modal
        ],
        expand=True
    )

    def did_mount():
        layout.page.run_task(load_data)

    layout.did_mount = did_mount
    return layout
