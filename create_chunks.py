import whisper
import json
import os
model=whisper.load_model("base")
audios = os.listdir("audios")
for audio in audios:
    number=audio.split("_")[0]
    title=audio.split("_")[1]
    print(number ,title) 
    result=model.transcribe(audio=f"audios/{audio}",
                                   language='hi',
                                   task="translate",
                                   word_timestamps=False)
    
    chunks = []

    for segment in result["segments"]:
        chunks.append({
            "number": number,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
            "title":title
        })
    chunks_with_metadata={"chunks":chunks,"text":result["text"]}
    with open(f"jsons/{audio}.json", "w", encoding="utf-8") as f:
        json.dump(chunks_with_metadata, f, indent=4, ensure_ascii=False)

    print(chunks)
