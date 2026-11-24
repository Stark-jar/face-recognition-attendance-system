# AI-Based Face Recognition Attendance Management System

An intelligent attendance management system developed using **Python, OpenCV, and Streamlit** that automates student attendance through real-time face recognition and blink-based anti-spoofing technology.

The system reduces manual attendance work, prevents proxy attendance, and provides an interactive dashboard for managing students and monitoring attendance records.

## 🚀 Features

- **Face Recognition:** Identifies registered students using facial recognition and face encodings.
- **Anti-Spoofing Detection:** Uses eye-blink detection and Eye Aspect Ratio (EAR) to distinguish live faces from static photographs.
- **Student Registration:** Captures multiple facial images from different angles (front, left, and right).
- **Admin Dashboard:** Provides an interface for managing students, approving registrations, and monitoring attendance.
- **Automated Attendance:** Records student attendance with date and subject details while preventing duplicate entries.
- **Attendance Reports:** Generates attendance reports with Excel and CSV export functionality.
- **Accuracy Evaluation:** Includes face recognition testing and performance evaluation.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| OpenCV | Image processing and face detection |
| Dlib | Facial landmark detection |
| Face Recognition | Face encoding and matching |
| Streamlit | Interactive web interface |
| NumPy | Numerical operations |
| Pandas | Attendance data processing |
| Excel / CSV | Attendance report generation |

## 🧠 Working Methodology

1. **Student Registration:** Captures facial images of students from multiple angles.
2. **Face Encoding:** Extracts unique facial features and generates face encodings.
3. **Face Recognition:** Compares real-time camera input with stored facial encodings.
4. **Blink Detection:** Uses 68 facial landmarks and Eye Aspect Ratio (EAR) to detect eye blinking.
5. **Attendance Recording:** Marks attendance after successful face recognition and live-face verification.
6. **Report Generation:** Stores attendance records and generates downloadable reports.

## 📂 Project Modules

- `app.py` – Main application interface.
- `Student_Reg.py` – Student registration module.
- `admin.py` – Admin dashboard and management.
- `faceBlink.py` – Eye-blink detection and anti-spoofing.
- `encodings.pkl` – Stores generated facial encodings.

*Note: The filenames above represent the main modules; your actual project may contain additional supporting files.*

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AI-Face-Recognition-Attendance.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Face-Recognition-Attendance
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install opencv-python streamlit numpy pandas openpyxl
```

Install the additional face-recognition and Dlib dependencies required by your environment.

### 5. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser.

## 📊 Project Performance

- Achieved approximately **89.22% face recognition accuracy** during the project evaluation on a dataset of 30 images per student.
- Implemented blink-based anti-spoofing to improve attendance authenticity.
- Supports multiple student registrations and subject-wise attendance management.

*Performance may vary depending on lighting conditions, camera quality, facial angles, and dataset quality.*

## 🎯 Applications

- Schools and Colleges
- Universities and Educational Institutions
- Computer Training Institutes
- Corporate Offices
- Employee Attendance Management

## 🔮 Future Enhancements

- Cloud-based attendance storage.
- Mobile application integration.
- Advanced anti-spoofing using deep learning.
- Real-time attendance analytics.
- Integration with institutional management systems.

## 👨‍💻 Developed By

**Abhishek Choulager**

MSc Computer Science

Rani Channamma University, Belagavi

**Project Title:** AI-Based Face Recognition Attendance Management System with Anti-Spoofing and Analytics.

---

⭐ If you find this project useful, consider giving this repository a star!
