import tkinter as tk
from tkinter import filedialog
from model import Model


class App:
    def __init__(self, master):
        self.master = master
        master.title("Data Analysis App")

        self.model_instance = Model()

        # Load File Button
        self.load_file_button = tk.Button(master, text="Load File", command=self.load_file)
        self.load_file_button.pack()
        self.load_label = tk.Label(master, text='')
        self.load_label.pack()

        # Show Statistics Button
        self.show_statistics_button = tk.Button(master, text="Show Statistics", command=self.show_statistics)
        self.show_statistics_button.pack()
        self.stats_label = tk.Label(master, text='')
        self.stats_label.pack()

        # Show Plots Button
        self.show_plots_button = tk.Button(master, text="Show Plots", command=self.show_plots)
        self.show_plots_button.pack()


    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
        if file_path:
            self.model_instance.load_data(file_path)
            self.load_label.config(text='File loaded successfully!')

    def show_statistics(self):
        if self.model_instance.data is not None:
            self.stats_label.config(text=self.model_instance.show_statistics())
        else:
            self.stats_label.config(text='Please load a file first.')

    def show_plots(self):
        if self.model_instance.data is not None:
            self.model_instance.analyze_data()
        else:
            print('Please load a file first.')


