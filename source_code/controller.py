from view import App
from model import Model
import tkinter as tk


def main():
    root = tk.Tk()
    model_instance = Model()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
