import pandas as pd
from scipy.signal import welch
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self) :
        self.sound = None
        self.data = None
        self.db_data = None
        self.sample_rate = None

    def load_data(self, file_path) :
        valid_file = 0
        while not valid_file :
            # convert .mp3 to .wav
            if file_path.endswith('.mp3') :
                valid_file = 1
                self.sound = AudioSegment.from_mp3(file_path)
                self.sound.export('converted.wav', format="wav")
                self.sound = AudioSegment.from_wav('converted.wav')
            elif file_path.endswith('.wav') :
                valid_file = 1
                self.sound = AudioSegment.from_wav(file_path)
            else :
                print("Not a valid file format.")
        self.sample_rate = self.sound.frame_rate
        # handle mono/stereo
        channels = self.sound.channels
        if channels == 1 :
            raw_data = self.sound.get_array_of_samples()
            self.data = np.array(raw_data)
        else :
            # split stereo channels to two mono channels and use one
            stereo_channels = self.sound.split_to_mono()
            mono_sound = stereo_channels[0]
            raw_data = mono_sound.get_array_of_samples()
            self.data = np.array(raw_data)

        self.db_data = self.data.astype(float) / (1 << 15)
        self.db_data = 20 * np.log10(np.abs(self.db_data))

    def show_statistics(self):
        # Print summary statistics
        low, mid, high = self.calculate_rt60_for_frequency_ranges()
        return f'Summary Statistics:\nChannels: {self.sound.channels}\nBit Depth: {self.sound.sample_width * 8}\nLength (ms): {len(self.sound)}\ndominant_frequency is {round(self.calculate_resonance_frequency(self.data))} Hz\nRT60 for Low Frequencies: {low}\nRT60 for Mid Frequencies: {mid}\nRT60 for High Frequencies: {high}'

    def analyze_data(self):
        # Create self visualizations
        self.plot_histogram()
        self.plot_scatter()
        self.plot_sine_wave()
        # self.visualize_waveform()
        self.decibels()

        # Identify patterns or trends in RT60 values over three frequency ranges
        # self.identify_rt60_trends()

        # Display plots
        plt.show()

    def separate_frequency(self, freq_range) :
        frequencies = np.fft.fftfreq(len(self.data), 1 / self.sample_rate)
        freq_mask = (frequencies >= freq_range[0]) & (frequencies <= freq_range[-1])
        filtered_data = self.data * freq_mask
        return filtered_data

    def plot_histogram(self):
        plt.subplot(2, 2, 1)  # 2x2 grid, position 1
        plt.hist(self.data)
        plt.xlabel('Bins')
        plt.ylabel('Amplitude')
        plt.title('Histogram')

    def plot_scatter(self):
        plt.subplot(2, 2, 2)  # 2x2 grid, position 2
        x = np.arange(len(self.data))
        plt.scatter(x, self.data)
        plt.title('Scatter')
        plt.xlabel('Index')
        plt.ylabel('Amplitude')

    def plot_sine_wave(self):
        plt.subplot(2, 2, 3)  # 2x2 grid, position 3
        x_sine = np.linspace(0, 2 * np.pi, 1000)
        y_sine = np.sin(x_sine)
        plt.plot(x_sine, y_sine, label='Sine Wave')
        plt.title('Sine Wave')
        plt.xlabel('X-Axis')
        plt.ylabel('Y-axis')
        plt.legend()

    def visualize_waveform(self):
        plt.subplot(2, 2, 4) # 2x2 grid, position 4
        x = np.arange(len(self.data))
        plt.plot(x, self.data)
        plt.title('Waveform')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
    
    def decibels(self):
        plt.subplot(2,2,4)
        plt.plot(self.db_data)

    def calculate_resonance_frequency(self, data):
        frequencies, power = welch(data, self.sample_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        return dominant_frequency
    
    def calculate_rt60(self, data) :
        pass
    
    def calculate_rt60_for_range(self, freq_range) :
            filtered_data = self.separate_frequency(freq_range)
            rt60 = self.calculate_rt60(filtered_data)
            return rt60

    def calculate_rt60_for_frequency_ranges(self) :
        if self.data is not None :
            low_freq_range = (20, 200)
            mid_freq_range = (200, 2000)
            high_freq_range = (2000, 20000)

            rt60_low = self.calculate_rt60_for_range(low_freq_range)
            rt60_mid = self.calculate_rt60_for_range(mid_freq_range)
            rt60_high = self.calculate_rt60_for_range(high_freq_range)

        return rt60_low, rt60_mid, rt60_high

    def calculate_rt60_difference(self) :
        if self.data is not None :
            target_rt60 = 0.5
            

    # def identify_rt60_trends(self, rt60_values):
    #     # Maybe store rt60 values into some iterable and pass them through here

    #     # Boxplot of RT60 values
    #     plt.subplot(2, 2, 4)  # 2x2 grid, position 4
    #     rt60_values.plot(kind='box', title='Boxplot of RT60 Values')

    #     # Bar chart of RT60 values for each frequency range
    #     plt.subplot(2, 2, 4)  # 2x2 grid, position 4 (or choose a new position)
    #     self.plot_rt60_bar_chart()

    def plot_rt60_bar_chart(self):
        # Assuming self has columns 'LowFreq_RT60', 'MidFreq_RT60', 'HighFreq_RT60'
        rt60_freq_ranges = ['LowFreq_RT60', 'MidFreq_RT60', 'HighFreq_RT60']
        rt60_values = self.self[rt60_freq_ranges]
        rt60_values.plot(kind='bar', stacked=True, title='RT60 Values Over Three Frequency Ranges')



