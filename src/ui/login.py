import flet as ft
from src.lib.auth import authenticate


def login_view(page: ft.Page, on_success, connection):
    # Campos de texto con íconos
    user = ft.TextField(
        hint_text="Username",
        prefix_icon="person",
        width=300,
        border_radius=30,
        bgcolor="#FFFFFF",
        color="#000000",
    )
    password = ft.TextField(
        hint_text="Password",
        password=True,
        can_reveal_password=True,
        prefix_icon="lock",
        width=300,
        border_radius=30,
        bgcolor="#FFFFFF",
        color="#000000",
    )


    msg = ft.Text(value="", color="red")

    def login(e):
        if authenticate(user.value, password.value):
            on_success()
        else:
            msg.value = "Credenciales incorrectas"
            page.update()

    # Botón con gradiente
    login_btn = ft.Container(
        content=ft.Text("LOG IN", color="white", weight=ft.FontWeight.BOLD, size=16),
        alignment=ft.alignment.center,
        width=300,
        height=45,
        border_radius=30,
        on_click=login,
        bgcolor= "blue"
    )

    # Links
    forgot = ft.TextButton("Olvide la contraseña", style=ft.ButtonStyle(color="black"))
    
    # Caja central
    login_box = ft.Container(
        content=ft.Column(
            [
                ft.Text("Login", size=28, weight=ft.FontWeight.BOLD, color="black"),
                user,
                password,
                login_btn,
                forgot,
                msg,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        width=400,
        height=400,
        padding=30,
        border_radius=20,
        bgcolor="white",
    )

    # Fondo azul
    page.add(
        ft.Container(
            bgcolor="#9E9E9E",
            content=ft.Row(
                
                [login_box],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        )
    )
