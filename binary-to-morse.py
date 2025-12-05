import time
import math
import sys
import os

# Try to import audio module
try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: pyaudio not installed. Install with: pip install pyaudio")
    print("Audio will be simulated.\n")


SAMPLE_RATE = 44100
FREQUENCY = 800

DOT_DURATION = 0.005     # 5 ms
DASH_DURATION = 0.015    # 15 ms
GAP_DURATION = 0.002     # 2 ms

pa = None
stream = None
DOT_BUF = None
DASH_BUF = None
GAP_BUF = None


def generate_tone_buffer(duration):
    """Generate a 16-bit PCM sine wave buffer."""
    samples = int(SAMPLE_RATE * duration)
    return b"".join(
        int(math.sin(2 * math.pi * FREQUENCY * i / SAMPLE_RATE) * 32767)
        .to_bytes(2, "little", signed=True)
        for i in range(samples)
    )


def init_audio():
    """Initialize PyAudio and generate buffers once."""
    global pa, stream, DOT_BUF, DASH_BUF, GAP_BUF

    if not AUDIO_AVAILABLE:
        return

    if pa is None:
        pa = pyaudio.PyAudio()

    if stream is None:
        stream = pa.open(format=pyaudio.paInt16,
                         channels=1,
                         rate=SAMPLE_RATE,
                         output=True)

    # Pre-generate all tone buffers once
    if DOT_BUF is None:
        DOT_BUF = generate_tone_buffer(DOT_DURATION)
        DASH_BUF = generate_tone_buffer(DASH_DURATION)
        GAP_BUF = generate_tone_buffer(GAP_DURATION)


def close_audio():
    """Clean up audio stream."""
    global pa, stream
    if stream:
        stream.stop_stream()
        stream.close()
        stream = None
    if pa:
        pa.terminate()
        pa = None


def play_dot():
    if AUDIO_AVAILABLE:
        stream.write(DOT_BUF)
    else:
        print(".", end="")
        time.sleep(DOT_DURATION)


def play_dash():
    if AUDIO_AVAILABLE:
        stream.write(DASH_BUF)
    else:
        print("-", end="")
        time.sleep(DASH_DURATION)


def gap():
    if AUDIO_AVAILABLE:
        stream.write(GAP_BUF)
    else:
        time.sleep(GAP_DURATION)

def read_binary(filepath, max_bytes=5000):
    with open(filepath, 'rb') as f:
        data = f.read(max_bytes)
    return ''.join(format(b, '08b') for b in data), len(data)


def binary_to_morse(binary):
    return ["." if bit == "0" else "-" for bit in binary]

def play_morse(symbols, max_symbols=None):
    init_audio()

    if max_symbols:
        symbols = symbols[:max_symbols]

    print(f"\nPlaying {len(symbols)} symbols...\n")

    for s in symbols:
        if s == ".":
            play_dot()
        else:
            play_dash()
        gap()

    close_audio()
    print("\nDone.\n")

def main():
    print("=" * 60)
    print("FAST Binary → Morse Player")
    print("=" * 60)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("\nEnter path to file:\n> ").strip().strip('"')

    if not os.path.exists(filepath):
        print("File not found.")
        sys.exit(1)

    print("\nReading file...")
    binary_str, read_bytes = read_binary(filepath)
    print(f"Read {read_bytes} bytes ({len(binary_str)} bits)")

    print(f"\nFirst 64 bits: {binary_str[:64]}...\n")

    # Convert to fast Morse symbol list
    morse_symbols = binary_to_morse(binary_str)

    max_symbols = 20000
    print(f"Ready to play first {max_symbols} symbols (~{max_symbols/8:.1f} bytes)")

    if input("\nPress Enter to play or 'q' to cancel: ").strip().lower() != "q":
        play_morse(morse_symbols, max_symbols)
    else:
        print("Canceled.")


if __name__ == "__main__":
    main()
