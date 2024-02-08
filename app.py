from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

def predict_fraud(input_values):
    model = pickle.load(open("model.pkl", "rb"))
    predicted = model.predict(input_values.reshape(1, -1))[0]
    return predicted

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get the input values from the form
        input_values = np.array([
            float(request.form.get('type')),
            float(request.form.get('amount')),
            float(request.form.get('oldbalanceOrg')),
            float(request.form.get('newbalanceOrig')),
            float(request.form.get('oldbalanceDest')),
            float(request.form.get('newbalanceDest'))
            
        ])
        predicted = predict_fraud(input_values)
        # Convert the prediction to a string ('Fraud' or 'Not Fraud')
        prediction_str = 'Fraud' if predicted == 1 else 'Not Fraud'
        return render_template('result.html', predict=prediction_str)
    return render_template('result.html', predict=None)

if __name__ == '__main__':
    app.run(debug=True)
