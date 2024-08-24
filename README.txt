# Audio Transcription App

This is a simple desktop application that transcribes audio files into text. The app supports various audio formats and can run on both Windows and macOS. It uses `ffmpeg` for audio processing and Google's Web Speech API for transcription.

## Features

- Supports multiple audio formats (WAV, MP3, FLAC, OGG, AAC, M4A)
- Converts audio to text using Google's Web Speech API
- Runs on both Windows and macOS
- Simple and intuitive graphical user interface (GUI)

## Requirements

### Windows
- Windows 7 or later

### macOS
- macOS 10.12 (Sierra) or later

### Python Packages

- pydub
- python-docx
- SpeechRecognition
- PyInstaller (for building the executable)

## Installation

### Prerequisites

- Python 3.7 or later
- `PyInstaller` for packaging the app
- `ffmpeg` binaries for Windows and macOS

### Setup

1. Clone this repository:

   ```sh
   git clone https://github.com/AisD-1998/Audio-To-Text.git
   cd Audio-To-Text
   ```

2. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Download the appropriate `ffmpeg` binaries for your platform:
   
   - For Windows, download `ffmpeg.exe` and `ffprobe.exe` and place them in `ffmpeg/windows/`.
   - For macOS, download the `ffmpeg` and `ffprobe` binaries and place them in `ffmpeg/macos/`.

### Building on Windows

1. Run the following command to package the app for Windows:

   ```sh
   python -m PyInstaller --onefile --windowed --add-data "ffmpeg/windows/;ffmpeg/windows/" script.py
   ```

2. The executable `script.exe` will be created in the `dist` directory.

### Building on macOS

1. Run the following command to package the app for macOS:

   ```sh
   python3 -m PyInstaller --onefile --windowed --add-data "ffmpeg/macos/:ffmpeg/macos/" script.py
   ```

2. The executable `script` will be created in the `dist` directory.

## Usage

1. Open the application.
2. Select an audio file you want to transcribe.
3. Choose an output directory where the transcription will be saved.
4. Click "Start Transcription".
5. Wait for the transcription to complete, and a link to the output file will be provided.

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This app uses [PyDub](https://github.com/jiaaro/pydub) for audio processing.
- Transcription is powered by [Google Web Speech API](https://cloud.google.com/speech-to-text).
- GUI is built using [Tkinter](https://docs.python.org/3/library/tkinter.html).

---

Feel free to reach out if you have any questions or need help with anything!
