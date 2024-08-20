# audio_utils.py

from pydub import AudioSegment
import speech_recognition as sr
import os
import re


def convert_mav_to_wav(mav_file_path, wav_file_path):
    """
    Converts an MAV file to WAV format.
    
    :param mav_file_path: Path to the MAV file.
    :param wav_file_path: Path to save the converted WAV file.
    """
    audio = AudioSegment.from_file(mav_file_path, format="mav")
    audio.export(wav_file_path, format="wav")


def extract_text_from_audio(wav_file_path):
    """
    Extracts text from a WAV audio file using the Google Web Speech API.
    
    :param wav_file_path: Path to the WAV file.
    :return: Extracted text from the audio.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            return "Google Web Speech API could not understand the audio."
        except sr.RequestError as e:
            return f"Could not request results from Google Web Speech API; {e}"


def extract_numbers_from_text(text):
    """
    Extracts numbers from text, including both digit sequences and number words.
    
    :param text: Text extracted from the audio.
    :return: Combined integer representing all extracted numbers.
    """
    num_words = {
        'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
        'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
    }

    # Convert words to numbers using the mapping
    words = text.lower().split()
    word_numbers = [num_words[word] for word in words if word in num_words]

    # Use regular expressions to find all digit sequences in the text
    digit_numbers = re.findall(r'\d+', text)
    digit_numbers = [int(num) for num in digit_numbers]

    # Combine word numbers and digit numbers
    combined_numbers = word_numbers + digit_numbers

    # Combine the numbers into a single integer (if needed)
    if combined_numbers:
        combined_number = int(''.join(map(str, combined_numbers)))
        return combined_number
    return None


def process_audio(mav_file_path):
    """
    Converts an MAV file to WAV, extracts text, and then extracts numbers from that text.
    
    :param mav_file_path: Path to the MAV file.
    :return: Combined integer representing all extracted numbers from the audio.
    """
    wav_file_path = './converted.wav'

    # Convert MAV to WAV
    convert_mav_to_wav(mav_file_path, wav_file_path)

    # Extract text from the WAV file
    text = extract_text_from_audio(wav_file_path)

    # Extract numbers from the text
    numbers = extract_numbers_from_text(text)

    # Clean up the WAV file
    os.remove(wav_file_path)

    return numbers
