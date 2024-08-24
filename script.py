import os
import platform
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from pydub import AudioSegment
from docx import Document
import speech_recognition as sr
from threading import Thread
import webbrowser

class TranscriptionApp:
    def __init__(self, root):
        print("Initializing application...")
        self.root = root
        self.root.title("Audio Transcription App")
        self.root.geometry("600x500")
        self.root.configure(bg="#f7f7f7")
        self.root.resizable(True, True)

        # Initialize cancel flag and set the ffmpeg path
        self.cancel_flag = False
        self.set_ffmpeg_paths()

        # Create and place GUI elements
        self.create_widgets()

    def set_ffmpeg_paths(self):
        print("Setting FFmpeg paths...")
        base_dir = os.path.dirname(__file__)
        if platform.system() == 'Windows':
            self.ffmpeg_path = os.path.join(base_dir, 'ffmpeg', 'windows', 'ffmpeg.exe')
            self.ffprobe_path = os.path.join(base_dir, 'ffmpeg', 'windows', 'ffprobe.exe')
        elif platform.system() == 'Darwin':  # macOS
            self.ffmpeg_path = os.path.join(base_dir, 'ffmpeg', 'macos', 'ffmpeg')
            self.ffprobe_path = os.path.join(base_dir, 'ffmpeg', 'macos', 'ffprobe')
        else:
            raise Exception("Unsupported operating system")

        # Set ffmpeg and ffprobe for pydub
        AudioSegment.converter = self.ffmpeg_path
        AudioSegment.ffprobe = self.ffprobe_path

    def create_widgets(self):
        print("Creating widgets...")
        # File selection section
        file_frame = ttk.Frame(self.root, padding="10")
        file_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(file_frame, text="1. Select Audio File:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="grey")
        self.file_label.pack(anchor="w", pady=2)
        self.select_button = ttk.Button(file_frame, text="Browse", command=self.select_file)
        self.select_button.pack(anchor="w", pady=5)

        # Output directory selection section
        output_frame = ttk.Frame(self.root, padding="10")
        output_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(output_frame, text="2. Select Output Directory:", font=("Arial", 10, "bold")).pack(anchor="w")
        self.output_dir_label = ttk.Label(output_frame, text="No directory selected", foreground="grey")
        self.output_dir_label.pack(anchor="w", pady=2)
        self.output_dir_button = ttk.Button(output_frame, text="Browse", command=self.select_output_dir)
        self.output_dir_button.pack(anchor="w", pady=5)

        # Action buttons section
        action_frame = ttk.Frame(self.root, padding="10")
        action_frame.pack(pady=10, padx=10, fill="x")

        self.transcribe_button = ttk.Button(action_frame, text="Start Transcription", command=self.start_transcription)
        self.transcribe_button.pack(anchor="w", pady=5)
        self.transcribe_button.config(state=tk.DISABLED)

        self.cancel_button = ttk.Button(action_frame, text="Cancel", command=self.cancel_transcription)
        self.cancel_button.pack(anchor="w", pady=5)
        self.cancel_button.config(state=tk.DISABLED)

        # Progress bar section
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, padx=10, fill="x")

        # Output log section
        self.progress_text = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, font=("Arial", 10))
        self.progress_text.pack(pady=10, padx=10, fill="both", expand=True)

    def select_file(self):
        print("Selecting file...")
        filetypes = [("Audio Files", "*.wav *.mp3 *.flac *.ogg *.aac *.m4a")]
        self.audio_file = filedialog.askopenfilename(filetypes=filetypes)
        if self.audio_file:
            self.file_label.config(text=f"Selected: {os.path.basename(self.audio_file)}", foreground="black")
            self.transcribe_button.config(state=tk.NORMAL)
        else:
            self.file_label.config(text="No file selected", foreground="grey")
            self.transcribe_button.config(state=tk.DISABLED)

    def select_output_dir(self):
        print("Selecting output directory...")
        self.output_dir = filedialog.askdirectory()
        if self.output_dir:
            self.output_dir_label.config(text=f"Selected: {self.output_dir}", foreground="black")
        else:
            self.output_dir_label.config(text="No directory selected", foreground="grey")

    def start_transcription(self):
        print("Starting transcription...")
        if self.audio_file and self.output_dir:
            self.transcribe_button.config(state=tk.DISABLED)
            self.select_button.config(state=tk.DISABLED)
            self.output_dir_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            self.progress_text.delete(1.0, tk.END)
            self.progress_text.insert(tk.END, "Starting transcription...\n")
            self.progress_var.set(0)
            self.cancel_flag = False
            thread = Thread(target=self.transcribe_audio)
            thread.start()
        else:
            messagebox.showerror("Error", "No audio file or output directory selected.")

    def cancel_transcription(self):
        print("Cancelling transcription...")
        self.cancel_flag = True
        self.progress_text.insert(tk.END, "Cancelling transcription...\n")

    def transcribe_audio(self):
        print("Transcribing audio...")
        try:
            # Load the selected audio file
            audio = AudioSegment.from_file(self.audio_file)

            # Split the audio into smaller chunks (e.g., 60 seconds each)
            chunk_length_ms = 60 * 1000  # 60 seconds
            chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

            recognizer = sr.Recognizer()
            overall_offset = 0  # Keep track of the overall time offset

            doc_filename = os.path.join(self.output_dir, "transcription.docx")
            doc = Document()  # Create a new Word document

            for i, chunk in enumerate(chunks):
                if self.cancel_flag:
                    self.progress_text.insert(tk.END, "Transcription cancelled by user.\n")
                    break

                chunk_silent = AudioSegment.silent(duration=500)  # Add some silence before and after each chunk
                audio_chunk = chunk_silent + chunk + chunk_silent
                chunk_filename = f"chunk{i}.wav"

                audio_chunk.export(chunk_filename, format="wav")

                with sr.AudioFile(chunk_filename) as source:
                    audio_data = recognizer.record(source)
                    
                    try:
                        # Transcribe the chunk using Google Web Speech API
                        text = recognizer.recognize_google(audio_data)
                        sentences = text.split('. ')
                        for sentence in sentences:
                            if sentence.strip():
                                timestamp = self.format_timestamp(overall_offset)
                                doc.add_paragraph(f"[{timestamp}] {sentence.strip()}")
                        overall_offset += len(chunk)  # Update the overall time offset by actual chunk length
                        self.progress_text.insert(tk.END, f"Chunk {i} processed successfully.\n")
                        self.progress_var.set((i + 1) / len(chunks) * 100)
                    except sr.RequestError as e:
                        self.progress_text.insert(tk.END, f"Could not request results from Google Web Speech API; {e}\n")
                    except sr.UnknownValueError:
                        self.progress_text.insert(tk.END, f"Google Web Speech API could not understand audio in chunk {i}\n")
                    except Exception as e:
                        self.progress_text.insert(tk.END, f"Error processing chunk {i}: {e}\n")

                # Delete the chunk file after processing
                os.remove(chunk_filename)

            if not self.cancel_flag:
                # Save the document after all chunks are processed
                doc.save(doc_filename)
                self.progress_text.insert(tk.END, f"Final transcription saved to '{doc_filename}'\n")

                # Display a clickable link to the Word document
                link = ttk.Label(self.root, text="Open Transcription", foreground="blue", cursor="hand2", font=("Arial", 10, "bold"))
                link.pack(pady=10)
                link.bind("<Button-1>", lambda e: self.open_file(doc_filename))

        except Exception as e:
            self.progress_text.insert(tk.END, f"Error: {e}\n")
        finally:
            self.transcribe_button.config(state=tk.NORMAL)
            self.select_button.config(state=tk.NORMAL)
            self.output_dir_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            self.progress_var.set(0)

    def open_file(self, path):
        webbrowser.open(f'file://{os.path.realpath(path)}')

    def format_timestamp(self, ms):
        seconds = ms / 1000
        return str(datetime.timedelta(seconds=seconds))

if __name__ == "__main__":
    print("Starting GUI...")
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()
    print("GUI closed.")
