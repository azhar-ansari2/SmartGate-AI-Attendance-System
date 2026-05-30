import streamlit as st
import json, os
 
SETTINGS_FILE = "data/settings.json"
 
DEFAULT_SETTINGS = {
    "company_name": "Infosys Limited",
    "gate_name": "Main Gate — Block A",
    "face_confidence_threshold": 75.0,
    "voice_confidence_threshold": 70.0,
    "require_voice_verification": True,
    "audio_announcements": True,
    "working_hours_start": "08:00",
    "working_hours_end": "19:00",
    "late_threshold": "09:30",
}
 
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()
 
def save_settings(s):
    os.makedirs("data", exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(s, f, indent=2)
 
 
def show():
    st.markdown('<div class="main-title">⚙️ Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Configure the SmartGate system</div>', unsafe_allow_html=True)
 
    s = load_settings()
 
    tab1, tab2, tab3 = st.tabs(["🏢 Company", "🔐 Verification", "🔊 Audio"])
 
    with tab1:
        s["company_name"] = st.text_input("Company Name", s["company_name"])
        s["gate_name"] = st.text_input("Gate / Location Name", s["gate_name"])
        s["working_hours_start"] = st.text_input("Working Hours Start", s["working_hours_start"])
        s["working_hours_end"] = st.text_input("Working Hours End", s["working_hours_end"])
        s["late_threshold"] = st.text_input("Late Arrival Threshold", s["late_threshold"])
 
    with tab2:
        s["face_confidence_threshold"] = st.slider(
            "Face Recognition Confidence Threshold (%)",
            50.0, 99.0, s["face_confidence_threshold"], 0.5
        )
        s["voice_confidence_threshold"] = st.slider(
            "Voice Gender Confidence Threshold (%)",
            50.0, 99.0, s["voice_confidence_threshold"], 0.5
        )
        s["require_voice_verification"] = st.toggle(
            "Require Voice Verification", s["require_voice_verification"]
        )
 
    with tab3:
        s["audio_announcements"] = st.toggle(
            "Enable Audio Announcements", s["audio_announcements"]
        )
        st.info("Audio uses pyttsx3 (offline) for announcements like 'Welcome Azhar, Access Granted'")
 
    st.markdown("---")
    if st.button("💾 Save Settings"):
        save_settings(s)
        st.success("✅ Settings saved!")