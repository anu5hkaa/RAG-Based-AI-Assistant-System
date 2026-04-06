import requests
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
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
    raise Exception("embedding failed after retries")
def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate", json={
        # "model": "deepseek-r1",
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    })

    response = r.json()
    print(response)
    return response

df=joblib.load('embedding.joblib')

incoming_question=input("Ask a question: ")
question_embedding=create_embedding([incoming_question])[0]
print(question_embedding)
print("step 1 done" )
similarities=  cosine_similarity (np.vstack(df['embedding']),[question_embedding]).flatten()
#print(similarities)
print("step2 done")
top_results=5
max_index=similarities.argsort()[::-1][0:top_results]
#print(max_index)
new_df=df.loc[max_index]
#print(new_df[["title","number",'text']])
prompt = f'''  you are a friendly  teaching assistant for this course helping user to understnad concepts in breif and letting t hem know the timestamp of that video from chunks .here are the video subtitle chunks contaning video title,video number ,start time in seconds ,end time in seconds,the 
text at tha time:
{new_df[['title','number','start','end','text']].to_json(orient='records')}
"{incoming_question}"
User asked the question related to the video chunks, you have to answer where and how much content is taught in which video and also explain the question in short to let them know thwhat that question is abhoout (in which video and what timestamp)
and guide the user to go to that particular video.if user askes unrealated question,tell him that you can only ask question realated to this course.

'''
print("step3 done")
with open("prompt.txt","w",encoding='utf-8') as f:
    f.write(prompt)
    print("going to call LLM...")
result = inference(prompt)
response=result.get('response',"")
print(response)

with open("response.txt", "w",encoding='utf-8') as f:
    f.write(response)
# for index, item in ne
#for index,item in new_df.iterrows():
 #   print(index,item['title'],item['number'],item['text'],item['start'],item['end'])