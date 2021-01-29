from typing import List

import ffmpeg
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np


def get_mp3_metadata(file_location: str):
    metadata = {}

    metadata["duration"] = ffmpeg.probe(file_location)["format"]["duration"]


def display_wave(file_location: str):
    x, sr = librosa.load(file_location, sr=44100)
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(x, sr=sr)
    plt.show()


def display_spectrum(file_location: str):
    x, sr = librosa.load(file_location, sr=44100)
    X = librosa.stft(x)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sr, x_axis="time", y_axis="hz")
    plt.colorbar()
    plt.show()


def find_largest_frequencies(wave: np.ndarray) -> List[float]:
    # Get number of samples in the wave based on its shape.
    number_of_samples = wave.shape[0]

    # Convert from time domain to frequency domain using a fast fourier transform.
    fft = np.fft.fft(wave)

    # Extract amplitudes and frequencies from the fft results.
    amplitudes = 1 / number_of_samples * np.abs(fft)
    frequencies = np.fft.fftfreq(number_of_samples) * number_of_samples * 1 / (1 - 0)

    # Get one side of the frequency/amplitude ranges.
    frequencies = frequencies[: len(frequencies) // 2]
    amplitudes = amplitudes[: len(fft) // 2]

    # Stack the result, and sort by frequency.
    frequency_domain = np.column_stack((frequencies, amplitudes))
    frequency_domain = frequency_domain[((-frequency_domain[:, 1]).argsort())]

    # Return largest frequencies.
    return frequency_domain[:, 0]
