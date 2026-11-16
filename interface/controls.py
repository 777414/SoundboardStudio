import customtkinter as ctk
from tkinter import messagebox


def create_controls(window, sounds):
    controls = ctk.CTkFrame(
        window,
        fg_color="transparent"
    )
    controls.grid(
        row=2,
        column=1,
        sticky="ew",
        padx=24,
        pady=(12, 22)
    )

    record_button = ctk.CTkButton(
        controls,
        text="🎙 Записать звук",
        height=44,
        fg_color="#5141A5",
        text_color="#FFFFFF",
        command=lambda: messagebox.showinfo(
            "Запись звука",
            "Запись будет доступна в следующем этапе."
        )
    )
    record_button.pack(side="left", padx=(0, 10))

    import_button = ctk.CTkButton(
        controls,
        text="＋ Добавить WAV",
        height=44,
        fg_color="#315D78",
        text_color="#FFFFFF",
        command=lambda: messagebox.showinfo(
            "Добавление звука",
            "Импорт WAV будет доступен в следующем этапе."
        )
    )
    import_button.pack(side="left")

    stop_button = ctk.CTkButton(
        controls,
        text="■ ОСТАНОВИТЬ ЗВУК",
        height=44,
        fg_color="#783A45",
        text_color="#FFFFFF",
        state="disabled"
    )
    stop_button.pack(side="right")
