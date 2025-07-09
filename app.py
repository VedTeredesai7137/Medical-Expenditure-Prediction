from flask import Flask, render_template, request
import numpy as np
import pickle
import os

app = Flask(__name__)

# Load the trained ML model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values from the form
        age = float(request.form['age'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        sex = request.form['sex']
        smoker = request.form['smoker']
        region = request.form['region']

        # Manually encode categorical variables
        sex_male = 1 if sex == 'male' else 0
        smoker_yes = 1 if smoker == 'yes' else 0
        region_northwest = 1 if region == 'northwest' else 0
        region_southeast = 1 if region == 'southeast' else 0
        region_southwest = 1 if region == 'southwest' else 0

        # Final input array (order must match training)
        input_features = np.array([[age, bmi, children, sex_male, smoker_yes,
                                    region_northwest, region_southeast, region_southwest]])

        # Predict using the model
        prediction = model.predict(input_features)[0]

        # Return result to the same page
        return render_template('index.html',
                               prediction_text=f'Estimated Medical Charges: ₹{prediction:,.2f}')

    except Exception as e:
        return render_template('index.html',
                               prediction_text=f'Error: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)
