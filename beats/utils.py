import numpy as np

def crossfade_tracks(track1, track2, fade_duration_sec, sample_rate=44100):
    fade_samples = int(fade_duration_sec * sample_rate)

    fade_out = np.linspace(1, 0, fade_samples)
    fade_in = np.linspace(0, 1, fade_samples)

    track1[-fade_samples:, 0] *= fade_out
    track1[-fade_samples:, 1] *= fade_out
    track2[:fade_samples, 0] *= fade_in
    track2[:fade_samples, 1] *= fade_in

    return np.concatenate((track1, track2), axis=0)
