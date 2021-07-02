import nltk
import pickle
import re

from flask import Flask, request, render_template
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('stopwords')

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

port_stem = PorterStemmer()


def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
    stemmed_content = ' '.join(stemmed_content)
    return stemmed_content


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    int_features = [str(x) for x in request.form.values()]
    import pandas as pd
    int_features = pd.DataFrame(int_features)

    feature = int_features['content'] = int_features.loc[0, :] + ' ' + int_features.loc[1, :]
    feature = feature.apply(stemming)

    X = feature.values

    vectorizer = TfidfVectorizer()
    vectorizer.fit(X)
    X = vectorizer.transform(X)

    X__prediction = model.predict(X)

    prediction = X__prediction

    if X__prediction == 0:
        statement = 'The news is Real'
    else:
        statement = 'The news is Fake'

    return statement


if __name__ == '__main__':
    app.run()
