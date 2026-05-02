import streamlit as st
import cv2
import pandas as pd
from datetime import datetime
import os
from faceBlink import recognize_face

# ---------------- BACKGROUND ----------------
def set_bg():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1523580846011-d3a5bc25702b");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# ---------------- SAFE CSV LOADER ----------------
def load_attendance():
    file = "attendance.csv"

    if not os.path.exists(file):
        df = pd.DataFrame(columns=["Name", "Date", "Time", "Subject"])
        df.to_csv(file, index=False)
        return df

    df = pd.read_csv(file)

    # 🔥 Fix old file (missing Subject column)
    if "Subject" not in df.columns:
        df["Subject"] = "Unknown"

    return df

# ---------------- SAVE CSV ----------------
def save_attendance(df):
    try:
        df.to_csv("attendance.csv", index=False)
    except PermissionError:
        st.error("❌ Close attendance.csv file and try again")

# ---------------- MARK ATTENDANCE ----------------
def mark_attendance(name, subject):
    df = load_attendance()

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%I:%M:%S %p")

    if not ((df["Name"] == name) &
            (df["Date"] == date) &
            (df["Subject"] == subject)).any():

        new_row = pd.DataFrame([[name, date, time, subject]],
                               columns=["Name", "Date", "Time", "Subject"])

        df = pd.concat([df, new_row], ignore_index=True)
        save_attendance(df)

        st.success(f"✅ {name} marked for {subject}")

    else:
        st.info(f"ℹ️ {name} already marked for {subject}")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Dashboard")
option = st.sidebar.radio(
    "Select Option",
    ["Home", "Start Attendance", "Student List", "View Attendance"]
)

# ---------------- HOME ----------------
if option == "Home":
    st.title("🎓 AI Attendance System")
    st.subheader("Face Recognition with Anti-Spoofing")

# ---------------- START ATTENDANCE ----------------
elif option == "Start Attendance":
    st.title("📸 Live Attendance")

    # ✅ SUBJECT DROPDOWN
    subject = st.selectbox(
        "📘 Select Current Period",
        [
            "Digital Image Processing",
            "Artificial Intelligence and Machine Learning",
            "Operating System",
            "Big Data Analytics"
        ]
    )

    st.warning("⚠️ Please blink your eyes")

    if "run_camera" not in st.session_state:
        st.session_state.run_camera = False

    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ Start Camera"):
            st.session_state.run_camera = True

    with col2:
        if st.button("⏹️ Stop Camera"):
            st.session_state.run_camera = False

    FRAME_WINDOW = st.empty()
    status_text = st.empty()

    if st.session_state.run_camera:
        cap = cv2.VideoCapture(0)
        marked_names = set()

        while st.session_state.run_camera:
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Camera not working")
                break

            results = recognize_face(frame)

            for (top, right, bottom, left, name) in results:

                if name not in ["Unknown", "Fake/No Blink"]:
                    status_text.success(f"✅ Detected: {name}")

                    if name not in marked_names:
                        mark_attendance(name, subject)
                        marked_names.add(name)

                else:
                    status_text.warning(f"⚠️ {name}")

                color = (0, 255, 0) if name not in ["Unknown", "Fake/No Blink"] else (0, 0, 255)

                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                cv2.putText(frame, name, (left, top-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(frame)

        cap.release()
        FRAME_WINDOW.empty()
        st.info("📷 Camera Stopped")

# ---------------- STUDENT LIST ----------------
elif option == "Student List":
    st.markdown("<h2 style='text-align:center;'>📋 Students List</h2>", unsafe_allow_html=True)

    dataset_path = "dataset"

    if os.path.exists(dataset_path):

        students = os.listdir(dataset_path)

        if len(students) == 0:
            st.warning("⚠️ No students found")
        else:
            data = []

            # 🔥 Extract Name + Reg No
            for s in students:
                if "_" in s:
                    name, reg = s.rsplit("_", 1)
                else:
                    name = s
                    reg = "N/A"

                data.append([name, reg])

            df = pd.DataFrame(data, columns=["Student Name", "Register No"])

            # 🔍 Search
            search = st.text_input("🔍 Search Student")
            if search:
                df = df[
                    df["Student Name"].str.contains(search, case=False) |
                    df["Register No"].str.contains(search, case=False)
                ]

            # 🔥 SORT BY REGISTER NO (ASCENDING)
            df_valid = df[df["Register No"] != "N/A"].sort_values(by="Register No")
            df_na = df[df["Register No"] == "N/A"]

            df = pd.concat([df_valid, df_na])

            # 🔥 RESET INDEX + ADD SERIAL NUMBER
            df = df.reset_index(drop=True)
            df.insert(0, "S.No", range(1, len(df) + 1))

            st.markdown(f"**Total Students: {len(df)}**")

            # 🎨 STYLE TABLE
            styled_df = df.style.set_properties(**{
                'font-size': '22px',
                'text-align': 'left'
            }).set_table_styles([
                {'selector': 'th',
                 'props': [('font-size', '20px'),
                           ('background-color', '#f0f2f6')]},
                {'selector': 'td',
                 'props': [('padding', '10px')]}
            ])

            # ✅ DISPLAY WITHOUT EXTRA INDEX COLUMN
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

    else:
        st.error("❌ Dataset folder not found")

# ---------------- VIEW ATTENDANCE ----------------
elif option == "View Attendance":
    st.title("📊 Attendance")

    df = load_attendance()  # 🔥 SAFE LOAD (fixes missing Subject)

    # 🔍 Search
    search = st.text_input("🔍 Search by Name")
    if search:
        df = df[df["Name"].str.contains(search, case=False)]

    # 📅 Filter by date
    date_filter = st.date_input("📅 Select Date")
    if date_filter:
        df = df[df["Date"] == str(date_filter)]

    # 📊 Count
    st.metric("Total Records", len(df))

    # 🔥 SAFE SORT (no crash now)
    df = df.sort_values(by=["Date", "Subject"])

    st.dataframe(df)

    # 📥 Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", csv, "attendance.csv")