import os
import wave
import datetime
from pydub import AudioSegment
from docx import Document
import speech_recognition as sr

# Set the path to the ffmpeg executable
ffmpeg_path = r"C:\ffmpeg\ffmpeg-7.0.2-essentials_build\bin\ffmpeg.exe"
AudioSegment.converter = ffmpeg_path

# Load the cleaned audio file
audio = AudioSegment.from_wav("videoplayback.wav")

# Split the audio into smaller chunks (e.g., 60 seconds each)
chunk_length_ms = 60 * 1000  # 60 seconds
chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

# Initialize recognizer
recognizer = sr.Recognizer()

# Create a new Word document
doc = Document()
doc_filename = "transcription.docx"

# Function to format timestamp
def format_timestamp(ms):
    seconds = ms / 1000
    return str(datetime.timedelta(seconds=seconds))

# Process each chunk
overall_offset = 0  # Keep track of the overall time offset

for i, chunk in enumerate(chunks):
    chunk_silent = AudioSegment.silent(duration=500)  # Add some silence before and after each chunk
    audio_chunk = chunk_silent + chunk + chunk_silent
    chunk_filename = f"chunk{i}.wav"
    audio_chunk.export(chunk_filename, format="wav")
    
    # Load the chunk into the recognizer
    with sr.AudioFile(chunk_filename) as source:
        audio_data = recognizer.record(source)
        
        try:
            # Transcribe the chunk using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            sentences = text.split('. ')
            for sentence in sentences:
                if sentence.strip():
                    timestamp = format_timestamp(overall_offset)
                    doc.add_paragraph(f"[{timestamp}] {sentence.strip()}")
            overall_offset += chunk_length_ms  # Update the overall time offset
            print(f"Chunk {i} processed successfully.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
        except sr.UnknownValueError:
            print(f"Google Web Speech API could not understand audio in chunk {i}")
    
    # Save the document after each chunk
    doc.save(doc_filename)
    print(f"Document saved after processing chunk {i}")

# Final save after all chunks are processed
doc.save(doc_filename)
print(f"Final transcription saved to '{doc_filename}'")
