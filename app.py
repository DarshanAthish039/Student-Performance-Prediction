import streamlit as st
import pandas as pd
import joblib


st.set_page_config(
    page_title="Student Performance AI",
    page_icon="🎓",
    layout="wide"
)


model = joblib.load("models/student_model.pkl")

def generate_recommendations(
    attendance,
    study_hours,
    previous_marks,
    assignments,
    prediction
):

    recommendations = []
    strengths = []
    risk_factors = []



    if attendance < 60:
        risk_factors.append(
            "Very low attendance"
        )

        recommendations.append(
            "Improve attendance immediately. "
            "Target at least 75% attendance."
        )

    elif attendance < 75:
        risk_factors.append(
            "Attendance below recommended level"
        )

        recommendations.append(
            "Increase attendance and maintain at least "
            "75–85% regular attendance."
        )

    else:
        strengths.append(
            "Good attendance"
        )


    if study_hours < 2:

        risk_factors.append(
            "Low daily study time"
        )

        recommendations.append(
            "Increase study time gradually to "
            "at least 3–4 hours per day."
        )

    elif study_hours < 4:

        recommendations.append(
            "Try increasing daily study time to "
            "4–5 focused hours."
        )

    else:

        strengths.append(
            "Good study routine"
        )



    if previous_marks < 50:

        risk_factors.append(
            "Low previous academic performance"
        )

        recommendations.append(
            "Revise fundamental concepts and "
            "practice previous examination questions."
        )

    elif previous_marks < 70:

        recommendations.append(
            "Focus on weak subjects and solve "
            "additional practice problems."
        )

    else:

        strengths.append(
            "Strong previous academic performance"
        )

 
    if assignments < 60:

        risk_factors.append(
            "Low assignment performance"
        )

        recommendations.append(
            "Complete assignments regularly and "
            "review mistakes before submission."
        )

    elif assignments < 75:

        recommendations.append(
            "Improve assignment quality and "
            "submit work consistently."
        )

    else:

        strengths.append(
            "Good assignment performance"
        )


    if prediction < 50:

        risk_level = "HIGH"

        recommendations.append(
            "Create a structured weekly study plan "
            "and seek additional academic support."
        )

    elif prediction < 70:

        risk_level = "MEDIUM"

        recommendations.append(
            "Focus on weak areas and maintain "
            "consistent weekly revision."
        )

    else:

        risk_level = "LOW"

        recommendations.append(
            "Maintain your current study habits "
            "and continue regular revision."
        )

    return (
        risk_level,
        strengths,
        risk_factors,
        recommendations
    )

st.markdown("""
<style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: gray;
        margin-bottom: 30px;
    }

    .card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f5f5;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


st.sidebar.title("🎓 Student AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Student Prediction",
        "📈 Analytics"
    ]
)



if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">🎓 Student Performance AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'AI-powered academic performance prediction and analytics system'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
        <h3>🤖 ML Prediction</h3>
        <p>Predict student final scores using machine learning.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
        <h3>📊 Analytics</h3>
        <p>Analyze attendance, study hours and academic performance.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
        <h3>🎯 Recommendations</h3>
        <p>Identify students who need academic improvement.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("About the Project")

    st.write("""
    This system predicts student academic performance using:

    - Attendance percentage
    - Study hours
    - Previous examination marks
    - Assignment scores

    The system uses a Machine Learning model trained using
    historical student performance data.
    """)



elif page == "📊 Student Prediction":

    st.title("📊 Student Performance Prediction")

    st.write("Enter the student's academic information.")

    col1, col2 = st.columns(2)

    with col1:

        attendance = st.slider(
            "Attendance (%)",
            min_value=0,
            max_value=100,
            value=80
        )

        study_hours = st.slider(
            "Study Hours per Day",
            min_value=0,
            max_value=12,
            value=4
        )

    with col2:

        previous_marks = st.slider(
            "Previous Marks (%)",
            min_value=0,
            max_value=100,
            value=75
        )

        assignments = st.slider(
            "Assignment Score (%)",
            min_value=0,
            max_value=100,
            value=80
        )

    st.divider()

    if st.button(
        "🔮 Predict Student Performance",
        use_container_width=True
    ):

        input_data = pd.DataFrame({
            "Attendance": [attendance],
            "Study_Hours": [study_hours],
            "Previous_Marks": [previous_marks],
            "Assignments": [assignments]
        })

        prediction = model.predict(input_data)[0]

        prediction = max(0, min(100, prediction))

        st.subheader("Prediction Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Predicted Final Score",
                f"{prediction:.2f}%"
            )

        with col2:

            if prediction >= 85:
                performance = "Excellent ⭐"
                st.success(performance)

            elif prediction >= 70:
                performance = "Good 👍"
                st.info(performance)

            elif prediction >= 50:
                performance = "Average 📚"
                st.warning(performance)

            else:
                performance = "Needs Improvement ⚠️"
                st.error(performance)

        st.progress(int(prediction))

        st.subheader("🎯 Academic Recommendation")

        if attendance < 75:
            st.warning(
                "Improve attendance. Try to maintain at least 75–85% attendance."
            )

        if study_hours < 3:
            st.warning(
                "Increase daily study time to at least 3–4 hours."
            )

        if previous_marks < 60:
            st.warning(
                "Focus on improving fundamental concepts from previous subjects."
            )

        if assignments < 70:
            st.warning(
                "Complete assignments regularly to improve academic performance."
            )

        if (
            attendance >= 75
            and study_hours >= 3
            and previous_marks >= 60
            and assignments >= 70
        ):
            st.success(
                "Good academic habits! Continue maintaining your current performance."
            )

elif page == "📈 Analytics":

    import matplotlib.pyplot as plt
    import seaborn as sns

    st.title("📈 Student Performance Analytics")

    # Load dataset
    data = pd.read_csv("dataset/student_data.csv")



    st.subheader("📋 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", len(data))

    with col2:
        st.metric(
            "Average Attendance",
            f"{data['Attendance'].mean():.1f}%"
        )

    with col3:
        st.metric(
            "Average Study Hours",
            f"{data['Study_Hours'].mean():.1f}"
        )

    with col4:
        st.metric(
            "Average Final Score",
            f"{data['Final_Score'].mean():.1f}%"
        )

    st.divider()

    st.subheader("📊 Student Dataset")

    st.dataframe(
        data,
        use_container_width=True
    )

    st.divider()

  

    st.subheader("🤖 Machine Learning Model Comparison")

    comparison_file = "models/model_comparison.csv"

    try:

        results = pd.read_csv(comparison_file)

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        # Find best model
        best_row = results.loc[
            results["R2_Score"].idxmax()
        ]

        best_model_name = best_row["Model"]
        best_r2 = best_row["R2_Score"]

        st.success(
            f"🏆 Best Model: {best_model_name} | "
            f"R² Score: {best_r2:.3f}"
        )

      

        st.subheader("📈 R² Score Comparison")

        chart_data = results.set_index("Model")["R2_Score"]

        st.bar_chart(chart_data)

    except FileNotFoundError:

        st.warning(
            "Model comparison file not found. "
            "Run 'python train.py' first."
        )

    st.divider()

 

    st.subheader("🔥 Feature Correlation")

    correlation = data[
        [
            "Attendance",
            "Study_Hours",
            "Previous_Marks",
            "Assignments",
            "Final_Score"
        ]
    ].corr()

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.heatmap(
        correlation,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        ax=ax
    )

    ax.set_title("Student Performance Correlation")

    st.pyplot(fig)

    st.divider()


    st.subheader("📚 Attendance vs Final Score")

    st.scatter_chart(
        data,
        x="Attendance",
        y="Final_Score"
    )

    st.divider()


    st.subheader("⏱️ Study Hours vs Final Score")

    st.scatter_chart(
        data,
        x="Study_Hours",
        y="Final_Score"
    )

    st.divider()



    st.subheader("📝 Previous Marks vs Final Score")

    st.scatter_chart(
        data,
        x="Previous_Marks",
        y="Final_Score"
    )

    st.divider()


    st.subheader("📑 Assignment Score vs Final Score")

    st.scatter_chart(
        data,
        x="Assignments",
        y="Final_Score"
    )

# elif page == "📈 Analytics":

#     st.title("📈 Student Performance Analytics")

#     # Load dataset
#     data = pd.read_csv("dataset/student_data.csv")

#     st.subheader("Dataset Preview")

#     st.dataframe(
#         data,
#         use_container_width=True
#     )

#     st.divider()

#     # Metrics
#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(
#             "Students",
#             len(data)
#         )

#     with col2:
#         st.metric(
#             "Average Attendance",
#             f"{data['Attendance'].mean():.1f}%"
#         )

#     with col3:
#         st.metric(
#             "Average Study Hours",
#             f"{data['Study_Hours'].mean():.1f}"
#         )

#     with col4:
#         st.metric(
#             "Average Final Score",
#             f"{data['Final_Score'].mean():.1f}%"
#         )

#     st.divider()

#     st.subheader("📊 Performance Analysis")

#     chart_data = data[
#         [
#             "Attendance",
#             "Study_Hours",
#             "Previous_Marks",
#             "Assignments",
#             "Final_Score"
#         ]
#     ]

#     st.line_chart(chart_data)

#     st.subheader("📚 Attendance vs Final Score")

#     st.scatter_chart(
#         data,
#         x="Attendance",
#         y="Final_Score"
#     )

#     st.subheader("⏱️ Study Hours vs Final Score")

#     st.scatter_chart(
#         data,
#         x="Study_Hours",
#         y="Final_Score"
#     )