import pickle
import numpy as np

# Load the trained model (ensure it's a scikit-learn model)
with open('student_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Check if the model is loaded correctly
print(f"Model type: {type(model)}")

# Sample input data (ensure it matches the model's feature set)
sample_input = np.array([[
    1,  # Marital_status
    1,  # Application_mode
    1,  # Application_order
    33,  # Course
    1,  # Daytime_evening_attendance
    1,  # Previous_qualification
    160,  # Previous_qualification_grade
    1,  # Nacionality
    1,  # Mothers_qualification
    1,  # Fathers_qualification
    1,  # Mothers_occupation
    1,  # Fathers_occupation
    160,  # Admission_grade
    0,  # Displaced
    0,  # Educational_special_needs
    0,  # Debtor
    1,  # Tuition_fees_up_to_date
    1,  # Gender
    0,  # Scholarship_holder
    20,  # Age_at_enrollment
    0,  # International
    0,  # Curricular_units_1st_sem_credited
    6,  # Curricular_units_1st_sem_enrolled
    5,  # Curricular_units_1st_sem_evaluations
    4,  # Curricular_units_1st_sem_approved
    13.5,  # Curricular_units_1st_sem_grade
    0,  # Curricular_units_1st_sem_without_evaluations
    0,  # Curricular_units_2nd_sem_credited
    6,  # Curricular_units_2nd_sem_enrolled
    5,  # Curricular_units_2nd_sem_evaluations
    4,  # Curricular_units_2nd_sem_approved
    14.0,  # Curricular_units_2nd_sem_grade
    0,  # Curricular_units_2nd_sem_without_evaluations
    10.0,  # Unemployment_rate
    2.5,  # Inflation_rate
    1.5,  # GDP
    1,  # Attendance
]]).reshape(1, -1)

# Make prediction (check if model has a 'predict' method)
if hasattr(model, 'predict'):
    prediction = model.predict(sample_input)

    # Map numerical prediction back to labels
    status_map = {0: 'Dropout', 1: 'Graduate', 2: 'Enrolled'}
    predicted_status = status_map.get(prediction[0], "Unknown")

    print(f"Predicted Student Status: {predicted_status}")
else:
    print("The model does not have a 'predict' method!")
