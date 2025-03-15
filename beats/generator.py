import numpy as np

def generate_binaural_section(duration, base_freq, start_beat, end_beat, sample_rate=44100, fade=True):
    samples = int(duration * sample_rate)
    t = np.linspace(0, duration, samples, endpoint=False)

    if fade:
        beat_freqs = np.linspace(start_beat, end_beat, samples)
    else:
        beat_freqs = np.full(samples, start_beat)

    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freqs) * t)

    return np.stack([left, right], axis=-1)
