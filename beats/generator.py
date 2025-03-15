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

def generate_soothing_overlay_section(duration_sec, sample_rate=44100, pulse_count=120, base_freq=440, spread_range=15):
    total_samples = int(duration_sec * sample_rate)
    track = np.zeros((total_samples, 2))  # Start with silence

    for _ in range(pulse_count):
        # Random pulse duration (0.2 to 2.5 sec)
        pulse_dur = np.random.uniform(0.2, 2.5)
        pulse_samples = int(pulse_dur * sample_rate)

        # Random start time
        start = np.random.randint(0, total_samples - pulse_samples)

        # Random modulation around base frequency
        left_freq = base_freq + np.random.uniform(-spread_range, spread_range)
        right_freq = base_freq + np.random.uniform(-spread_range, spread_range)

        t = np.linspace(0, pulse_dur, pulse_samples, endpoint=False)
        fade = np.linspace(0, 1, pulse_samples // 10)
        envelope = np.concatenate([fade, np.ones(pulse_samples - 2*len(fade)), fade[::-1]]) if len(fade)*2 < pulse_samples else np.ones(pulse_samples)

        left = envelope * np.sin(2 * np.pi * left_freq * t)
        right = envelope * np.sin(2 * np.pi * right_freq * t)

        # Mix into track
        track[start:start + pulse_samples, 0] += left
        track[start:start + pulse_samples, 1] += right

    # Normalize
    track = track / np.max(np.abs(track)) * 0.6  # Keep it soft
    return track