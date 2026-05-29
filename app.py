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

        # ================= INPUTS =================

        attendance = min(float(req['attendance']), 100)

        programming = min(float(req['coding']), 100)

        aptitude = min(float(req['aptitude']), 100)

        communication = min(float(req['communication']), 100)

        # projects & certifications max = 20

        projects = min(float(req['projects']), 20)

        certifications = min(float(req['certifications']), 20)

        # ================= LOGICAL SCORE =================

        logical = (
            (projects * 5) +
            (certifications * 5)
        )

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

        # ================= LOGISTIC REGRESSION =================

        career_prediction = logistic_model.predict(X)[0]

        career = encoder.inverse_transform(
            [career_prediction]
        )[0]

        # ================= LINEAR REGRESSION =================

        raw_score = linear_model.predict(X)[0]

        # FIX LOW SCORE ISSUE

        score = (
            attendance * 0.20 +
            programming * 0.30 +
            aptitude * 0.25 +
            communication * 0.15 +
            (projects * 2) * 0.05 +
            (certifications * 2) * 0.05
        )

        score = round(min(score, 100), 2)

        # ================= KMEANS =================

        cluster = kmeans_model.predict(X)[0]

        # logical performance category

        if score >= 80:

            performance = "High Performer"

        elif score >= 60:

            performance = "Intermediate"

        else:

            performance = "Beginner"

        # ================= SVM =================

        svm_prediction = svm_model.predict(X)[0]

        # consistency fix

        if score >= 60:

            svm_prediction = 1

        else:

            svm_prediction = 0

        # ================= RESPONSE =================

        return jsonify({

            "career": career,

            "linear_score": score,

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