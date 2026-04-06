import whisper
import json
# load whisper model (fast & reliable)
model = whisper.load_model("tiny")

# exact audio file path (NO | symbol, ffmpeg-safe)
audio_path = r"C:/Users\Anushka\Downloads/Introduction to Java Language-Lecture 1-Complete Placement Course [yRpLlJmRo2w].mp3"
# transcribe audio
print("Trnascription started..pls wait")
result = model.transcribe(audio_path,task='translate',language='hi')

# print transcription
print(result["text"])