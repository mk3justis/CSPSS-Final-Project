import pandas as pd
from scipy.signal import welch
from pydub import AudioSegment
import numpy as np
import matplotlib.pyplot as plt


class Model:
    def __init__(self) :
        self.sound = None
        self.data = None
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
        
    def clean_data(self, sound):
        # Implement self cleaning tool
        sound = sound._spawn(b'')


    def show_statistics(self):
        # Print summary statistics
        return f'Summary Statistics:\nChannels: {self.sound.channels}\nBit Depth: {self.sound.sample_width * 8}\nLength (ms): {len(self.sound)}\ndominant_frequency is {round(self.calculate_rt60())} Hz'

    def analyze_data(self):
        # Create self visualizations
        self.plot_histogram()
        self.plot_scatter()
        # self.plot_sine_wave()
        self.visualize_waveform()

        # Identify patterns or trends in RT60 values over three frequency ranges
        self.identify_rt60_trends()

        # Adjust layout
        plt.tight_layout()

        # Display plots
        plt.show()

    def plot_histogram(self):
        plt.subplot(2, 2, 1)  # 2x2 grid, position 1
        plt.hist(self.data)
        plt.xlabel('Bins')
        plt.ylabel('Amplitude')
        plt.title('Histogram of File Data')

    def plot_scatter(self):
        plt.subplot(2, 2, 2)  # 2x2 grid, position 2
        x = np.arange(len(self.data))
        plt.scatter(x, self.data)
        plt.title('Scatter Plot of File Data')
        plt.xlabel('Index')
        plt.ylabel('Amplitude')

    def plot_sine_wave(self):
        plt.subplot(2, 2, 3)  # 2x2 grid, position 3
        x_sine = np.linspace(0, 2 * np.pi, 1000)
        y_sine = np.sin(x_sine)
        plt.plot(x_sine, y_sine, label='Sine Wave')
        plt.title('Plot of a Sine Wave')
        plt.xlabel('X-Axis')
        plt.ylabel('Y-axis')
        plt.legend()

    def visualize_waveform(self):
        x = np.arange(len(self.data))
        plt.plot(x, self.data)
        plt.title('Waveform')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()

    def calculate_rt60(self):
        frequencies, power = welch(self.data, self.sample_rate, nperseg=4096)
        dominant_frequency = frequencies[np.argmax(power)]
        return dominant_frequency


    def identify_rt60_trends(self, rt60_values):
        # Maybe store rt60 values into some iterable and pass them through here

        # Boxplot of RT60 values
        plt.subplot(2, 2, 4)  # 2x2 grid, position 4
        rt60_values.plot(kind='box', title='Boxplot of RT60 Values')

        # Bar chart of RT60 values for each frequency range
        plt.subplot(2, 2, 4)  # 2x2 grid, position 4 (or choose a new position)
        self.plot_rt60_bar_chart()

    def plot_rt60_bar_chart(self):
        # Assuming self has columns 'LowFreq_RT60', 'MidFreq_RT60', 'HighFreq_RT60'
        rt60_freq_ranges = ['LowFreq_RT60', 'MidFreq_RT60', 'HighFreq_RT60']
        rt60_values = self.self[rt60_freq_ranges]
        rt60_values.plot(kind='bar', stacked=True, title='RT60 Values Over Three Frequency Ranges')

    # def analyze_data(self):
    #     # Implement self analysis methods
    #     summary_stats = self.self.describe()

    #     # Print summary statistics
    #     print("Summary Statistics:")
    #     print(summary_stats)


        # Create self visualizations (you can customize based on your requirements)
        # Example: Histogram
        #self.self['Channel 1'].plot(kind='hist', title='Histogram of Channel 1')

        # Example: Scatter Plot
        # self.self.plot.scatter(x='Channel 1', y='SomeOtherColumn', title='Scatter Plot')



        # Identify patterns or trends in the self
        # (This part depends on your specific analysis requirements)



