import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("dataset.csv")

X = df[['Aptitude','Communication','Programming','Logical','Attendance']]
y = df['Career']

# Encode output
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# -------- MODEL 1: Linear Regression --------
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# -------- MODEL 2: Logistic Regression --------
logistic_model = LogisticRegression(max_iter=2000)
logistic_model.fit(X_train, y_train)

# -------- MODEL 3: SVM --------
svm_model = SVC(kernel='linear', probability=True)
svm_model.fit(X_train, y_train)

# -------- MODEL 4: KMeans --------
kmeans_model = KMeans(n_clusters=3, random_state=42, n_init=10)
kmeans_model.fit(X)

# Save everything
joblib.dump({
    "linear": linear_model,
    "logistic": logistic_model,
    "svm": svm_model,
    "kmeans": kmeans_model,
    "encoder": le
}, "models.pkl")

print("✅ Model training completed successfully")