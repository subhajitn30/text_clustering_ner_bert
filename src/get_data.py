## read params
## process
### return dataframe
import os
import yaml
import pandas as pd
import argparse

'''
This function is for reading the configuration parametrs
config_path: path for configuration file
returns configuartion parameter values
'''
def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

'''
This function is for getting the training data, which converts tabular data to dataframe
config_path: path for configuration file
returns training data in data frame format.
'''
def get_data(config_path):
    config = read_params(config_path)
    data_path = config["data_source"]["s3_source"]
    df = pd.read_csv(data_path)
    return df

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = get_data(config_path = parsed_args.config)