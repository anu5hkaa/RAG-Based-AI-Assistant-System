import requests
import os
import json
import pandas as pd
import joblib
import time


def create_embedding(text_list):
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

        except Exception as e:
            print(f"Retry {attempt+1}...")
            time.sleep(5)

    return []


jsons = os.listdir('jsons')

my_dict = []
chunk_id = 0

for json_file in jsons:
    print(f"\nStarting embedding for {json_file}")

    with open(f"jsons/{json_file}", "r", encoding="utf-8") as f:
        content = json.load(f)

    texts = [c['text'] for c in content['chunks']]
    embedding = []
    batch_size = 16

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"batch {i//batch_size + 1}")

        batch_embedding = create_embedding(batch)
        embedding.extend(batch_embedding)

        time.sleep(1)

    for i, chunk in enumerate(content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = embedding[i]

        chunk_id += 1
        my_dict.append(chunk)


df = pd.DataFrame.from_records(my_dict)
joblib.dump(df, 'embedding.joblib')

print("Done")