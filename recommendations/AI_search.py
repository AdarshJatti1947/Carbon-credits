##from train1 import train
from train1 import df1,df
import torch
from sentence_transformers import SentenceTransformer
import pandas as pd
import pickle

device = 'cpu'  # Use 'cuda' for Nvidia GPU or 'cpu' for CPU
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
model = model.to(device) # "mps" for Mac Gpu or "cuda" for Nvidia Gpu
from sentence_transformers import util
import pandas as pd

with open('D:/CAPSTONE-BACKEND/recommendations/meme-embeddings1.pkl','rb') as f:
  embeddings1=pickle.load(f)

with open('D:/CAPSTONE-BACKEND/recommendations/meme-embeddings2.pkl','rb') as f:
  embeddings2=pickle.load(f)
  
  
def fun1(prompt):
  prompt_embedding = model.encode(prompt, convert_to_tensor=True)
  hits = util.semantic_search(prompt_embedding, embeddings1, top_k=15)
  hits = pd.DataFrame(hits[0], columns=['corpus_id', 'score'])

  # Note that "corpus_id" is the index of the meme for that embedding
  # You can use the "corpus_id" to look up the meme

  miss=util.semantic_search(prompt_embedding, embeddings2, top_k=15)
  miss = pd.DataFrame(miss[0], columns=['corpus_id', 'score'])

  # Extracting corpus_id values as a list

  hits_filtered1 = hits[hits['score'] >= 0.50]

  corpus_ids_list1 = hits_filtered1['corpus_id'].tolist()

  #print(corpus_ids_list1)

  hits_filtered2 = miss[miss['score'] >= 0.50]

  corpus_ids_list2 = hits_filtered2['corpus_id'].tolist()

  #print(corpus_ids_list2)

  # Retrieve rows based on row numbers in corpus_ids_list_modified
  selected_rows1 = df1.iloc[corpus_ids_list1]
  selected_rows2 = df1.iloc[corpus_ids_list2]

  # Include a particular column
  selected_rows_with_column1 = selected_rows1[['organisation','Merged_Column']]

  #selected_rows_with_column1


  selected_rows_with_column2 = selected_rows2[['organisation','Merged_Column']]

  #selected_rows_with_column2

  first_hit_score = hits['score'].iloc[0]
  first_miss_score = miss['score'].iloc[0]

  #print("First score from hits:", first_hit_score)
  #print("First score from miss:", first_miss_score)

  #mongodb://localhost:27017/GICC

  if len(corpus_ids_list1)!=0 and len(corpus_ids_list2)!=0:
    if first_hit_score>first_miss_score:
      return pd.DataFrame(selected_rows_with_column1)
    else:
      return pd.DataFrame(selected_rows_with_column2)
  else:
    if len(corpus_ids_list1)==0:
      return pd.DataFrame(selected_rows_with_column2)
    if len(corpus_ids_list2)==0:
      return pd.DataFrame(selected_rows_with_column1)



import json

def get_keys(prompt):
  #prompt="Give me details of all the EV companies from the United States"
  
  result=fun1(prompt)

  json_data = result.to_json()
  data = json.loads(json_data)
  company_keys = list(data['organisation'].keys())
  company_keys = [ int(x) for x in company_keys ]
  column_name = '_id'
  selected_rows_column = df.loc[company_keys,column_name]
  selected_rows_column = selected_rows_column.to_json(default_handler=str)
  return selected_rows_column

prompt = input()
get_keys(prompt)

