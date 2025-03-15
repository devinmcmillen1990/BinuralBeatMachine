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

def generate_soothing_overlay_section(duration_sec, sample_rate=44100, pulse_count=200, base_freq=432, spread_range=12):
    total_samples = int(duration_sec * sample_rate)
    track = np.zeros((total_samples, 2))

    for _ in range(pulse_count):
        pulse_dur = np.random.uniform(1.5, 4.0)  # Longer, smoother pulses
        pulse_samples = int(pulse_dur * sample_rate)
        start = np.random.randint(0, total_samples - pulse_samples)

        # Choose gentle musical interval base tones
        base_choices = [174, 210, 285, 396, 432, 528, 639]
        base_freq = np.random.choice(base_choices)

        # Subtle binaural offset
        beat_freq = np.random.uniform(4.0, 8.0)
        left_freq = base_freq
        right_freq = base_freq + beat_freq

        t = np.linspace(0, pulse_dur, pulse_samples, endpoint=False)

        fade_len = pulse_samples // 6
        fade = np.linspace(0, 1, fade_len)
        envelope = np.concatenate([fade, np.ones(pulse_samples - 2*fade_len), fade[::-1]])

        left = envelope * np.sin(2 * np.pi * left_freq * t)
        right = envelope * np.sin(2 * np.pi * right_freq * t)

        track[start:start + pulse_samples, 0] += left
        track[start:start + pulse_samples, 1] += right

    # Normalize gently
    track = track / np.max(np.abs(track)) * 0.5
    return track

def generate_ambient_background_layer(
    duration_sec,
    sample_rate=44100,
    tone_count=30,
    base_tones=[174, 285, 396, 432, 528, 639],
    amplitude=0.3,
    phase_spread=0.3
):
    total_samples = int(duration_sec * sample_rate)
    track = np.zeros((total_samples, 2))

    for _ in range(tone_count):
        tone_dur = np.random.uniform(10.0, 30.0)  # Long ambient tones
        fade_dur = tone_dur * 0.3
        tone_samples = int(tone_dur * sample_rate)
        fade_samples = int(fade_dur * sample_rate)
        start = np.random.randint(0, total_samples - tone_samples)

        freq = np.random.choice(base_tones)
        t = np.linspace(0, tone_dur, tone_samples, endpoint=False)

        fade = np.linspace(0, 1, fade_samples)
        sustain = np.ones(tone_samples - 2 * fade_samples)
        envelope = np.concatenate([fade, sustain, fade[::-1]])

        left = envelope * np.sin(2 * np.pi * freq * t)
        right = envelope * np.sin(2 * np.pi * freq * t + phase_spread)

        track[start:start + tone_samples, 0] += left
        track[start:start + tone_samples, 1] += right

    track = track / np.max(np.abs(track)) * amplitude
    return track

