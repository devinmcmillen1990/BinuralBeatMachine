import numpy as np

# Single tone frequency
def generate_monotone_section(duration, base_freq, start_beat, end_beat, sample_rate=44100, fade=True):
    samples = int(duration * sample_rate)
    t = np.linspace(0, duration, samples, endpoint=False)

    if fade:
        beat_freqs = np.linspace(start_beat, end_beat, samples)
    else:
        beat_freqs = np.full(samples, start_beat)

    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + beat_freqs) * t)

    return np.stack([left, right], axis=-1)

# Polytonal frequency
def generate_polytonal_section(duration, base_freq, start_beat, end_beat, sample_rate=44100):
    samples = int(duration * sample_rate)
    t = np.linspace(0, duration, samples, endpoint=False)

    # Base beat frequency sweep
    beat_freqs = np.linspace(start_beat, end_beat, samples)

    # Add layered slow modulation for polytonal effect
    mod1 = 1.5 * np.sin(2 * np.pi * 0.05 * t)  # slow wave
    mod2 = 1.0 * np.sin(2 * np.pi * 0.07 * t)  # mid wave
    mod3 = 0.7 * np.sin(2 * np.pi * 0.03 * t)  # deep wave

    dynamic_beat_freqs = beat_freqs + mod1 + mod2 + mod3

    left = np.sin(2 * np.pi * base_freq * t)
    right = np.sin(2 * np.pi * (base_freq + dynamic_beat_freqs) * t)

    return np.stack([left, right], axis=-1)
