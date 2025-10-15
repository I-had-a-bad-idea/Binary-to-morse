import time
import math
import sys
import os

# Try to import audio library
try:
    import pyaudio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    print("Warning: pyaudio not installed. Install with: pip install pyaudio")
    print("Audio playback will be simulated with text output.\n")

# Generate a sine wave tone as a list of 16-bit audio samples
def generate_tone(frequency = 800, duration = 0.1, sample_rate = 44100):
    if not AUDIO_AVAILABLE:
        return None # Cant play it anyway (doesnt have pyaudio)
    
    samples = int(sample_rate * duration)
    wave = []
    for i in range(samples):
        value = math.sin(2 * math.pi * frequency * i / sample_rate)
        wave.append(int(value * 32767))  # 16-bit audio
    return wave

# Play a tone or simulate with text
def play_tone(duration=0.1):
    if AUDIO_AVAILABLE:
        try:
            # intitialize pyaudio
            p = pyaudio.PyAudio()
            stream = p.open(format = pyaudio.paInt16, channels = 1, rate = 44100, output = True)
            
            # Generate tone samples and convert to bytes
            tone = generate_tone(duration=duration)
            tone_bytes = b''.join(int(sample).to_bytes(2, byteorder = 'little', signed = True) for sample in tone)
            
            # Play the sound
            stream.write(tone_bytes)
            
            # Cleanup
            stream.stop_stream()
            stream.close()
            p.terminate()
        except Exception as e:
            print(f"Audio error: {e}")
    else:
        # Fallback: print visual symbol and wait tone duration
        print("•" if duration < 0.2 else "—")
        time.sleep(duration)

# Reads up to max_bytes from a binary file and gives binary string
def read_exe_as_binary(filepath, max_bytes = 100):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, 'rb') as f:
        data = f.read(max_bytes)  # Read first max_bytes bytes
    
    # Convert each byte to an 8-bit binary string
    binary_string = ''.join(format(byte, '08b') for byte in data)
    return binary_string, len(data)

# Convert a binary string to Morse (. and -)
def binary_to_morse(binary_string):
    morse = ''
    for bit in binary_string:
        if bit == '0':
            morse += '. '
        elif bit == '1':
            morse += '- '
    return morse.strip()

# Play Morse code audio or simulate with symbols
def play_morse(morse_code, max_symbols=None):
    dot_duration = 0.08   # 80ms for a dot 
    dash_duration = 0.24  # 240ms for a dash
    symbol_gap = 0.05     # 50ms between symbols
    
    # Limit number of symbols to play
    if max_symbols:
        symbols = morse_code.split()[:max_symbols]
        morse_code = ' '.join(symbols)
    
    print(f"\nPlaying Morse code ({len(morse_code.replace(' ', ''))} symbols)...\n")
    
    symbol_count = 0
    for symbol in morse_code:
        if symbol == '.':
            print('.', end='')
            play_tone(dot_duration)
            time.sleep(symbol_gap)
            symbol_count += 1
        elif symbol == '-':
            print('-', end='')
            play_tone(dash_duration)
            time.sleep(symbol_gap)
            symbol_count += 1
        elif symbol == ' ':
            if symbol_count % 8 == 0: # print every 8 symbols (every byte)
                print(' ', end='')
    
    print("\n")

# Entry point
def main():
    print("=" * 60)
    print("EXE/Binary File to Morse Code Player")
    print("=" * 60)
    print("\nConverts binary executable to Morse: 0 = dot, 1 = dash")
    
    # Get file path from argument or prompt user
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        print("\nEnter path to .exe or binary file:")
        filepath = input("> ").strip().strip('"')
    
    try:
        # Read file
        max_bytes = 50  # Limit to first 50 bytes (400 bits)
        print(f"\nReading first {max_bytes} bytes of file...")
        binary_string, bytes_read = read_exe_as_binary(filepath, max_bytes)
        
        print(f"Read {bytes_read} bytes ({len(binary_string)} bits)")
        print(f"\nFirst 64 bits: {binary_string[:64]}...")
        
        # Convert binary to Morse
        morse = binary_to_morse(binary_string)
        
        # Ask to play
        max_symbols = 200  # Limit playback
        print(f"\nReady to play first {max_symbols} symbols")
        print(f"(Each byte = 8 symbols, this is about {(max_symbols / 8):.1f} bytes)")
        
        response = input("\nPress Enter to play, or 'q' to quit: ").strip().lower()
        
        if response != 'q':
            play_morse(morse, max_symbols)
            print("Done!")
        else:
            print("Cancelled.")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

# Run programm
if __name__ == "__main__":
    main()