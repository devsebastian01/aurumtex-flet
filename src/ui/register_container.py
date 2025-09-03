from src.lib.container import register_container
from src.utils.read_excel import read_excel_by_headers
from src.utils.normalize import normalize_headers
import flet as ft

uploaded_files = []

def register_container_view(connection_db):
    uploaded_files_view = ft.ListView(
        expand=False,
        height=200,
        spacing=10,
        padding=10,
        auto_scroll=False,
    )

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            for f in e.files:
                uploaded_files.append(f)  # 👈 Guardamos el archivo seleccionado

                file_item = ft.Row(
                    controls=[
                        ft.Icon(name="insert_drive_file", color="blue"),
                        ft.Text(f.name, color="black"),
                        ft.IconButton(
                            icon="delete",
                            icon_color="red",
                            tooltip="Eliminar",
                            on_click=lambda ev, item=f: remove_file(item),
                        ),
                    ]
                )
                uploaded_files_view.controls.append(file_item)
            uploaded_files_view.update()

    def remove_file(file_obj):
        global uploaded_files
        uploaded_files = [f for f in uploaded_files if f.name != file_obj.name]
        uploaded_files_view.controls = [
            row for row in uploaded_files_view.controls
            if not any(isinstance(ctrl, ft.Text) and ctrl.value == file_obj.name for ctrl in row.controls)
        ]
        uploaded_files_view.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)

    upload_btn = ft.ElevatedButton(
        "Cargar archivo (.xlsx, .xls)",
        icon="upload_file",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=True,
            allowed_extensions=["xlsx", "xls"],
        ),
    )

    def register_files(e: ft.ControlEvent):
        global uploaded_files

        if not uploaded_files:
            e.page.snack_bar = ft.SnackBar(
                ft.Text("No hay archivos para registrar"),
                bgcolor="red"
            )
            e.page.snack_bar.open = True
            e.page.update()
            return

        # Obtener rutas completas de los archivos
        document_files = [f.path for f in uploaded_files]
        headers_model = normalize_headers(["ITEM", "COLOR", "ROLL NO", "MTS", "KG", "CODIGO SIIGO"])

        list_dict_excels = read_excel_by_headers(
            headers_model=headers_model,
            document_files=document_files
        )
        register_container(list_dict_excels= list_dict_excels,
                           connection_db = connection_db)
        

        # Limpiar archivos cargados
        uploaded_files.clear()
        uploaded_files_view.controls.clear()
        uploaded_files_view.update()

        # Mostrar mensaje de éxito
        # !!!
        #

    register_btn = ft.ElevatedButton(
        "Registrar",
        bgcolor="green",
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        icon="check",
        on_click=register_files
    )

    return ft.Column(
        controls=[
            file_picker,
            ft.Text("Subir lista de contenedor", size=20, weight="bold", color="black"),
            upload_btn,
            uploaded_files_view,
            ft.Divider(),
            register_btn,
        ]
    )
