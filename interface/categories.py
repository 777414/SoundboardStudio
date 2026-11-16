import customtkinter as ctk


CATEGORIES = [
    "Все звуки",
    "Эффекты",
    "Голоса",
    "Сигналы",
    "Разное"
]


def create_categories(window):
    sidebar = ctk.CTkFrame(
        window,
        width=190,
        corner_radius=0,
        fg_color="#1B2030"
    )
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)

    title = ctk.CTkLabel(
        sidebar,
        text="КАТЕГОРИИ",
        font=("Arial", 12, "bold"),
        text_color="#B6BED0"
    )
    title.pack(anchor="w", padx=18, pady=(36, 16))

    buttons = []

    for category in CATEGORIES:
        button = ctk.CTkButton(
            sidebar,
            text=category,
            height=42,
            anchor="w",
            corner_radius=8,
            fg_color="#5141A5" if category == "Все звуки" else "transparent",
            hover_color="#34304F",
            text_color="#FFFFFF"
        )
        button.pack(fill="x", padx=12, pady=4)
        buttons.append(button)

    return buttons
