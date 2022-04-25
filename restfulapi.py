from prediction_service import prediction as pred 
import sys
import os
from flask import request
from utils.main_app import app
from utils.response_util import response_with
from flask_restful import Api, Resource, reqparse
import json

parser = reqparse.RequestParser()
parser.add_argument('data')


def predict_doamin(Input_text):
    return pred.predict_domain(Input_text)

def predict_entity(Input_text):
    return pred.predict_entity_api(Input_text)

@app.route('/')
def get_home():
    return response_with({'message':'Named Entity Recognition'})

@app.route('/api/predictdomain', methods=['POST'])

def PredictDomain():
    #args = parser.parse_args()
    request_data = request.get_json()
    print('THE INPUT DATA:',request_data)
    input_text = request_data['input_text']
    #input_text = request.args.get('input_text')
    print('THE INPUT DATA:',input_text)
    domain = predict_doamin(input_text)
   
    return response_with(domain)

@app.route('/api/predictentity', methods=['POST'])
def PredictEntity():
    request_data = request.get_json()
    print('THE INPUT DATA:',request_data)
    input_text = request_data['input_text']
    #input_text = request.args.get('input_text')
    print('THE INPUT DATA:',input_text)
    entity = predict_entity(input_text)
   
    return response_with(entity)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="8085", threaded=True)


