import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path
import shutil
import soundfile as sf

from storage import save_sounds
from interface.sound_panel import refresh_sound_panel, stop_sound
from recorder import start_recording


SOUNDS_FOLDER = Path("sounds/custom")


def next_sound_id(sounds):
    if not sounds:
        return 1
    return max(sound["id"] for sound in sounds) + 1


def import_sound(state):
    file_path = filedialog.askopenfilename(
        title="Выбери WAV-файл",
        filetypes=[("WAV-файлы", "*.wav")]
    )

    if not file_path:
        return

    try:
        sf.info(file_path)
    except Exception:
        messagebox.showerror("Ошибка файла", "Не удалось открыть этот WAV-файл.")
        return

    name = simpledialog.askstring(
        "Название звука",
        "Как назовём звук?",
        parent=state["window"]
    )
    if name is None:
        return

    name = name.strip()
    if not name:
        messagebox.showwarning("Название", "Введи название звука.")
        return

    SOUNDS_FOLDER.mkdir(parents=True, exist_ok=True)
    sound_id = next_sound_id(state["sounds"])
    destination = SOUNDS_FOLDER / f"sound_{sound_id}.wav"

    try:
        shutil.copy2(file_path, destination)
        state["sounds"].append({
            "id": sound_id,
            "name": name,
            "file": str(destination).replace("\\", "/")
        })
        save_sounds(state["sounds"])
        refresh_sound_panel(state)
    except OSError as error:
        messagebox.showerror("Ошибка импорта", str(error))


def create_controls(state):
    controls = ctk.CTkFrame(state["window"], fg_color="transparent")
    controls.grid(row=2, column=0, sticky="ew", padx=24, pady=(12, 22))

    record_button = ctk.CTkButton(
        controls,
        text="🎙 Записать звук",
        height=46,
        fg_color="#5141A5",
        text_color="#FFFFFF",
        command=lambda: start_recording(state)
    )
    record_button.pack(side="left", padx=(0, 10))

    import_button = ctk.CTkButton(
        controls,
        text="＋ Добавить WAV",
        height=46,
        fg_color="#315D78",
        text_color="#FFFFFF",
        command=lambda: import_sound(state)
    )
    import_button.pack(side="left")

    stop_button = ctk.CTkButton(
        controls,
        text="■ ОСТАНОВИТЬ ЗВУК",
        height=46,
        fg_color="#783A45",
        text_color="#FFFFFF",
        command=lambda: stop_sound(state)
    )
    stop_button.pack(side="right")
