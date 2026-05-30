# 🏢 SmartGate — Enterprise Face & Voice Attendance System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Analytics-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

**An enterprise-grade attendance system using Face Recognition + Voice Gender Verification**

*Built for large organizations like Infosys, TCS, Wipro*

[🚀 Live Demo](#) · [📖 Docs](#how-it-works) · [🐛 Report Bug](#)

</div>

---

## 🌟 Why SmartGate?

Traditional attendance systems are slow, easy to fool (buddy punching), and generate no insights. SmartGate solves all three:

| Problem | SmartGate Solution |
|---------|-------------------|
| Buddy punching | Face recognition — only YOU can check in |
| Gender spoofing | Voice pitch analysis cross-verifies gender |
| No insights | Real-time dashboard with charts & reports |
| Manual records | Auto CSV export with timestamps |

---

## ✨ Features

- 👤 **Face Recognition** — Identify employees via webcam
- 🔊 **Voice Gender Verification** — Pitch analysis to verify gender matches face
- ✅ **Auto Attendance Marking** — One scan = attendance logged with timestamp
- 🔐 **Dual Verification Mode** — Face + Voice must both pass for access
- 📊 **Analytics Dashboard** — Daily/weekly trends, gender distribution charts
- 👥 **Employee Management** — Register, search, delete employees
- 📋 **Attendance Log** — Filter, search, export to CSV
- 🔊 **Audio Announcements** — "Welcome Azhar! Access Granted" via pyttsx3
- ⚙️ **Configurable Settings** — Confidence thresholds, working hours

---

## 🗂️ Project Structure

```
smartgate/
├── app.py                      # Main Streamlit entry point
├── requirements.txt
├── README.md
│
├── pages/
│   ├── gate.py                 # Entry gate — face + voice scan
│   ├── dashboard.py            # Analytics dashboard
│   ├── employees.py            # Employee registration & management
│   ├── attendance_log.py       # View & export attendance
│   └── settings.py             # System configuration
│
├── utils/
│   ├── face_engine.py          # Face detection, recognition, gender
│   ├── voice_engine.py         # Voice recording & gender from pitch
│   ├── attendance.py           # Attendance CRUD operations
│   └── database.py             # Employee JSON database
│
├── model/
│   ├── train.py                # Train gender classification model
│   ├── pca_model.pkl           # Saved PCA (after training)
│   └── classifier.pkl          # Saved LogisticRegression (after training)
│
└── data/                       # Auto-created at runtime
    ├── employees.json
    ├── attendance.json
    └── settings.json
```

---

## 🚀 Getting Started

### 1. Clone
```bash
git clone https://github.com/azhar-ansari2/smartgate-attendance.git
cd smartgate-attendance
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
streamlit run app.py
```
Opens at: **http://localhost:8501**

---

## 📖 How It Works

```
EMPLOYEE ARRIVES AT GATE
         ↓
📷 Webcam captures face
         ↓
🔍 Haar Cascade detects face region
         ↓
🤖 PCA + Logistic Regression → Gender classified
         ↓
🔎 Face encoding compared against registered employees
         ↓
🔊 Microphone records 3 seconds of voice
         ↓
🎵 Librosa analyzes pitch (Hz) → Voice gender
         ↓
✅ Face gender == Voice gender?
         ↓
    YES → ACCESS GRANTED + Attendance Marked
    NO  → ACCESS DENIED
         ↓
🔊 pyttsx3 announces: "Welcome [Name]. Access Granted."
```

---

## 🔐 Verification Modes

| Mode | Description |
|------|-------------|
| Face Only | Quick scan — face recognition + gender |
| Voice Only | Voice pitch analysis only |
| Face + Voice | Full dual verification — most secure |

---

## 📊 Dashboard Features

- KPI cards: Total employees, present, absent, attendance rate
- Weekly attendance bar chart
- Gender distribution pie chart
- Today's check-in timeline (scatter plot)

---

## 🏗️ How to Deploy

### Streamlit Community Cloud (Free)
1. Push to GitHub
2. Go to share.streamlit.io
3. Connect GitHub repo
4. Set main file: `app.py`
5. Deploy ✅

### Local Network (Office Use)
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```
Access from any device on same WiFi at `http://YOUR_PC_IP:8501`

---

## 👨‍💻 Author

**Md Azhar Ansari** — Data Science & AI Intern @ Infosys

- 💼 [LinkedIn](https://linkedin.com/in/md-azhar-ansari)
- 🌐 [Portfolio](https://azhar-ansari2.github.io)
- 📧 azharansari9148@gmail.com

---

## 📄 License
MIT License — free to use, modify, and deploy.

---
<div align="center">⭐ Star this repo if you found it useful!</div>
