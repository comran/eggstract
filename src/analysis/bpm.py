import librosa

from src.dsp.wave import Wave


def find_bpm(wave: Wave) -> float:
    estimated_bpm = librosa.beat.tempo(wave.signal, wave.sample_rate)[0]

    return float(estimated_bpm)
