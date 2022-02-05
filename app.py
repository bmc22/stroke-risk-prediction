from flask import Flask, render_template, request
import numpy as np
from xgboost import XGBClassifier
import pandas as pd
import sklearn


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    gender = request.form.get('gender')
    age = int(request.form['age'])
    hypertension = request.form.get('hypertension')
    heart_disease = request.form.get('heart_disease')
    ever_married = request.form.get('ever_married')
    residence_type = request.form.get('residence_type')
    avg_glucose_level = float(request.form['avg_glucose_level'])
    bmi = float(request.form['bmi'])
    work_type = request.form.get('work_type')
    smoking_status = request.form.get('smoking_status')

    # defining the values of the work_type columns
    govt_job = never_worked = private = self_employed = child = 0

    if work_type == "gvt_job":
        govt_job = 1
    elif work_type == "never_worked":
        never_worked = 1
    elif work_type == "private":
        private = 1
    elif work_type == "self_employed":
        self_employed = 1
    elif work_type == "child":
        child = 1

        # defining the values of the smoking_status columns

    uknown = formerly_smoked = never_smoked = smokes = 0

    if smoking_status == "formerly_smoked":
        formerly_smoked = 1
    elif smoking_status == "never_smoked":
        never_smoked = 1
    elif smoking_status == "smokes":
        smokes = 1

    # --------------------- importing the data ---------------------
    data = pd.read_csv("stroke.csv", skiprows=0)

    # --------------------- the machine learning model -------------

    # the X matrix contains all the data before the last column (the features)
    X = data.values[:, :17]

    # the Y matrix contains the data in the last column (the response variable)
    Y = data.values[:, 17]

    # using the xgboost classifier
    clf = XGBClassifier(booster= 'gbtree', verbosity= 0, use_label_encoder= False, scale_pos_weight=23).fit(X, Y)

    data_values = np.array([[1 if gender == "male" else 0,
                             age,
                             1 if hypertension == "yes" else 0,
                             1 if heart_disease == "yes" else 0,
                             1 if ever_married == "yes" else 0,
                             1 if residence_type == "urban" else 0,
                             avg_glucose_level,
                             bmi,
                             govt_job, never_worked, private, self_employed, child,
                             uknown, formerly_smoked, never_smoked, smokes]])

    result = clf.predict(data_values)

    return render_template('result.html', prediction= result, org_input = [gender, age, hypertension, heart_disease, ever_married, residence_type, avg_glucose_level, bmi, work_type, smoking_status])


if __name__ == "__main__":
    app.run(debug=True)

