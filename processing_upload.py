import os
import json
import time
import joblib
import pandas as pd
import requests
import whisper

WHISPER_MODEL_NAME = "base"  # same as create_chunks.py
_model = None


def get_whisper_model():
    """Load whisper once and reuse it across requests instead of reloading every upload."""
    global _model
    if _model is None:
        _model = whisper.load_model(WHISPER_MODEL_NAME)
    return _model


def create_embedding(text_list):
    # unchanged from read_chunks.py
    print(f"Creating embeddings for {len(text_list)} chunks...")
    for attempt in range(3):
        try:
            r = requests.post(
                "http://localhost:11434/api/embed",
                json={
                    "model": "bge-m3",
                    "input": text_list
                },
                timeout=300
            )
            return r.json()['embeddings']
            print("Embeddings received from Ollama.")
        except Exception as e:
            print(f"Retry {attempt+1}...")
            time.sleep(5)

    return []


def transcribe_file(file_path, number, title):
    """
    Same transcription + chunking logic as create_chunks.py, applied to a single
    uploaded file instead of looping over the audios/ folder.
    """
    model = get_whisper_model()
    print("Whisper started...")
    print("File:", file_path)
    print("File exists:", os.path.exists(file_path))
    print("File size (MB):", round(os.path.getsize(file_path) / (1024 * 1024), 2))
    result = model.transcribe(
        audio=file_path,
        language='hi',
        task="translate",
        word_timestamps=False
    )
    print("Whisper finished.")
    chunks = []
    for segment in result["segments"]:
        chunks.append({
            "number": number,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"],
            "title": title
        })

    chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

    os.makedirs("jsons", exist_ok=True)
    json_filename = f"jsons/{os.path.basename(file_path)}.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(chunks_with_metadata, f, indent=4, ensure_ascii=False)

    return chunks


def embed_and_store_chunks(chunks):
    """
    Same embedding logic as read_chunks.py, but appends to the existing
    embedding.joblib instead of overwriting it, so previously processed
    lectures aren't lost when a new one is uploaded.
    """
    texts = [c['text'] for c in chunks]
    embedding = []
    batch_size = 16  # unchanged from read_chunks.py

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"batch {i // batch_size + 1}")

        batch_embedding = create_embedding(batch)
        embedding.extend(batch_embedding)

        time.sleep(1)

    if os.path.exists('embedding.joblib'):
        existing_df = joblib.load('embedding.joblib')
        chunk_id = int(existing_df['chunk_id'].max()) + 1 if len(existing_df) else 0
    else:
        existing_df = None
        chunk_id = 0

    new_records = []
    for i, chunk in enumerate(chunks):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embedding[i]
        chunk_id += 1
        new_records.append(chunk)

    new_df = pd.DataFrame.from_records(new_records)

    if existing_df is not None:
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df

    joblib.dump(combined_df, 'embedding.joblib')
    return len(new_records)


def process_uploaded_file(file_path, number, title):
    print("========== UPLOAD STARTED ==========")

    print("STEP 1: Starting transcription")
    chunks = transcribe_file(file_path, number, title)
    print(f"STEP 2: Transcription finished. Chunks created: {len(chunks)}")

    print("STEP 3: Starting embedding generation")
    chunks_added = embed_and_store_chunks(chunks)
    print(f"STEP 4: Embeddings completed. Added {chunks_added} chunks.")

    print("========== UPLOAD FINISHED ==========")

    return chunks_added