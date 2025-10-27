import streamlit as st
import base64
from modules.chat_engine import ask_medgpt
from modules.eda import load_data, show_basic_info
from modules.viz import show_visualizations
from modules.prediction import train_predict
from modules.report_generator import generate_report

st.set_page_config(page_title="🩺 MedGPT - AI Healthcare Assistant", layout="wide")

# Sidebar navigation
st.sidebar.title("🩺 MedGPT Navigation")
page = st.sidebar.radio(
    "Go to:",
    [
        "💬 Chatbot",
        "📂 Data Analysis",
        "📊 Visualization",
        "🤖 Prediction",
        "💊 Medicine Identifier",
        "🧾 Prescription Assistant"
    ]
)

st.title("🩺 MedGPT - Smart Healthcare Assistant")

# ---------------- Chatbot Page ---------------- #
if page == "💬 Chatbot":
    st.write("Ask me anything about health or medical insights (educational use only).")
    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.chat_input("Type your medical question here...")
    if user_input:
        with st.spinner("Thinking..."):
            reply = ask_medgpt(user_input)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("MedGPT", reply))

    # Display chat history
    for sender, msg in st.session_state.history:
        st.chat_message("user" if sender == "You" else "assistant").markdown(msg)

    # Download Chat as PDF
    if st.button("🧾 Download Chat as PDF"):
        chat_history = "\n".join([f"{sender}: {msg}" for sender, msg in st.session_state.history])
        pdf_path = generate_report(chat_history)

        with open(pdf_path, "rb") as f:
            pdf_data = f.read()

        b64 = base64.b64encode(pdf_data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="MedGPT_Chat_Report.pdf">📥 Click here to download</a>'
        st.markdown(href, unsafe_allow_html=True)

# ---------------- Data Analysis Page ---------------- #
elif page == "📂 Data Analysis":
    uploaded_file = st.file_uploader("Upload your medical dataset (CSV)", type=["csv"])
    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            show_basic_info(df)

# ---------------- Visualization Page ---------------- #
elif page == "📊 Visualization":
    uploaded_file = st.file_uploader("Upload CSV for visualization", type=["csv"])
    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            show_visualizations(df)

# ---------------- Prediction Page ---------------- #
elif page == "🤖 Prediction":
    uploaded_file = st.file_uploader("Upload CSV for prediction", type=["csv"])
    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            train_predict(df)

# ---------------- Medicine Identifier Page ---------------- #
elif page == "💊 Medicine Identifier":
    st.subheader("💊 Upload a Tablet or Medicine Image")
    uploaded_img = st.file_uploader("Upload image (JPG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_img:
        from modules.medicine_identifier import extract_text_from_image, analyze_medicine_info
        from modules.email_sender import send_medicine_email  # ✅ import email sender

        # Show uploaded image
        st.image(uploaded_img, caption="Uploaded Image", use_column_width=True)

        # Step 1: Extract text
        with st.spinner("🔍 Reading image..."):
            text = extract_text_from_image(uploaded_img)
            st.write(f"**Detected Text:** {text}")

        # Step 2: Analyze medicine
        with st.spinner("💬 Analyzing medicine info..."):
            info = analyze_medicine_info(text)
            st.success("✅ Medicine Information:")
            st.write(info)

        # Step 3: Email sending section
        st.markdown("---")
        st.subheader("📧 Send This Report to Your Email")

        user_email = st.text_input("Enter your email address:")

        if st.button("Send Email"):
            if user_email:
                # Reset file cursor and read image bytes
                uploaded_img.seek(0)
                image_bytes = uploaded_img.read()

                # Send the email using your email_sender.py
                status = send_medicine_email(
                    to_email=user_email,
                    detected_text=text,
                    description=info,
                    image_bytes=image_bytes,
                    image_filename=uploaded_img.name
                )

                if status is True:
                    st.success(f"✅ Report sent successfully to **{user_email}**")
                else:
                    st.error(status)
            else:
                st.warning("⚠️ Please enter your email address before sending.")


# ---------------- Prescription Assistant Page ---------------- #
# ---------------- Prescription Assistant Page ---------------- #
elif page == "🧾 Prescription Assistant":
    st.subheader("🧾 Describe Your Symptoms to Get an AI Prescription (Educational Only)")

    # --- Collect patient details with helpful placeholders ---
    patient_name = st.text_input("👤 Enter Patient Name:", placeholder="Please enter your full name")
    age = st.number_input("🎂 Enter Age:", min_value=0, max_value=120, step=1, help="Enter your age in years")
    gender = st.selectbox("⚧️ Select Gender:", ["Select gender", "Male", "Female", "Other"])
    symptoms = st.text_area("🩺 Describe your symptoms:", placeholder="Describe how you're feeling, e.g. headache, fever, cough, etc.")
    user_email = st.text_input("📧 Enter your email:", placeholder="example@gmail.com")

    if st.button("Generate Prescription"):
        from modules.prescription_assistant import generate_prescription
        from modules.email_sender import send_prescription

        # Combine patient info with symptoms for context
        full_description = (
            f"Patient Name: {patient_name}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n"
            f"Symptoms: {symptoms}\n"
        )

        with st.spinner("Analyzing symptoms..."):
            result = generate_prescription(full_description)
            st.success("✅ AI-generated Prescription:")
            st.write(result)

        # Combine patient info + AI result for the PDF
        full_report = (
            f"--- Patient Details ---\n"
            f"Name: {patient_name}\n"
            f"Age: {age}\n"
            f"Gender: {gender}\n\n"
            f"--- Symptoms ---\n{symptoms}\n\n"
            f"--- AI Prescription ---\n{result}\n"
        )

        # Generate PDF
        pdf_path = generate_report(full_report)

        if user_email:
            with st.spinner("📧 Sending prescription to your email..."):
                status = send_prescription(user_email, pdf_path)
                st.success(status)

    st.markdown(
        """
        ⚠️ **Disclaimer:** This prescription is AI-generated for *educational purposes only*.
        Always consult a licensed doctor before taking any medication.
        """
    )
