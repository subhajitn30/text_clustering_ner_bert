from sentence_transformers import SentenceTransformer
import os
from get_data import read_params
import argparse
import re
import pandas as pd


model = SentenceTransformer('paraphrase-mpnet-base-v2')



def embeddings(data):
    sentence_embeddings = model.encode(list(data['cleaned_text']))
    return sentence_embeddings


def data_embeddings(config_path):
    config = read_params(config_path)
    raw_data_path = config["load_data"]["raw_dataset_csv"]
    data = pd.read_csv(raw_data_path)
    embeddings_trs=embeddings(data)
    data['embediing_trf_roberta']=list(embeddings_trs)
    processed_data_path = config["process_data"]["processed_dataset_csv"]
    data.to_csv(processed_data_path)

if __name__=="__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data_embeddings(config_path=parsed_args.config)  





