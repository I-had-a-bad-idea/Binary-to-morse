# Binary-to-morse

Listen to your favourite executables. Converts binary into morse and plays it. Sounds terrible but is fun.

## Description

This Python script converts binary files (like executables) into Morse code and plays it as audio. Each binary bit is represented as:
- 0 = dot (short beep)
- 1 = dash (long beep)

The script can either play the Morse code as actual audio tones (if PyAudio is installed) or display it visually in the terminal.

## Features

- Reads binary files and converts them to Morse code
- Audio playback support (requires PyAudio)
- Visual fallback mode if audio is not available
- Very fast playback speed for quick listening, but this makes it sound quite noisy
- Command-line interface

## Requirements

- Python 3.x
- PyAudio (optional, for audio playback)
  ```
  pip install pyaudio
  ```

## Usage

1. Run the script directly:
   ```
   python binary-to-morse.py
   ```
   Then enter the path to your binary file when prompted.

2. Or specify the file path as an argument:
   ```
   python binary-to-morse.py path/to/your/file.exe
   ```

The script will:
1. Read the first 50 bytes of the file
2. Convert the binary data to Morse code
3. Show a preview of the first 64 bits
4. Play the first 200 Morse code symbols (about 25 bytes)

## Audio Settings

- Dot duration: 80ms
- Dash duration: 240ms
- Gap between symbols: 50ms
- Tone frequency: 800 Hz

## License

MIT License - See LICENSE file for details.

## Why?

Because sometimes you just need to know what your executables sound like in Morse code. 


