import customtkinter as ctk
from tkinter import messagebox
from pathlib import Path
import sounddevice as sd
import soundfile as sf

from storage import save_sounds
from interface.sound_panel import refresh_sound_panel


TEMP_FILE = Path("sounds/recording_preview.wav")
SOUNDS_FOLDER = Path("sounds/custom")


def start_recording(state):
    if state["recording"]:
        return

    sd.stop()
    state["playing_id"] = None

    try:
        TEMP_FILE.parent.mkdir(parents=True, exist_ok=True)

        sample_rate = 44100
        state["recording_data"] = sd.rec(
            int(5 * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32"
        )
        state["recording"] = True
        messagebox.showinfo(
            "Запись звука",
            "Запись началась. Запиши звук сейчас — она остановится через 5 секунд."
        )
        state["window"].after(5100, lambda: finish_recording(state))
    except Exception as error:
        state["recording"] = False
        messagebox.showerror(
            "Ошибка микрофона",
            f"Не удалось начать запись. Проверь подключение микрофона.\n\n{error}"
        )


def finish_recording(state):
    try:
        sd.wait()
        sf.write(TEMP_FILE, state["recording_data"], 44100)
        state["recording"] = False
        show_preview(state)
    except Exception as error:
        state["recording"] = False
        messagebox.showerror("Ошибка записи", str(error))


def show_preview(state):
    preview = ctk.CTkToplevel(state["window"])
    preview.title("Прослушивание записи")
    preview.geometry("380x300")
    preview.resizable(False, False)
    preview.transient(state["window"])
    preview.grab_set()

    ctk.CTkLabel(
        preview,
        text="Запись готова!",
        font=("Arial", 22, "bold"),
        text_color="#FFFFFF"
    ).pack(pady=(25, 8))

    ctk.CTkLabel(
        preview,
        text="Прослушай звук. Если нужно, запиши ещё раз.",
        text_color="#B6BED0"
    ).pack(pady=5)

    def play_preview():
        try:
            data, sample_rate = sf.read(TEMP_FILE, dtype="float32")
            sd.stop()
            sd.play(data, sample_rate)
        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось воспроизвести запись.\n{error}")

    def record_again():
        sd.stop()
        preview.destroy()
        start_recording(state)

    def save_recording():
        dialog = ctk.CTkInputDialog(
            text="Введи название звука:",
            title="Сохранение звука"
        )
        name = dialog.get_input()

        if name is None:
            return

        name = name.strip()
        if not name:
            messagebox.showwarning("Название", "Название не может быть пустым.")
            return

        SOUNDS_FOLDER.mkdir(parents=True, exist_ok=True)
        sound_id = max(
            [sound["id"] for sound in state["sounds"]],
            default=0
        ) + 1
        destination = SOUNDS_FOLDER / f"sound_{sound_id}.wav"

        try:
            TEMP_FILE.replace(destination)
            state["sounds"].append({
                "id": sound_id,
                "name": name,
                "file": str(destination).replace("\\", "/")
            })
            save_sounds(state["sounds"])
            preview.destroy()
            refresh_sound_panel(state)
        except OSError as error:
            messagebox.showerror("Ошибка сохранения", str(error))

    def cancel_preview():
        sd.stop()
        preview.destroy()
        if TEMP_FILE.exists():
            TEMP_FILE.unlink()

    ctk.CTkButton(
        preview,
        text="▶ Прослушать",
        command=play_preview,
        fg_color="#5141A5",
        text_color="#FFFFFF"
    ).pack(fill="x", padx=35, pady=(20, 6))

    ctk.CTkButton(
        preview,
        text="Записать ещё раз",
        command=record_again,
        fg_color="#315D78",
        text_color="#FFFFFF"
    ).pack(fill="x", padx=35, pady=6)

    ctk.CTkButton(
        preview,
        text="Сохранить звук",
        command=save_recording,
        fg_color="#287A59",
        text_color="#FFFFFF"
    ).pack(fill="x", padx=35, pady=6)

    ctk.CTkButton(
        preview,
        text="Отмена",
        command=cancel_preview,
        fg_color="#783A45",
        text_color="#FFFFFF"
    ).pack(fill="x", padx=35, pady=(6, 18))

    preview.protocol("WM_DELETE_WINDOW", cancel_preview)
