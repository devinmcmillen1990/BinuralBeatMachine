import sys
import os
import argparse
import numpy as np
from scipy.io.wavfile import write

# Ensure parent directory is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import generators and utilities
from beats.generator import generate_monotone_section, generate_polytonal_section, generate_soothing_overlay_section
from beats.ambient_mixer import mix_with_ambient
from beats.utils import crossfade_tracks

def main():
    parser = argparse.ArgumentParser(description="Generate a binaural beats track with optional ambient background.")
    parser.add_argument("--duration", type=int, default=600, help="Total duration in seconds (default: 600)")
    parser.add_argument("--fade", type=int, default=10, help="Crossfade duration between sections (seconds)")
    parser.add_argument("--ambient", type=str, help="Path to ambient WAV file")
    parser.add_argument("--output", type=str, default="output/binural-beat.wav", help="Path to save final output WAV")
    parser.add_argument("--style", choices=["monotonal", "polytonal", "soothing-poly"], default="monotonal", help="Beat generation style (default: monotonal)")

    args = parser.parse_args()

    sample_rate = 44100
    base_freq = 440

    print(f"[INFO] Generating track: style={args.style}, duration={args.duration}s")

    # Generate the two sections
    if args.style == "monotonal":
        section1 = generate_monotone_section(args.duration // 2, base_freq, 40, 40, sample_rate)
        section2 = generate_monotone_section(args.duration // 2, base_freq, 40, 8, sample_rate, fade=True)
    elif args.style == "polytonal":
        section1 = generate_polytonal_section(args.duration // 2, base_freq, 40, 40, sample_rate)
        section2 = generate_polytonal_section(args.duration // 2, base_freq, 40, 8, sample_rate)
    elif args.style == "soothing-poly":
        section1 = generate_soothing_overlay_section(
            duration_sec=args.duration,
            base_freq=base_freq,
            sample_rate=sample_rate
        )
        section2 = None

    if section2 is not None:
        print(f"[INFO] Crossfading sections...")
        final_track = crossfade_tracks(section1, section2, args.fade, sample_rate)
    else:
        final_track = section1


    if args.ambient:
        print(f"[INFO] Mixing in ambient track: {args.ambient}")
        final_track = mix_with_ambient(final_track, args.ambient, sample_rate)

    # Normalize and save
    print(f"[INFO] Saving to {args.output}")
    normalized = np.int16(final_track / np.max(np.abs(final_track)) * 32767)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    write(args.output, sample_rate, normalized)

    print("[DONE] Binaural beat track created successfully.")

if __name__ == "__main__":
    main()
