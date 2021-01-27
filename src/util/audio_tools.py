import ffmpeg
import librosa
import librosa.display
import matplotlib.pyplot as plt

def get_mp3_metadata(file_location: str):
    metadata = {}

    metadata['duration'] = ffmpeg.probe(file_location)['format']['duration']

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
    librosa.display.specshow(Xdb, sr=sr, x_axis='time', y_axis='hz')
    plt.colorbar()
    plt.show()
