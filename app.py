from flask import Flask, send_file, send_from_directory, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load models
data = joblib.load("models.pkl")


@app.route('/')
def home():
    return send_file("index.html")


@app.route('/style.css')
def css():
    return send_from_directory('.', 'style.css')


@app.route('/script.js')
def js():
    return send_from_directory('.', 'script.js')


@app.route('/predict', methods=['POST'])
def predict():

    try:

        req = request.get_json()

        aptitude = float(req['aptitude'])
        communication = float(req['communication'])
        programming = float(req['programming'])
        logical = float(req['logical'])
        attendance = float(req['attendance'])

        X = np.array([[
            aptitude,
            communication,
            programming,
            logical,
            attendance
        ]])

        linear_model = data["linear"]
        logistic_model = data["logistic"]
        svm_model = data["svm"]
        kmeans_model = data["kmeans"]
        encoder = data["encoder"]

        career_prediction = logistic_model.predict(X)[0]

        career = encoder.inverse_transform(
            [career_prediction]
        )[0]

        score = linear_model.predict(X)[0]

        cluster = kmeans_model.predict(X)[0]

        if cluster == 0:
            performance = "Low Performer"

        elif cluster == 1:
            performance = "Average Performer"

        else:
            performance = "High Performer"

        svm_prediction = svm_model.predict(X)[0]

        return jsonify({

            "career": career,
            "linear_score": round(float(score), 2),
            "performance": performance,
            "svm_class": int(svm_prediction)

        })

    except Exception as e:

        print(e)

        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)