import customtkinter
from bot import Bot

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("Dark")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("green")


class GUI(customtkinter.CTk):
    bot = Bot()

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Senjin Clip Generator")
        self.geometry(f"{1100}x{580}")
