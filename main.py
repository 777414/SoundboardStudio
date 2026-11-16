import customtkinter as ctk

from interface.window import create_window
from interface.header import create_header
from interface.sound_panel import create_sound_panel
from interface.controls import create_controls
from storage import load_sounds


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

sounds = load_sounds()

window = create_window()

state = {
    "window": window,
    "sounds": sounds,
    "panel": None,
    "playing_id": None,
    "recording": False
}

create_header(window)
create_sound_panel(state)
create_controls(state)

window.mainloop()
