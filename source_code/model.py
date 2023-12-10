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
            # here we try to read the file if it is .wav
            try:
                sample_rate, sample_data = wavfile.read(path_file)
            except ValueError:
                audio = AudioSegment.from_file(path_file)
                audio.export("converted.wav", format="wav")
                sample_rate, sample_data = wavfile.read("converted.wav")

        self.data = pd.DataFrame({'Channel 1': sample_data})

        if self.data is not None:
            print(self.data)
            print("this is channel 1")
            print(self.data['Channel 1'])
            print(self.data.info())
            print(self.data.columns)
            print(sample_data)
            print(self.data.head())
            print(self.data.shape)

    def clean_data(self):
        # Implement self cleaning tool
        self.data = self.data.dropna()

        if 'MetadataColumn' in self.data.columns:
            self.data = self.data.drop(columns=['MetadataColumn'])

    def analyze_data(self):
        # Generate summary statistics
        summary_stats = self.data.describe()

        # Print summary statistics
        print("Summary Statistics:")
        print(summary_stats)

        # Create self visualizations
        self.plot_histogram()
        self.plot_scatter()
        self.plot_sine_wave()

        # Identify patterns or trends in RT60 values over three frequency ranges
        self.identify_rt60_trends()

        # Adjust layout
        plt.tight_layout()

        # Display plots
        plt.show()

    def plot_histogram(self):
        plt.subplot(2, 2, 1)  # 2x2 grid, position 1
        self.data['Channel 1'].plot(kind='hist', title='Histogram of Channel 1')

    def plot_scatter(self):
        plt.subplot(2, 2, 2)  # 2x2 grid, position 2
        plt.scatter(self.data.index, self.data['Channel 1'])
        plt.title('Scatter Plot of Channel 1')
        plt.xlabel('Index')
        plt.ylabel('Channel 1')

    def plot_sine_wave(self):
        plt.subplot(2, 2, 3)  # 2x2 grid, position 3
        x_sine = np.linspace(0, 2 * np.pi, 1000)
        y_sine = np.sin(x_sine)
        plt.plot(x_sine, y_sine, label='Sine Wave')
        plt.title('Plot of a Sine Wave')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.legend()

    def identify_rt60_trends(self):
        pass

    def visualize_waveform(self):
        plt.plot(self.data.index, self.data['Channel 1'])
        plt.title('Waveform')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()


        # all the commented below was me trying to find the
        # RT60 but no luck

"""
    def calculate_rt60(self):

        data = self.data['Channel 1'].to_numpy()
        time = self.data.index.to_numpy()

        # Step 1: Find Maximum value of dB's in array
        max_db = np.max(data)

        # Step 2: Slice self and time arrays to location of maximum value
        max_index = np.argmax(data)
        data_slice = data[max_index:]
        time_slice = time[max_index:]

        # Step 3: Find value which is Max - 5dB
        threshold_5db = max_db - 5
        index_5db = np.argmax(data_slice <= threshold_5db)
        value_5db = data_slice[index_5db]
        time_5db = time_slice[index_5db]

        # Step 4: Find a value which is equal to max - 25dB
        threshold_25db = max_db - 25
        index_25db = np.argmax(data_slice <= threshold_25db)
        value_25db = data_slice[index_25db]
        time_25db = time_slice[index_25db]

        # Step 5: Calculate RT20 as time it takes amplitude to drop from max (less 5dB) to max (less 25dB)
        rt20 = time_25db - time_5db

        # Step 6: Multiply times by 3 to give RT60 reverb time
        rt60 = rt20 * 3

        return rt60

    def identify_rt60_trends(self):
        # Assume RT60 values are in a column named 'RT60'
        rt60_values = self.self['RT60']

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

    def analyze_data(self):
        # Implement self analysis methods
        summary_stats = self.self.describe()

        # Print summary statistics
        print("Summary Statistics:")
        print(summary_stats)

        # Create self visualizations (you can customize based on your requirements)
        # Example: Histogram
        #self.self['Channel 1'].plot(kind='hist', title='Histogram of Channel 1')

        # Example: Scatter Plot
        # self.self.plot.scatter(x='Channel 1', y='SomeOtherColumn', title='Scatter Plot')



        # Identify patterns or trends in the self
        # (This part depends on your specific analysis requirements)"""



