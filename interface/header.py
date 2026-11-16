import customtkinter as ctk


def create_header(window):
    header = ctk.CTkFrame(window, fg_color="transparent")
    header.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 12))
    header.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(
        header,
        text="Soundboard Studio",
        font=("Arial", 26, "bold"),
        text_color="#FFFFFF"
    )
    title.grid(row=0, column=0, sticky="w")

    status = ctk.CTkLabel(
        header,
        text="● ГОТОВО",
        font=("Arial", 13, "bold"),
        text_color="#65C99A"
    )
    status.grid(row=0, column=1, sticky="e")
