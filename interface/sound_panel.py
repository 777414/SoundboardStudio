import customtkinter as ctk


def create_sound_panel(window, sounds):
    panel = ctk.CTkFrame(
        window,
        fg_color="#202637",
        corner_radius=15
    )
    panel.grid(
        row=1,
        column=1,
        sticky="nsew",
        padx=24,
        pady=12
    )
    panel.grid_columnconfigure(0, weight=1)
    panel.grid_rowconfigure(0, weight=1)

    if len(sounds) == 0:
        empty = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        empty.place(relx=0.5, rely=0.5, anchor="center")

        icon = ctk.CTkLabel(
            empty,
            text="♫",
            font=("Arial", 64),
            text_color="#B6A9FF"
        )
        icon.pack(pady=(0, 10))

        title = ctk.CTkLabel(
            empty,
            text="Пока нет звуков",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(pady=5)

        description = ctk.CTkLabel(
            empty,
            text="Добавь первый звук в свою коллекцию!",
            font=("Arial", 14),
            text_color="#B6BED0"
        )
        description.pack(pady=5)

    return panel
