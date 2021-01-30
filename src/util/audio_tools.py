from typing import List

import ffmpeg
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import soundfile

from src.util.constants import DEFAULT_SAMPLE_RATE


def get_mp3_metadata(file_location: str):
    metadata = {}

    metadata["duration"] = ffmpeg.probe(file_location)["format"]["duration"]


def load_wave_from_file(file_location: str, sample_rate: int = DEFAULT_SAMPLE_RATE):
    wave, _ = librosa.load(file_location, sr=sample_rate)

    return wave


def write_wave_to_file(
    file_location: str, wave: np.ndarray, sample_rate: int = DEFAULT_SAMPLE_RATE
):

    soundfile.write(file_location, wave, sample_rate, "PCM_24")


def display_wave(wave: np.ndarray, sample_rate: int = DEFAULT_SAMPLE_RATE):
    plt.figure(figsize=(14, 5))
    librosa.display.waveplot(wave, sr=sample_rate)
    plt.show()


def display_spectrum(wave: np.ndarray, sample_rate: int = DEFAULT_SAMPLE_RATE):
    X = librosa.stft(wave)
    Xdb = librosa.amplitude_to_db(abs(X))
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr=sample_rate, x_axis="time", y_axis="hz")

    plt.colorbar()
    plt.show()


def find_largest_frequencies(wave: np.ndarray, sample_rate: int) -> List[float]:
    # Get number of samples in the wave based on its shape.
    number_of_samples = len(wave)
    duration = 1.0 * number_of_samples / sample_rate

    # Convert from time domain to frequency domain using a fast fourier transform.
    fft = np.fft.fft(wave)

    # Extract amplitudes and frequencies from the fft results.
    amplitudes = 1 / number_of_samples * np.abs(fft)
    frequencies = np.fft.fftfreq(number_of_samples) * number_of_samples / (duration)

    # Get one side of the frequency/amplitude ranges.
    frequencies = frequencies[: len(frequencies) // 2]
    amplitudes = amplitudes[: len(fft) // 2]

    # Stack the result, and sort by frequency.
    frequency_domain = np.column_stack((frequencies, amplitudes))
    frequency_domain = frequency_domain[((-frequency_domain[:, 1]).argsort())]

    # Return largest frequencies.
    return frequency_domain[:, 0]
