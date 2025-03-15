import argparse
import numpy as np
from scipy.io.wavfile import write

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from beats.generator import generate_binaural_section
from beats.ambient_mixer import mix_with_ambient
from beats.utils import crossfade_tracks

# Example: python cli/main.py --duration 600 --fade 10 --ambient assets/ambient/rain.wav --output output/meditation.wav

def main():
    parser = argparse.ArgumentParser(description="Generate Binaural Beat Tracks.")
    parser.add_argument("--duration", type=int, default=600)
    parser.add_argument("--fade", type=int, default=10)
    parser.add_argument("--ambient", type=str, help="Path to ambient WAV file.")
    parser.add_argument("--output", type=str, default="output/generated_track.wav")
    args = parser.parse_args()

    sr = 44100
    base_freq = 440

    section1 = generate_binaural_section(args.duration // 2, base_freq, 40, 40, sr)
    section2 = generate_binaural_section(args.duration // 2, base_freq, 40, 8, sr, fade=True)

    final_track = crossfade_tracks(section1, section2, args.fade, sr)

    if args.ambient:
        final_track = mix_with_ambient(final_track, args.ambient, sr)

    normalized = np.int16(final_track / np.max(np.abs(final_track)) * 32767)
    write(args.output, sr, normalized)
    print(f"Track written to {args.output}")

if __name__ == "__main__":
    main()
