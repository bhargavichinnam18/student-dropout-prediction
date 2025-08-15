import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from joblib import load
import plotly.graph_objects as go
import requests  # Added for potential real-time API integration

st.set_page_config(layout="wide")

# Apply a global black background theme
st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
            color: #ffffff;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] h2 {
            color: #333333 !important;
        }
        .stSelectbox label, .stTextInput label, .stRadio label, .stNumberInput label {
            color: #ffffff !important;
        }
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #333333;
            color: #ffffff;
            border-color: #555555;
        }
        .stSelectbox div[data-baseweb="select"] span {
            color: #ffffff !important;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: 1px solid #388E3C;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #45a049;
            border-color: #388E3C;
        }
        [data-testid="stSidebar"] {
            background-color: #222222;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        .plotly .modebar {
            background-color: #222222 !important;
        }
        .plotly .modebar-btn text, .plotly .modebar-btn span {
            color: #ffffff !important;
            fill: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# Check if the CSV file exists to catch potential file-related errors
try:
    data = pd.read_csv("databaru.csv", delimiter=",")
    data_0 = data.loc[data['Status'] == 0]
    data_1 = data.loc[data['Status'] == 1]
    data_2 = data.loc[data['Status'] == 2]
except FileNotFoundError:
    st.error("Error: 'databaru.csv' file not found. Please ensure the file exists in the same directory as app.py.")
    st.stop()

category_mapping = {
    33: 'Computer Science (Specialisation)',
    171: 'Animation and Multimedia Design',
    8014: 'Social Service (evening attendance)',
    9003: 'Agronomy',
    9070: 'Information Technology',
    9085: 'Veterinary Nursing',
    9119: 'Informatics Engineering',
    9130: 'Equinculture',
    9147: 'Management',
    9238: 'Social Service',
    9254: 'Tourism',
    9500: 'Computer Science',
    9556: 'Oral Hygiene',
    9670: 'Advertising and Marketing Management',
    9773: 'Journalism and Communication',
    9853: 'Electronics',
    9991: 'Management (evening attendance)'
}
data['Course_Label'] = data['Course'].replace(category_mapping)

# Initialize session state for login and prediction results
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None  # To store prediction output
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Dashboard"  # Default page

# Define the login page with the college logo
def login_page():
    st.markdown("""
        <style>
            h1 {
                color: #ffffff !important;
                font-size: 2rem !important;
                font-weight: bold !important;
                text-align: center !important;
                margin-bottom: 10px !important;
            }
            h2 {
                color: #ffffff !important;
                font-size: 1.5rem !important;
                font-weight: bold !important;
                text-align: center !important;
                margin-bottom: 5px !important;
            }
            img {
                max-height: 100px;
                object-fit: contain;
            }
        </style>
    """, unsafe_allow_html=True)

    st.image("https://nnrg.edu.in/bcategory/nnrg-logo.jpg", use_container_width=True, output_format="auto")
    st.markdown('<div style="margin-bottom: 10px;"></div>', unsafe_allow_html=True)

    st.header("Login Page")
    st.title("Login")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("""
                <style>
                    [data-testid="stVerticalBlockBorderWrapper"] {
                        background-color: #ffffff;
                        border: 2px solid #ccc;
                        border-radius: 5px;
                        padding: 10px;
                        text-align: center;
                        color: #333;
                    }
                    .stTextInput > div > div > input {
                        width: 100%;
                        padding: 10px;
                        margin: 5px 0;
                        border: 1px solid #ccc;
                        border-radius: 5px;
                        box-sizing: border-box;
                        font-size: 16px;
                    }
                    .stTextInput label {
                        color: #333 !important;
                        font-size: 16px !important;
                    }
                    .stButton button {
                        width: 100%;
                        padding: 10px;
                        background-color: #4CAF50;
                        color: white;
                        border: 1px solid #388E3C;
                        border-radius: 5px;
                        font-size: 16px;
                        margin-top: 5px;
                    }
                    .stButton button:hover {
                        background-color: #45a049;
                        border-color: #388E3C;
                    }
                    .error {
                        color: red;
                        text-align: center;
                        margin-top: 5px;
                        font-size: 14px;
                    }
                    .forgot-password {
                        color: #cccccc;
                        font-size: 14px;
                        text-align: center;
                        margin-top: 5px;
                    }
                </style>
            """, unsafe_allow_html=True)

            with st.form(key="login_form"):
                username = st.text_input("Username", key="login-username")
                password = st.text_input("Password", type="password", key="login-password")
                submit_button = st.form_submit_button("Login")

                if submit_button:
                    username = username.strip()
                    password = password.strip()
                    if username == "admin" and password == "1234":
                        st.session_state.logged_in = True
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.markdown('<div class="error">Invalid username or password.</div>', unsafe_allow_html=True)

            st.markdown('<div class="forgot-password"><a href="#">Forgot Password?</a></div>', unsafe_allow_html=True)

# Define logout functionality
def logout():
    st.session_state.logged_in = False
    st.session_state.prediction_result = None  # Clear prediction result on logout
    st.session_state.selected_page = "Dashboard"  # Reset to Dashboard
    st.rerun()

# Main app logic
if not st.session_state.logged_in:
    login_page()
else:
    # Add logout button in the sidebar
    st.sidebar.button("Logout", on_click=logout, key="logout-button")

    # Sidebar navigation with added "Prediction Result" page
    add_selectbox = st.sidebar.selectbox(
        "Choose a page",
        ("Dashboard", "Prediction", "Prediction Result"),
        index=["Dashboard", "Prediction", "Prediction Result"].index(st.session_state.selected_page),
        key="page-selectbox"
    )

    # Update session state based on user selection
    if add_selectbox != st.session_state.selected_page:
        st.session_state.selected_page = add_selectbox
        st.rerun()

    def add_rating(content):
        return f"""
            <div style='
                height: auto;
                border: 2px solid #ccc;
                border-radius: 5px;
                font-size: 25px;
                padding-bottom: 38px;
                padding-top: 38px;
                background-color: #ffffff;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
                color: #333;
                '>{content}</div>
            """

    def add_card(content):
        return f"""
            <div style='
                height: auto;
                font-size: auto;
                border: 2px solid #ccc;
                border-radius: 5px;
                padding: 10px;
                margin-bottom: 10px;
                background-color: #ffffff;
                text-align: center;
                display: flex;
                justify-content: center;
                align-items: center;
                line-height: 70px;
                color: #333;
                '>{content}</div>
            """

    def create_pie_chart(column, title):
        try:
            value_counts = kelas[column].value_counts()
            if len(value_counts) > 1:
                names = [False, True]
            else:
                if 1 in value_counts.index:
                    names = [True]
                elif 0 in value_counts.index:
                    names = [False]
            colors = ['#ffffff', '#666666']
            fig = px.pie(
                values=value_counts,
                names=names,
                title=title,
                color_discrete_sequence=colors)
            fig.update_layout(
                height=200,
                margin=dict(l=0, r=10, t=70, b=10),
                title=dict(
                    x=0,
                    font=dict(size=15, color='#ffffff'),
                ),
                plot_bgcolor='#000000',
                paper_bgcolor='#000000',
                font=dict(color='#ffffff'),
            )
            st.plotly_chart(fig)
        except UnboundLocalError as e:
            st.write("No data available to display.")

    # Dashboard Page
    if st.session_state.selected_page == "Dashboard":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            status_list = ['None', 'Dropout', 'Not Dropout']
            selected_status = st.selectbox('Select status', (status_list), key='initial_status')
            if selected_status == 'Dropout':
                selected_status = 0
            elif selected_status == 'Not Dropout':
                st.session_state['split_columns'] = True
                status_list = ['None', 'Enrolled', 'Graduated']
                selected_status = st.selectbox('Select type of Not Dropout', (status_list), key='not_dropout_type')
                if selected_status == 'None':
                    selected_status = 'Not Dropout'
                if selected_status == 'Enrolled':
                    selected_status = 1
                if selected_status == 'Graduated':
                    selected_status = 2
                kelas_selected_status = data[data.Status == selected_status]

        with col2:
            course_list = list(data.Course_Label.unique())[::-1]
            course_list.sort()
            course_list.insert(0, "None")
            selected_course = st.selectbox('Select course', (course_list), key='course_select')
            kelas_selected_course = data[data.Course_Label == selected_course]

        with col3:
            time_list = ['None', 'Daytime', 'Evening']
            selected_time = st.selectbox('Select attendance time', (time_list), key='time_select')
            kelas_selected_time = data[data.Daytime_evening_attendance == selected_time]
            if selected_time == 'Daytime':
                selected_time = 1
            elif selected_time == 'Evening':
                selected_time = 0

        with col4:
            gender_list = ['None', 'Male', 'Female']
            selected_gender = st.selectbox('Select gender', (gender_list), key='gender_select')
            kelas_selected_gender = data[data.Gender == selected_gender]
            if selected_gender == 'Male':
                selected_gender = 1
            elif selected_gender == 'Female':
                selected_gender = 0

        if selected_status == 'None':
            kelas = data
        elif selected_status == 'Not Dropout':
            kelas = data.loc[data['Status'] == 1]
        else:
            kelas = data.loc[data['Status'] == selected_status]

        if selected_course == "None":
            kelas = kelas
        else:
            kelas = kelas.loc[kelas['Course_Label'] == selected_course]

        if selected_time == "None":
            kelas = kelas
        else:
            kelas = kelas.loc[kelas['Daytime_evening_attendance'] == selected_time]

        if selected_gender == "None":
            kelas = kelas
        else:
            kelas = kelas.loc[kelas['Gender'] == selected_gender]

        st.title('Student Performance Dashboard')

        containerA = st.container(border=True)
        containerB = st.container(border=True)

        colDr, colSt = st.columns([1, 2])

        with containerA:
            with colDr:
                dropout_rate = str(round((kelas['Status_0'].sum() / (kelas['Status_0'].sum() + kelas['Status_1'].sum() + kelas['Status_2'].sum())) * 100, 3)) + "%"
                enrolled_rate = str(round((kelas['Status_1'].sum() / (kelas['Status_0'].sum() + kelas['Status_1'].sum() + kelas['Status_2'].sum())) * 100, 3)) + "%"
                graduation_rate = str(round((kelas['Status_2'].sum() / (kelas['Status_0'].sum() + kelas['Status_1'].sum() + kelas['Status_2'].sum())) * 100, 3)) + "%"
                st.markdown(add_rating(f"<b>Dropout Rate</b><br>{dropout_rate}"), unsafe_allow_html=True)

        with containerB:   
            with colSt:
                data_total = kelas['Status_0'].sum() + kelas['Status_1'].sum() + kelas['Status_2'].sum()
                st.markdown(add_card(f"<b>Total students</b><br>{data_total}"), unsafe_allow_html=True)

                col1, col2, col3 = st.columns(3)

                with col1:
                    data_do = kelas['Status_0'].sum()
                    st.markdown(add_card(f"<b>Dropped out student</b><br>{data_do}"), unsafe_allow_html=True)

                with col2:
                    data_enrolled = kelas['Status_1'].sum()
                    st.markdown(add_card(f"<b>Enrolled student</b><br>{data_enrolled}"), unsafe_allow_html=True)

                with col3:
                    data_graduated = kelas['Status_2'].sum()
                    st.markdown(add_card(f"<b>Graduated student</b><br>{data_graduated}"), unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        if selected_status == "None":
            grouper = "Status"
        elif selected_status == 'Not Dropout':
            grouper = "Status_New"
        else:
            grouper = "Status_" + str(selected_status)

        with col1:
            st.subheader('Scholarship Holder by Status')
            
            a = kelas.groupby(grouper)['Scholarship_holder'].sum()

            try:
                maxA = a.idxmax()
                colors = ['#666666' if b != maxA else '#ffffff' for b in a.index]
                bars = go.Bar(x=a.index, y=a, marker=dict(color=colors, line=dict(color='#ffffff', width=1)), text=a, textposition='auto')

                layout = {
                    'xaxis': {'title': 'Status', 'tickfont': {'color': '#ffffff'}, 'color': '#ffffff', 'showline': True, 'linecolor': '#ffffff', 'linewidth': 1},
                    'yaxis': {'title': 'Number of Student', 'tickfont': {'color': '#ffffff'}, 'color': '#ffffff', 'showline': True, 'linecolor': '#ffffff', 'linewidth': 1},
                    'plot_bgcolor': '#000000',
                    'paper_bgcolor': '#000000',
                    'font': {'color': '#ffffff'},
                    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40},
                    'xaxis_showline': True,
                    'yaxis_showline': True
                }
                fig = go.Figure(data=[bars], layout=layout)

                if grouper == 'Status':
                    fig.update_xaxes(tickvals=a.index, ticktext=['Dropout', 'Enrolled', 'Graduated'], tickangle=0)

                st.plotly_chart(fig)
            
            except ValueError as e:
                st.write("No data available to display.")

        with col2:
            st.subheader('Average Grade per Semester')

            try:
                avg_1st_sem = kelas.groupby(grouper)['Curricular_units_1st_sem_grade'].mean()
                avg_2nd_sem = kelas.groupby(grouper)['Curricular_units_2nd_sem_grade'].mean()

                diff = avg_2nd_sem - avg_1st_sem
                percentage_diff = (diff / (avg_1st_sem + avg_2nd_sem)) * 100

                bars_1st_sem = go.Bar(
                    x=avg_1st_sem.index, 
                    y=avg_1st_sem, 
                    name='1st Semester',
                    marker=dict(color='#666666', line=dict(color='#ffffff', width=1)),
                    text=[f"{value:.2f}" for value in avg_1st_sem],
                    textposition='auto'
                )

                bars_2nd_sem = go.Bar(
                    x=avg_2nd_sem.index, 
                    y=avg_2nd_sem, 
                    name='2nd Semester',
                    marker=dict(color='#ffffff', line=dict(color='#ffffff', width=1)),
                    text=[f"{value:.2f}" for value in avg_2nd_sem],
                    textposition='auto'
                )

                layout = {
                    'xaxis': {
                        'title': 'Status', 
                        'tickfont': {'color': '#ffffff'}, 
                        'color': '#ffffff', 
                        'showline': True, 
                        'linecolor': '#ffffff', 
                        'linewidth': 1
                    },
                    'yaxis': {
                        'title': 'Average Grade', 
                        'tickfont': {'color': '#ffffff'}, 
                        'color': '#ffffff', 
                        'showline': True, 
                        'linecolor': '#ffffff', 
                        'linewidth': 1
                    },
                    'plot_bgcolor': '#000000',
                    'paper_bgcolor': '#000000',
                    'font': {'color': '#ffffff'},
                    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40},
                    'xaxis_showline': True,
                    'yaxis_showline': True,
                    'barmode': 'group'
                }

                fig_semesters = go.Figure(data=[bars_1st_sem, bars_2nd_sem], layout=layout)

                for i, status in enumerate(avg_1st_sem.index):
                    fig_semesters.add_annotation(
                        x=status,
                        y=max(avg_1st_sem[status], avg_2nd_sem[status]) + 2,
                        text=f"Difference: {diff[status]:.2f} ({percentage_diff[status]:.2f}%)",
                        showarrow=False,
                        font=dict(color="#ffffff"),
                        align='center'
                    )

                if grouper == 'Status':
                    fig_semesters.update_xaxes(tickvals=avg_1st_sem.index, ticktext=['Dropout', 'Enrolled', 'Graduated'], tickangle=0)

                st.plotly_chart(fig_semesters)
            
            except ValueError as e:
                st.write("No data available to display.")

        container = st.container(border=True)
        col1, col2 = st.columns([4, 1])
        with container:
            with col1:
                st.subheader("Dropout Rate by Course")

                course_kls = kelas

                course_kls['Course'] = course_kls['Course'].map(category_mapping)

                data_do = course_kls[course_kls['Status_0'] == 1]
                data_notdo = course_kls.loc[course_kls['Status'] > 0]

                course_do = data_do.groupby('Course')['Status_0'].sum()
                course_notdo = data_notdo.groupby('Course')['Status'].sum()

                try:
                    total_course = round((course_do / (course_do + course_notdo) * 100), 2)
                    a_sorted = total_course.sort_values()
                    maxA = a_sorted.idxmax()

                    fig = px.bar(
                        x=a_sorted.values, 
                        y=a_sorted.index,
                        labels={'y': 'Course', 'x': 'Dropout Rate (%)'},
                        text=[f"{value}%" for value in a_sorted.values],
                        color=a_sorted.index,
                        color_discrete_sequence=['#666666' if b != maxA else '#ffffff' for b in a_sorted.index],
                        height=600
                    )
                    
                    fig.update_traces(
                        textposition='outside',
                    )

                    fig.update_layout(
                        plot_bgcolor='#000000',
                        paper_bgcolor='#000000',
                        font=dict(color='#ffffff'),
                        xaxis=dict(tickfont=dict(color='#ffffff'), linecolor='#ffffff'),
                        yaxis=dict(tickfont=dict(color='#ffffff'), linecolor='#ffffff'),
                        showlegend=False
                    )

                    st.plotly_chart(fig)

                except ValueError as e:
                    st.write("No data available to display.")

            with col2:
                create_pie_chart('Educational_special_needs', 'Educational Special Needs <br>Distribution')
                create_pie_chart('Debtor', 'Debtor Distribution')
                create_pie_chart('Tuition_fees_up_to_date', 'Tuition Fees Up to Date<br>Distribution')

        container = st.container(border=True)
        colors = ['#ffffff', '#666666']
        with container:
            colA, colB = st.columns([4, 1])
            with colA:
                try:
                    fig = px.histogram(
                        kelas,
                        x='Age_at_enrollment',
                        title='Age at Enrollment Distribution',
                        color_discrete_sequence=colors
                    )
                    
                    fig.update_layout(
                        title=dict(
                            text='Age at Enrollment Distribution',
                            font=dict(size=24, color='#ffffff')
                        ),
                        plot_bgcolor='#000000',
                        paper_bgcolor='#000000',
                        font=dict(color='#ffffff'),
                        xaxis=dict(tickfont=dict(color='#ffffff'), linecolor='#ffffff'),
                        yaxis=dict(tickfont=dict(color='#ffffff'), linecolor='#ffffff')
                    )
                    
                    st.plotly_chart(fig)

                except ValueError as e:
                    st.write("No data available to display.")

            with colB:
                max_age = kelas['Age_at_enrollment'].max()
                mean_age = kelas['Age_at_enrollment'].mean()
                min_age = kelas['Age_at_enrollment'].min()
                st.markdown(add_card(f"<b>Minimum age</b><br>{min_age}"), unsafe_allow_html=True)
                st.markdown(add_card(f"<b>Average age</b><br>{mean_age:.1f}"), unsafe_allow_html=True)
                st.markdown(add_card(f"<b>Maximum age</b><br>{max_age}"), unsafe_allow_html=True)

    # Prediction Page
    if st.session_state.selected_page == "Prediction":
        st.subheader("Prediction")
        course_list = list(data.Course_Label.unique())[::-1]
        course_list.sort()

        if 'pred_selected' not in st.session_state:
            st.session_state.pred_selected = None

        if st.session_state.pred_selected is None:
            course_selected = st.selectbox('Course', ['None', *course_list], key='pred_course_select')
        else:
            course_selected = st.selectbox('Course', course_list, key='pred_course_select_alt')

        if course_selected == 'None':
            st.error("Please select a valid course.")
        else:
            st.session_state.pred_selected = course_selected

        reverse_mapping = {v: k for k, v in category_mapping.items()}

        if course_selected != 'None':
            course_selected = reverse_mapping[course_selected]

        if course_selected in [9991, 8014]:
            time_selected = 0
        else:
            time_selected = 1

        roll_number = st.text_input("Student Roll Number", value="", key="roll_number_input")

        admgrade_selected = st.number_input("Admission grade", value=50.0, step=0.1, min_value=50.0, max_value=100.0, key="adm_grade_input")
        admgrade_selected = round(admgrade_selected, 1)

        gender_selected = st.selectbox('Gender', ['Male', 'Female'], key="gender_input")
        if gender_selected == "Female":
            gender_selected = 0
        elif gender_selected == "Male":
            gender_selected = 1

        bool1, bool2 = st.columns(2)
        with bool1:
            special_list = ['Yes', 'No']
            special_selected = st.radio('Special education needs?', (special_list), key="special_needs_input")
            if special_selected == "No":
                special_selected = 0
            elif special_selected == "Yes":
                special_selected = 1

        with bool2:
            debtor_list = ['Yes', 'No']
            debtor_selected = st.radio('Debtor?', (debtor_list), key="debtor_input")
            if debtor_selected == "No":
                debtor_selected = 0
            elif debtor_selected == "Yes":
                debtor_selected = 1

        attendance_mapping = {
            0: '75–100%',
            1: '65–75%',
            2: '41–65%',
            3: 'Below 40%'
        }
        attendance_input = st.radio(
            "Select Attendance Range:",
            options=list(attendance_mapping.keys()),
            format_func=lambda x: attendance_mapping[x],
            key="attendance_input"
        )
        attendance_selected = attendance_input

        bool3, bool4 = st.columns(2)
        with bool3:
            tuition_list = ['Yes', 'No']
            tuition_selected = st.radio('Tuition up to date?', (tuition_list), key="tuition_input")
            if tuition_selected == "No":
                tuition_selected = 0
            elif tuition_selected == "Yes":
                tuition_selected = 1

        with bool4:
            scholarship_list = ['Yes', 'No']
            scholarship_selected = st.radio('Scholarship holder?', (scholarship_list), key="scholarship_input")
            if scholarship_selected == "No":
                scholarship_selected = 0
            elif scholarship_selected == "Yes":
                scholarship_selected = 1

        grade1, grade2 = st.columns(2)
        with grade1:   
            grade1_selected = st.number_input("First year credits", value=0, step=1, min_value=0, max_value=40, key="grade1_input")
            grade1_selected = round(grade1_selected, 2)
        
        with grade2:
            grade2_selected = st.number_input("Second year credits", value=0, step=1, min_value=0, max_value=40, key="grade2_input")
            grade2_selected = round(grade2_selected, 2)

        st.markdown('<style>div.stButton > button {margin: 0 auto; display: block; background: #4CAF50; color: white;}</style>', unsafe_allow_html=True)
        button_predict = st.button("Predict", key='predict_button')
        if button_predict:
            if course_selected == "None":
                st.write("Please select a valid course.")
            elif not roll_number:
                st.write("Please enter a Student Roll Number.")
            else:
                # Check if model and scaler files exist
                try:
                    model = load('student_model.pkl')
                    scaler = load('scaler.pkl')
                except FileNotFoundError:
                    st.error("Error: 'student_model.pkl' or 'scaler.pkl' file not found. Please ensure these files exist in the same directory as app.py.")
                    st.stop()

                # Preprocess inputs to match training
                attendance_weighted = 4 - attendance_selected

                user_data = {
                    'Course': [course_selected],
                    'Daytime_evening_attendance': [time_selected],
                    'Admission_grade': [admgrade_selected],
                    'Educational_special_needs': [special_selected],
                    'Debtor': [debtor_selected],
                    'Tuition_fees_up_to_date': [tuition_selected],
                    'Gender': [gender_selected],
                    'Scholarship_holder': [scholarship_selected],
                    'Curricular_units_1st_sem_grade': [grade1_selected],
                    'Curricular_units_2nd_sem_grade': [grade2_selected],
                    'attendance_weighted': [attendance_weighted]
                }

                X_new = pd.DataFrame(user_data)
                numerical_features = ['Admission_grade', 'Curricular_units_1st_sem_grade', 'Curricular_units_2nd_sem_grade', 'attendance_weighted']
                X_new[numerical_features] = scaler.transform(X_new[numerical_features])

                # Calculate dropout percentage and prediction
                predictions = model.predict(X_new)

                # Rule: If attendance is below 50% (attendance_selected == 3), force dropout
                if attendance_selected == 3:
                    predictions[0] = 0  # Force dropout status
                    dropout_prob = 100.0  # Set dropout probability to 100%
                else:
                    # Heuristic dropout percentage calculation
                    dropout_score = 0
                    avg_credits = (grade1_selected + grade2_selected) / 2

                    # Attendance contribution
                    if attendance_selected == 2:
                        dropout_score += 20
                    elif attendance_selected == 1:
                        dropout_score += 10

                    # Credits contribution (linear scale, max 40 points)
                    credits_score = ((40 - avg_credits) / 40) * 40
                    dropout_score += credits_score

                    # Other factors
                    if debtor_selected == 1 and scholarship_selected == 0:
                        dropout_score += 15

                    if admgrade_selected < 100:
                        adm_grade_score = ((100 - admgrade_selected) / 100) * 15
                        dropout_score += adm_grade_score

                    if special_selected == 1:
                        dropout_score += 5

                    if tuition_selected == 0:
                        dropout_score += 5

                    dropout_prob = min(100, max(0, dropout_score))

                # Map predictions to meaningful labels with roll number
                status_mapping = {
                    0: f"Student with roll number {roll_number} is likely to dropout.",
                    1: f"Student with roll number {roll_number} is likely to be not dropout.",
                    2: f"Student with roll number {roll_number} is likely to graduate."
                }
                prediction_text = status_mapping.get(predictions[0], "Unknown status")

                # Store the prediction results in session state
                st.session_state.prediction_result = {
                    "prediction_text": prediction_text,
                    "dropout_prob": dropout_prob,
                    "attendance_selected": attendance_selected
                }

                # Navigate to the Prediction Result page
                st.session_state.selected_page = "Prediction Result"
                st.rerun()

    # Prediction Result Page
    if st.session_state.selected_page == "Prediction Result":
        st.title("Prediction Result")
        if st.session_state.prediction_result is None:
            st.warning("No prediction result available. Please make a prediction first.")
        else:
            result = st.session_state.prediction_result
            st.write(result["prediction_text"])
            st.warning(f"Dropout Chance: This student has a **{result['dropout_prob']:.1f}%** chance of dropping out.")
            st.progress(int(result["dropout_prob"]))
            if result["attendance_selected"] == 3:
                st.error("Warning: Attendance below 40% automatically classifies the student as likely to dropout.")

            # Add a button to go back to the Prediction page
            if st.button("Make Another Prediction"):
                st.session_state.prediction_result = None
                st.session_state.selected_page = "Prediction"
                st.rerun()