import pandas as pd
from scipy.io import wavfile
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self):
        self.data = None

    def load_data(self, path_file):
        if path_file.endswith('.WAV'):
            sample_rate, sample_data = wavfile.read(path_file)
        else:
            try:
                sample_rate, sample_data = wavfile.read(path_file)
            except ValueError:
                audio = AudioSegment.from_file(path_file)
                audio.export("converted.wav", format="wav")
                sample_rate, sample_data = wavfile.read("converted.wav")

        self.data = pd.DataFrame({'Channel 1': sample_data})

    def clean_data(self):
        self.data = self.data.dropna()

    def analyze_data(self):
        summary_stats = self.data.describe()

        self.plot_histogram()
        self.plot_scatter()
        self.plot_sine_wave()
        self.compute_highest_resonance()
        self.compute_rt60_for_frequency_ranges()
        self.calculate_rt60_difference()

        plt.tight_layout()
        plt.show()

    def plot_histogram(self):
        plt.subplot(2, 2, 1)
        self.data['Channel 1'].plot(kind='hist', title='Histogram of Channel 1')

    def plot_scatter(self):
        plt.subplot(2, 2, 2)
        plt.scatter(self.data.index, self.data['Channel 1'])
        plt.title('Scatter Plot of Channel 1')
        plt.xlabel('Index')
        plt.ylabel('Channel 1')

    def plot_sine_wave(self):
        plt.subplot(2, 2, 3)
        x_sine = np.linspace(0, 2 * np.pi, 1000)
        y_sine = np.sin(x_sine)
        plt.plot(x_sine, y_sine, label='Sine Wave')
        plt.title('Plot of a Sine Wave')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.legend()

    def calculate_rt60(self):
        data = self.data['Channel 1'].to_numpy()
        time = self.data.index.to_numpy()

        max_db = np.max(data)
        max_index = np.argmax(data)
        data_slice = data[max_index:]
        time_slice = time[max_index:]

        threshold_5db = max_db - 5
        index_5db = np.argmax(data_slice <= threshold_5db)
        value_5db = data_slice[index_5db]
        time_5db = time_slice[index_5db]

        threshold_25db = max_db - 25
        index_25db = np.argmax(data_slice <= threshold_25db)
        value_25db = data_slice[index_25db]
        time_25db = time_slice[index_25db]

        rt20 = time_25db - time_5db
        rt60 = rt20 * 3

        print("RT60:", rt60)

    def visualize_waveform(self):
        plt.plot(self.data.index, self.data['Channel 1'])
        plt.title('Waveform')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

    def compute_highest_resonance(self):
        if self.data is not None:
            data = self.data['Channel 1'].to_numpy()
            sample_rate = 1 / (self.data.index[1] - self.data.index[0])
            fft_result = np.fft.fft(data)
            frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
            magnitude = np.abs(fft_result)
            peak_freq_index = np.argmax(magnitude)
            highest_resonance_freq = frequencies[peak_freq_index]
            print("Highest Resonance Frequency:", highest_resonance_freq, "Hz")

    def compute_rt60_for_frequency_ranges(self):
        if self.data is not None:
            data = self.data['Channel 1'].to_numpy()
            sample_rate = 1 / (self.data.index[1] - self.data.index[0])
            frequencies = np.fft.fftfreq(len(data), 1 / sample_rate)

            low_freq_range = (20, 200)
            mid_freq_range = (200, 2000)
            high_freq_range = (2000, 20000)

            rt60_low = self.compute_rt60_for_range(data, frequencies, low_freq_range)
            rt60_mid = self.compute_rt60_for_range(data, frequencies, mid_freq_range)
            rt60_high = self.compute_rt60_for_range(data, frequencies, high_freq_range)

            print("RT60 for Low Frequencies:", rt60_low, "s")
            print("RT60 for Mid Frequencies:", rt60_mid, "s")
            print("RT60 for High Frequencies:", rt60_high, "s")

    def compute_rt60_for_range(self, data, frequencies, freq_range):
        freq_mask = (frequencies >= freq_range[0]) & (frequencies <= freq_range[1])
        filtered_data = data * freq_mask
        self.data['Channel 1'] = filtered_data  # Update data to the filtered range
        self.calculate_rt60()  # Recalculate RT60 for the filtered range
        return self.data['Channel 1']

    def calculate_rt60_difference(self):
        if self.data is not None:
            target_rt60 = 0.5
            self.calculate_rt60()  # Recalculate RT60 based on the current data
            original_rt60 = self.data['Channel 1'].to_numpy()
            rt60_difference = original_rt60 - target_rt60
            print("RT60 Difference (Original - Target):", rt60_difference, "s")
        else:
            print("No data loaded.")


if __name__ == "__main__":
    model = Model()
    model.load_data("your_audio_file.wav")
    model.clean_data()
    model.analyze_data()
