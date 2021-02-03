import librosa
import soundfile

from src.dsp.wave import Wave
from src.util.constants import DEFAULT_SAMPLE_RATE


def load_from_file(file_location: str, sample_rate: int = DEFAULT_SAMPLE_RATE) -> Wave:
    wave_array, _ = librosa.load(file_location, sr=sample_rate)
    wave = Wave(wave_array, sample_rate)

    return wave


def write_to_file(wave: Wave, file_location: str):
    soundfile.write(file_location, wave.signal, wave.sample_rate, "PCM_24")
