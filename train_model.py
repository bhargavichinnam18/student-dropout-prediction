import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib

# Load the dataset
data = pd.read_csv("databaru.csv")

# Preprocess the data
data['Curricular_units_1st_sem_grade'] = data['Curricular_units_1st_sem_grade'].apply(lambda x: min(40, x * 2))
data['Curricular_units_2nd_sem_grade'] = data['Curricular_units_2nd_sem_grade'].apply(lambda x: min(40, x * 2))

# Enhance attendance feature
data['attendance_weighted'] = 4 - data['Attendance']  # Higher value = lower attendance = higher risk

# Define features and target
features = [
    'Course', 'Daytime_evening_attendance', 'Admission_grade',
    'Educational_special_needs', 'Debtor', 'Tuition_fees_up_to_date',
    'Gender', 'Scholarship_holder', 'Curricular_units_1st_sem_grade',
    'Curricular_units_2nd_sem_grade', 'attendance_weighted'
]
target = 'Status'

X = data[features]
y = data[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
numerical_features = ['Admission_grade', 'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade', 'attendance_weighted']
X_train[numerical_features] = scaler.fit_transform(X_train[numerical_features])
X_test[numerical_features] = scaler.transform(X_test[numerical_features])

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
})
feature_importance = feature_importance.sort_values(by='Importance', ascending=False)
print("\nFeature Importance:")
print(feature_importance)

# Save the model and scaler
joblib.dump(model, 'student_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
print("Model and scaler saved as student_model.pkl and scaler.pkl")