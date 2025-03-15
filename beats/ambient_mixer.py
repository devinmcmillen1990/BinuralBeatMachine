import numpy as np
from scipy.io import wavfile

def mix_with_ambient(binaural_track, ambient_path, sample_rate=44100, ambient_volume=0.3):
    ambient_rate, ambient_data = wavfile.read(ambient_path)

    if ambient_rate != sample_rate:
        raise ValueError("Ambient file sample rate must match binaural track.")

    if ambient_data.ndim == 1:
        ambient_data = np.stack([ambient_data, ambient_data], axis=-1)

    # Normalize ambient
    ambient_data = ambient_data / np.max(np.abs(ambient_data)) * ambient_volume

    # Repeat ambient if it's too short
    if ambient_data.shape[0] < binaural_track.shape[0]:
        repeat_times = int(np.ceil(binaural_track.shape[0] / ambient_data.shape[0]))
        ambient_data = np.tile(ambient_data, (repeat_times, 1))

    # Match exact length
    ambient_data = ambient_data[:binaural_track.shape[0]]

    # Mix both tracks
    mixed = binaural_track + ambient_data
    return np.clip(mixed, -1.0, 1.0)
