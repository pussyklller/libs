import os
import ffmpeg
import asyncio
import tempfile
from pydub import AudioSegment
import speech_recognition as sr
from .. import loader

class AV2TLib(loader.Library):
    developer = "@frost_shard"
    version = (1, 0, 0)

    async def convert(self, input_data: bytes, output_format: str) -> bytes:
        """
        Конвертирует видео/аудио в указанный аудиоформат.
        :param input_data: Входной файл в формате байтов.
        :param output_format: Формат выходного файла ('mp3' или 'ogg').
        :return: Аудиофайл в байтах.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_in, \
             tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as temp_out:
            temp_in.write(input_data)
            temp_in.close()

            process = (
                ffmpeg
                .input(temp_in.name)
                .output(temp_out.name, format=output_format, acodec="libmp3lame" if output_format == "mp3" else "libvorbis")
                .overwrite_output()
            )
            await asyncio.get_event_loop().run_in_executor(None, process.run)

            temp_out.close()

            with open(temp_out.name, "rb") as f:
                output_data = f.read()

            os.unlink(temp_in.name)
            os.unlink(temp_out.name)

        return output_data

    async def recognize(self, input_data: bytes, language: str = "en-US") -> str:
        """
        Распознаёт речь из аудио.
        :param input_data: Аудиофайл в формате байтов.
        :param language: Язык для распознавания.
        :return: Распознанный текст.
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as temp_audio, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            temp_audio.write(input_data)
            temp_audio.close()

            audio = AudioSegment.from_file(temp_audio.name, format="ogg")
            audio.export(temp_wav.name, format="wav")
            temp_wav.close()

            recognizer = sr.Recognizer()
            with sr.AudioFile(temp_wav.name) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data, language=language)
                except sr.UnknownValueError:
                    text = "Speech was not recognized."
                except sr.RequestError:
                    text = "Google Speech Recognition API is unavailable."

            os.unlink(temp_audio.name)
            os.unlink(temp_wav.name)

        return text

async def init():
    return A2TLib()
