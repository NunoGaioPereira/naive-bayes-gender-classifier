from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap
import pandas as pd
import numpy as numpy

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.externals import joblib

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
	df = pd.read_csv("data/names_dataset.csv")
	df_X = df.name
	df_Y = df.sex

	corpus = df_X
	cv = CountVectorizer()
	X = cv.fit_transform(corpus)

	naivebayes_model = open("models/naivebayesgendermodel.pkl", "rb")
	clf = joblib.load(naivebayes_model)

	if request.method == 'POST':
		namequery = request.form['namequery']
		if namequery == '':
			return render_template('index.html', error = "Empty Input")
		data = [namequery]
		vect = cv.transform(data).toarray()
		my_prediction = clf.predict(vect)
	return render_template('results.html', prediction = my_prediction, name = namequery.upper())



if __name__ == '__main__':
	app.run(debug=True)
