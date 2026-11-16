import customtkinter as ctk

from interface.window import create_window
from interface.header import create_header
from interface.categories import create_categories
from interface.sound_panel import create_sound_panel
from interface.controls import create_controls
from storage import load_sounds


# Настройки внешнего вида
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Загружаем звуки и создаём главное окно
sounds = load_sounds()

window = create_window()

# Создаём части интерфейса
create_header(window)
create_categories(window)
create_sound_panel(window, sounds)
create_controls(window, sounds)

# Запускаем приложение
window.mainloop()
