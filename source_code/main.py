from controller import main

if __name__ == "__main__":
    main()

"""


import pandas as pd
from scipy.io import wavfile
from pydub import AudioSegment
import numpy as np
from model import Model


def main():
    # Instantiate the Model
    model_instance = Model()

    # Load data
    model_instance.load_data(r"C:\\Users\\mat\\Desktop\\final_python_project\\clap_sound.m4a")


    # Clean data
    model_instance.clean_data()

    # Analyze data
    model_instance.analyze_data()

    model_instance.visualize_waveform()

    rt60_result = model_instance.calculate_rt60()
    print(f"RT60 for the provided data is {rt60_result} seconds.")


if __name__ == "__main__":
    main()
"""