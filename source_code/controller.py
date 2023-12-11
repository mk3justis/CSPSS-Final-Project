from view import App
from model import Model
import tkinter as tk


def main():
    root = tk.Tk()
    root.geometry("400x200")
    root.minsize(400, 200)
    model_instance = Model()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
