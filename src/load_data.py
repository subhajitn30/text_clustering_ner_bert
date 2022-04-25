# read the data from data source
## save it in the data/processed for further process
import os
from get_data import read_params, get_data
import argparse
import re


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


'''
This function is for saving the preprocessed data into CSV files. 
'''
def load_and_save(config_path):
    config = read_params(config_path)
    data = get_data(config_path)
    data = data.dropna()
    #call the function
    cleaned_text = []
    data['Test Case Description']=data['Test Case Description'].astype(str)
    for t in data['Test Case Description']:
        cleaned_text.append(text_cleaner(t))
    data['cleaned_text']=cleaned_text
    ### Dropping duplicates
    data.drop_duplicates(keep='first', inplace=True)
    data['cleaned_text'].drop_duplicates(keep='first', inplace=True)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    data.to_csv(raw_data_path)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)  