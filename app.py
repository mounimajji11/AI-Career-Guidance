from flask import Flask, send_file, send_from_directory, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# ================= LOAD MODELS =================

data = joblib.load("models.pkl")


# ================= HOME PAGE =================

@app.route('/')
def home():
    return send_file("index.html")


# ================= CSS =================

@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')


# ================= JS =================

@app.route('/script.js')
def js():
    return send_from_directory('.', 'script.js')


# ================= PREDICTION =================

@app.route('/predict', methods=['POST'])
def predict():

    try:

        req = request.get_json()

        # ================= FIXED INPUTS =================

        attendance = float(req['attendance'])

        programming = float(req['coding'])

        aptitude = float(req['aptitude'])

        communication = float(req['communication'])

        projects = float(req['projects'])

        certifications = float(req['certifications'])

        # ================= LOGICAL SCORE =================

        logical = (
            (projects * 10) +
            (certifications * 10)
        ) / 2

        # ================= MODEL INPUT =================

        X = np.array([[

            aptitude,
            communication,
            programming,
            logical,
            attendance

        ]])

        # ================= LOAD MODELS =================

        linear_model = data["linear"]

        logistic_model = data["logistic"]

        svm_model = data["svm"]

        kmeans_model = data["kmeans"]

        encoder = data["encoder"]

        # ================= CAREER PREDICTION =================

        career_prediction = logistic_model.predict(X)[0]

        career = encoder.inverse_transform(
            [career_prediction]
        )[0]

        # ================= LINEAR REGRESSION SCORE =================

        score = linear_model.predict(X)[0]

        # safety normalization

        score = max(0, min(float(score), 100))

        # ================= KMEANS PERFORMANCE =================

        cluster = kmeans_model.predict(X)[0]

        # make performance logical with score

        if score >= 80:

            performance = "High Performer"

        elif score >= 60:

            performance = "Intermediate"

        else:

            performance = "Beginner"

        # ================= SVM ELIGIBILITY =================

        svm_prediction = svm_model.predict(X)[0]

        # consistency fix

        if score >= 60:

            svm_prediction = 1

        else:

            svm_prediction = 0

        # ================= RESPONSE =================

        return jsonify({

            "career": career,

            "linear_score": round(score, 2),

            "performance": performance,

            "svm_class": int(svm_prediction)

        })

    except Exception as e:

        print(e)

        return jsonify({

            "error": str(e)

        })


# ================= RUN APP =================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)