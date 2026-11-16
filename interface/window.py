import customtkinter as ctk


def create_window():
    window = ctk.CTk()
    window.title("Soundboard Studio")
    window.geometry("1050x700")
    window.minsize(800, 550)
    window.configure(fg_color="#171B27")

    window.grid_columnconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)

    return window
