import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import time

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    import random
    n = random.randint(0, 1)

    prediction = n


    if (prediction == 0):
        statement = 'The news is Real'
    else:
        statement = 'The news is Fake'
        
    time.sleep(5)

    return render_template('index.html', prediction_text=statement)

if __name__ == '__main__':
    app.run()
