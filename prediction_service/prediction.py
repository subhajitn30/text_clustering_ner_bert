
import json
import joblib
import numpy as np
#from src import data_embedding as emb
import streamlit as st 
from sentence_transformers import SentenceTransformer
#from src import load_data as ld
import re
import spacy
from spacy import displacy



#model_in = open("saved_models/model.joblib","rb")
model_in = open("saved_models/cls_mpnetv2_v4.joblib","rb")
cls_model=joblib.load(model_in)
NER = spacy.load("en_core_web_sm")

'''
This function is for text pre-processing, which is basically raw textual data.
Arguments::
text: input raw text to be pre-processed, should be a string
returns processed data.

'''
def text_cleaner(text):
   
    newString = text.lower()
    newString = re.sub(r"pre-conditions:","",newString)
    newString = re.sub(r"precondition:","",newString)
    newString = re.sub(r"hey","",newString)
    newString = re.sub(r"portal","",newString)
    newString = re.sub(r"hp","",newString)
    newString = re.sub(r"[^a-zA-Z]+", ' ', newString)
    #newString = remove_stopwords(newString)
    return newString

## Calling pre-trained text embedding model for encoding the text data
model = SentenceTransformer('paraphrase-mpnet-base-v2')

'''
This function is for text embedding of pre-processed data
arguments::
input_text: Processed input text data for embeddings.
returns encoded textual data.
'''
def embedding_text(input_text):
    input = text_cleaner(input_text)
    return model.encode(input_text)

'''
This function is for predicting domain of the input processed text.
arguments::
input_text: Processed input text data for embeddings.
returns the domain of the text data.
'''
def predict_domain(input_text):
    emb_text=embedding_text(input_text)
    out_put=cls_model.predict([emb_text])
    l2c_file = open("saved_dictionary/l2c_dictionary_v2.json", "r")
    l2c = l2c_file.read()
    l2c_data = json.loads(l2c)
    result=list(l2c_data.keys())[list(l2c_data.values()).index(out_put)]
    return result


'''
This function is for predicting the named entity of processed text 
such as 'person','GPE', etc.
arguments::
input_text: Processed input text data for embeddings.
returns the resulted entity data.
'''
def predict_entity(input_text):
    raw_text=input_text
    text1= NER(raw_text)
    words=[]
    entity=[]
    for word in text1.ents:
        words.append(word.text)
        entity.append(word.label_)
        word_entity_dict=dict(zip(words,entity))

    return displacy.render(text1,style="ent")

def predict_entity_api(input_text):
    raw_text=input_text
    text1= NER(raw_text)
    words=[]
    entity=[]
    word_entity_dict = {}
    for word in text1.ents:
        words.append(word.text)
        entity.append(word.label_)
        word_entity_dict=dict(zip(words,entity))
    return word_entity_dict




