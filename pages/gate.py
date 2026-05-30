import streamlit as st
import cv2
import numpy as np
import time
import datetime
from PIL import Image
from utils.face_engine import detect_and_recognize
from utils.voice_engine import record_and_verify_gender
from utils.attendance import mark_attendance, get_today_attendance
from utils.database import get_all_employees
 
 
def show():
    st.markdown('<div class="main-title">🚪 Entry Gate</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Face Recognition + Voice Gender Verification</div>', unsafe_allow_html=True)
 
    # Live clock
    now = datetime.datetime.now()
    col_t1, col_t2, col_t3 = st.columns(3)
    col_t1.markdown(f"""<div class="metric-card">
        <div class="metric-val">{now.strftime('%H:%M:%S')}</div>
        <div class="metric-key">Current Time</div></div>""", unsafe_allow_html=True)
    col_t2.markdown(f"""<div class="metric-card">
        <div class="metric-val">{now.strftime('%d %b')}</div>
        <div class="metric-key">Today's Date</div></div>""", unsafe_allow_html=True)
 
    today_att = get_today_attendance()
    col_t3.markdown(f"""<div class="metric-card">
        <div class="metric-val" style="color:#00ff88">{len(today_att)}</div>
        <div class="metric-key">Checked In Today</div></div>""", unsafe_allow_html=True)
 
    st.markdown("---")
 
    # Verification mode
    mode = st.radio("Verification Mode", [
        "📷 Face Only",
        "🔊 Voice Only",
        "🔐 Face + Voice (Full Verification)"
    ], horizontal=True)
 
    st.markdown("---")
 
    col1, col2 = st.columns([3, 2])
 
    with col1:
        st.markdown("### 📷 Camera Feed")
        img_input = st.camera_input("", key="gate_cam", label_visibility="collapsed")
 
        if img_input:
            # Convert to OpenCV
            file_bytes = np.asarray(bytearray(img_input.read()), dtype=np.uint8)
            frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
 
            with st.spinner("🔍 Scanning face..."):
                time.sleep(0.5)
                result = detect_and_recognize(frame)
 
            if result["face_detected"]:
                # Show annotated image
                ann_rgb = cv2.cvtColor(result["annotated_frame"], cv2.COLOR_BGR2RGB)
                st.image(ann_rgb, use_column_width=True)
            else:
                st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), use_column_width=True)
                st.warning("⚠️ No face detected. Please look directly at the camera.")
 
            # Store result in session
            st.session_state["face_result"] = result
 
    with col2:
        st.markdown("### 🔐 Verification Status")
 
        face_result = st.session_state.get("face_result", {})
 
        # ── FACE RESULT ──
        if face_result:
            if face_result.get("face_detected"):
                emp = face_result.get("employee")
                gender = face_result.get("gender", "Unknown")
                conf = face_result.get("confidence", 0)
 
                st.markdown(f"""<div class="info-box">
                    <b style='color:#c8dce8'>👤 Face Detection</b><br><br>
                    <b style='color:#00ff88'>✓ FACE DETECTED</b><br>
                    Gender: <span class="tag-{'male' if gender=='Male' else 'female'}">{gender}</span><br>
                    Confidence: <b style='color:#00d4ff'>{conf:.1f}%</b><br>
                    {"Employee: <b style='color:#00ff88'>" + emp['name'] + "</b>" if emp else "<span style='color:#ff6b35'>⚠ Unknown Person</span>"}
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="info-box">
                    <b style='color:#c8dce8'>👤 Face Detection</b><br><br>
                    <span style='color:#3a5a70'>⟳ Waiting for camera...</span>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="info-box">
                <b style='color:#c8dce8'>👤 Face Detection</b><br><br>
                <span style='color:#3a5a70'>⟳ Capture image to begin</span>
            </div>""", unsafe_allow_html=True)
 
        # ── VOICE VERIFICATION ──
        if "Voice" in mode or "Full" in mode:
            st.markdown("""<div class="info-box">
                <b style='color:#c8dce8'>🔊 Voice Verification</b><br><br>
                <span style='color:#3a5a70'>Press button to record voice</span>
            </div>""", unsafe_allow_html=True)
 
            if st.button("🎙️ Record Voice (3 sec)"):
                with st.spinner("🎙️ Recording... Speak now!"):
                    voice_result = record_and_verify_gender(duration=3)
                st.session_state["voice_result"] = voice_result
 
            voice_result = st.session_state.get("voice_result", {})
            if voice_result:
                vgender = voice_result.get("gender", "Unknown")
                vconf = voice_result.get("confidence", 0)
                st.markdown(f"""<div class="info-box">
                    <b style='color:#c8dce8'>🔊 Voice Result</b><br><br>
                    Gender: <span class="tag-{'male' if vgender=='Male' else 'female'}">{vgender}</span><br>
                    Confidence: <b style='color:#00d4ff'>{vconf:.1f}%</b>
                </div>""", unsafe_allow_html=True)
 
        st.markdown("---")
 
        # ── GRANT / DENY ACCESS ──
        if st.button("✅ Verify & Mark Attendance"):
            face_result = st.session_state.get("face_result", {})
            voice_result = st.session_state.get("voice_result", {})
 
            face_ok = face_result.get("face_detected", False)
            emp = face_result.get("employee")
 
            # Cross-verify gender if both modes
            gender_match = True
            if "Full" in mode and voice_result:
                fg = face_result.get("gender", "")
                vg = voice_result.get("gender", "")
                gender_match = fg == vg
 
            if face_ok and emp and gender_match:
                mark_attendance(emp["id"], emp["name"],
                                face_result.get("gender"),
                                face_result.get("confidence", 0))
                st.markdown(f"""<div class="status-granted">
                    ✅ ACCESS GRANTED<br>
                    <span style='font-size:.85rem;font-weight:400'>
                    Welcome, {emp['name']}! Attendance marked.
                    </span>
                </div>""", unsafe_allow_html=True)
                st.balloons()
                # Announce
                from utils.voice_engine import announce
                announce(f"Welcome {emp['name']}. Access granted.")
 
            elif not gender_match:
                st.markdown("""<div class="status-denied">
                    ❌ ACCESS DENIED<br>
                    <span style='font-size:.85rem;font-weight:400'>
                    Face and voice gender mismatch!
                    </span>
                </div>""", unsafe_allow_html=True)
            elif not emp:
                st.markdown("""<div class="status-denied">
                    ❌ ACCESS DENIED<br>
                    <span style='font-size:.85rem;font-weight:400'>
                    Employee not registered in system.
                    </span>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="status-denied">
                    ❌ ACCESS DENIED<br>
                    <span style='font-size:.85rem;font-weight:400'>
                    Verification failed. Please try again.
                    </span>
                </div>""", unsafe_allow_html=True)
 
            # Clear session
            st.session_state.pop("face_result", None)
            st.session_state.pop("voice_result", None)