# load the train and test
# train algo
# save the metrices, params
import os
import math
import warnings
import sys
import pandas as pd
import numpy as np
import sklearn.metrics as metrics
import numpy as np
import pandas as pd 
import re
import warnings
pd.set_option("display.max_colwidth", 200)
warnings.filterwarnings("ignore")
# import nltk
# import spacy                                       ## pip install -U spacy
# from nltk.tokenize.toktok import ToktokTokenizer
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from nltk.cluster import KMeansClusterer
from numpyencoder import NumpyEncoder
import nltk
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import numpy as np
import seaborn as sns
from get_data import read_params
import matplotlib.pyplot as plt
import argparse
import joblib
import json
import seaborn as sna
from sklearn.metrics import silhouette_score

'''
This function is for building and training the clustering model and save the results in the csv files
and save the cluster mapping json files. 

Finally, save the trained model for prediction.
'''
def train_clustering(config_path):
    config = read_params(config_path)
    process_data_path = config["process_data"]["processed_dataset_csv"]
    output_data_path = config["output_data"]["output_dataset_csv"]
    #random_state = config["base"]["random_state"]
    model_dir = config["model_dir"]


    #Building clustering model
    num_clusters = 17
    model = KMeans(n_clusters=num_clusters,max_iter=50, algorithm='auto', init='k-means++',n_init=10 )
    data= pd.read_csv(process_data_path)
    model.fit([np.array(np.matrix(x)).ravel()  for x in data['embediing_trf_roberta'] ])
    cluster_assignment = model.labels_
    data['Cluster_name']=cluster_assignment

    ######################################################################
    df1=pd.DataFrame(data.groupby(['Label','Cluster_name'])['Cluster_name'].count())
    df1.rename(columns = {'Cluster_name':'Count'}, inplace = True)
    df2=df1.reset_index()
    df2=df2.iloc[df2.groupby('Label')['Count'].idxmax().values.ravel()]
    l2c = dict(zip(list(df2.Label),df2.Cluster_name))
    l2c_file = open("saved_dictionary/l2c_dictionary_v1.json", "w")
    json.dump(l2c, l2c_file)
    l2c_file.close()
    data.to_csv(output_data_path)

#############################################################################
    
    range_n_clusters = [5, 7, 9, 11, 13, 15, 17, 19]
    score =[]
    for num_clusters in range_n_clusters:
    
        # intialise kmeans
        kmeans = KMeans(n_clusters=num_clusters,max_iter=50, algorithm='auto', init='k-means++',n_init=10)
        kmeans.fit([np.array(np.matrix(x)).ravel()  for x in data['embediing_trf_roberta'] ])
        
        cluster_labels = kmeans.labels_
        
        # silhouette score
        silhouette_avg = silhouette_score([np.array(np.matrix(x)).ravel()  for x in data['embediing_trf_roberta'] ], cluster_labels)
        score.append(silhouette_avg)
    silhouette_points = list(zip(range_n_clusters, score))  


    score_file = config["reports"]["scores"]
    #silhouette_file = config["reports"]["silhouette"]

    with open(score_file, "w") as sf:
        slht= {
            "silhouette" :[
                {"number_of_cluster":c,"silhouette_score":s}
                for c,s in silhouette_points
            ]
        }
        json.dump(slht, sf, indent=4, cls=NumpyEncoder)
    
#######################################################################################


    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model_v1.joblib")

    joblib.dump(model, model_path)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    train_clustering(config_path = parsed_args.config)