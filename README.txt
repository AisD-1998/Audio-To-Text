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

## Installation

### Download the App

You can download the latest version of the app from the [Releases](https://github.com/yourusername/your-repo/releases) page.

### Windows

1. Download the `script.exe` file from the [Releases](https://github.com/yourusername/your-repo/releases) page.
2. Run the executable file by double-clicking it.

### macOS

1. Download the `script` file from the [Releases](https://github.com/yourusername/your-repo/releases) page.
2. Open Terminal and navigate to the directory where the `script` file is located.
3. Run the following command to make the file executable:

   ```sh
   chmod +x script
   ```

4. You can then run the app by double-clicking the file or by running the following command in Terminal:

   ```sh
   ./script
   ```

## Building the App

If you want to build the app from source, follow these instructions.

### Prerequisites

- Python 3.7 or later
- `PyInstaller` for packaging the app
- `ffmpeg` binaries for Windows and macOS

### Setup

1. Clone this repository:

   ```sh
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

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
