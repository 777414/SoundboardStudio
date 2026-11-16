import customtkinter as ctk
from tkinter import messagebox, simpledialog
from pathlib import Path
import sounddevice as sd
import soundfile as sf

from storage import save_sounds


def create_sound_panel(state):
    panel = ctk.CTkScrollableFrame(
        state["window"],
        fg_color="#202637",
        corner_radius=15
    )
    panel.grid(row=1, column=0, sticky="nsew", padx=24, pady=12)
    panel.grid_columnconfigure((0, 1, 2), weight=1)
    state["panel"] = panel
    refresh_sound_panel(state)


def play_sound(state, sound):
    try:
        sd.stop()
        file_path = Path(sound["file"])
        data, sample_rate = sf.read(file_path, dtype="float32")
        sd.play(data, sample_rate)
        state["playing_id"] = sound["id"]
        state["window"].after(100, lambda: check_playback(state))
    except Exception as error:
        state["playing_id"] = None
        messagebox.showerror("Ошибка воспроизведения", f"Не удалось воспроизвести звук.\n\n{error}")


def check_playback(state):
    if state["playing_id"] is None:
        return

    try:
        stream = sd.get_stream()
        if stream is not None and stream.active:
            state["window"].after(100, lambda: check_playback(state))
        else:
            state["playing_id"] = None
    except Exception:
        state["playing_id"] = None


def stop_sound(state):
    sd.stop()
    state["playing_id"] = None


def edit_sound(state, sound):
    new_name = simpledialog.askstring(
        "Переименовать звук",
        "Введите новое название:",
        initialvalue=sound["name"],
        parent=state["window"]
    )

    if new_name is None:
        return

    new_name = new_name.strip()
    if not new_name:
        messagebox.showwarning("Название", "Название не может быть пустым.")
        return

    sound["name"] = new_name
    save_sounds(state["sounds"])
    refresh_sound_panel(state)


def delete_sound(state, sound):
    answer = messagebox.askyesno(
        "Удалить звук",
        f"Удалить звук «{sound['name']}»?"
    )
    if not answer:
        return

    if state["playing_id"] == sound["id"]:
        stop_sound(state)

    try:
        Path(sound["file"]).unlink(missing_ok=True)
    except OSError:
        pass

    state["sounds"].remove(sound)
    save_sounds(state["sounds"])
    refresh_sound_panel(state)


def refresh_sound_panel(state):
    panel = state["panel"]

    for widget in panel.winfo_children():
        widget.destroy()

    if not state["sounds"]:
        empty = ctk.CTkFrame(panel, fg_color="transparent")
        empty.grid(row=0, column=0, columnspan=3, pady=100)

        ctk.CTkLabel(
            empty,
            text="♫",
            font=("Arial", 64),
            text_color="#B6A9FF"
        ).pack(pady=8)

        ctk.CTkLabel(
            empty,
            text="Пока нет звуков",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=5)

        ctk.CTkLabel(
            empty,
            text="Запиши звук или добавь WAV-файл",
            font=("Arial", 14),
            text_color="#B6BED0"
        ).pack(pady=5)
        return

    sorted_sounds = sorted(
        state["sounds"],
        key=lambda item: item["id"],
        reverse=True
    )

    for index, sound in enumerate(sorted_sounds):
        card = ctk.CTkFrame(
            panel,
            fg_color="#30384A",
            corner_radius=12
        )
        card.grid(
            row=index // 3,
            column=index % 3,
            sticky="nsew",
            padx=8,
            pady=8
        )

        play_button = ctk.CTkButton(
            card,
            text="▶  " + sound["name"],
            height=58,
            font=("Arial", 15, "bold"),
            fg_color="#5141A5",
            hover_color="#6554BD",
            text_color="#FFFFFF",
            command=lambda item=sound: play_sound(state, item)
        )
        play_button.pack(fill="x", padx=10, pady=(10, 6))

        edit_button = ctk.CTkButton(
            card,
            text="Переименовать",
            height=30,
            fg_color="#39465C",
            text_color="#FFFFFF",
            command=lambda item=sound: edit_sound(state, item)
        )
        edit_button.pack(fill="x", padx=10, pady=3)

        delete_button = ctk.CTkButton(
            card,
            text="Удалить",
            height=30,
            fg_color="#783A45",
            text_color="#FFFFFF",
            command=lambda item=sound: delete_sound(state, item)
        )
        delete_button.pack(fill="x", padx=10, pady=(3, 10))
