import os
from PIL import Image
from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug import secure_filename

from classifier import predict_label


image_dir = '../data/images'

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=False)



@app.route('/', methods=['GET'])
@app.route('/predict')
def index():
	return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
	if request.method == 'POST':
		f = request.files['file']
		error = None
		image_path = None

		if not f.filename:
			error = 'No image selected'

		if error is None:
			image_path = secure_filename(f.filename)
			image_path = os.path.join(image_dir, image_path)
			f.save(image_path)
			class_label = get_label(image_path)

			return render_template('predict.html', class_label=class_label) 

		flash(error)

	return redirect(url_for('index')) 


def get_label(image_path):
	image = Image.open(image_path)
	return predict_label(image)

	
if __name__ == '__main__':
	app.run()
