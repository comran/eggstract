from src.components.wave import Wave


def generate_envelope(wave: Wave, subsample_rate: int = 10) -> Wave:
    step = round(wave.sample_rate / subsample_rate)
    subsampled_signal = wave.signal[::step]

    return Wave(subsampled_signal, subsample_rate)
