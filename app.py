import streamlit as st

st.set_page_config(
    page_title="SmartGate — Enterprise Attendance",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp { background: #050a0f; }
[data-testid="stSidebar"] { background: #080f18 !important; border-right: 1px solid #0d2137; }

.main-title {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #00d4ff, #00ff88);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.sub-title { color: #3a5a70; font-size: .85rem; margin-bottom: 20px; }

.metric-card {
    background: rgba(0,212,255,0.06);
    border: 1px solid rgba(0,212,255,0.18);
    border-radius: 10px; padding: 18px;
    text-align: center;
}
.metric-val { font-size: 2rem; font-weight: 800; color: #00d4ff; }
.metric-key { font-size: .7rem; color: #3a5a70; margin-top: 4px; text-transform: uppercase; letter-spacing: .1em; }

.status-granted {
    background: rgba(0,255,136,0.1); border: 1px solid rgba(0,255,136,0.3);
    color: #00ff88; padding: 12px 20px; border-radius: 8px;
    font-size: 1.1rem; font-weight: 700; text-align: center;
}
.status-denied {
    background: rgba(255,75,75,0.1); border: 1px solid rgba(255,75,75,0.3);
    color: #ff4b4b; padding: 12px 20px; border-radius: 8px;
    font-size: 1.1rem; font-weight: 700; text-align: center;
}
.info-box {
    background: rgba(255,255,255,0.02); border: 1px solid #0d2137;
    border-radius: 8px; padding: 14px; margin: 8px 0;
}
.tag-male { background: rgba(0,212,255,0.15); color: #00d4ff; padding: 2px 10px; border-radius: 20px; font-size: .75rem; font-weight: 600; }
.tag-female { background: rgba(255,95,160,0.15); color: #ff5fa0; padding: 2px 10px; border-radius: 20px; font-size: .75rem; font-weight: 600; }
.tag-present { background: rgba(0,255,136,0.15); color: #00ff88; padding: 2px 10px; border-radius: 20px; font-size: .75rem; }
.tag-absent { background: rgba(255,75,75,0.15); color: #ff4b4b; padding: 2px 10px; border-radius: 20px; font-size: .75rem; }

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #00d4ff, #0099cc);
    color: #000; font-weight: 700; border: none;
    border-radius: 8px; padding: 10px 28px;
    font-size: .9rem; width: 100%;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] button:hover { opacity: 0.85; transform: translateY(-1px); }

.stTabs [data-baseweb="tab"] { color: #3a5a70 !important; }
.stTabs [aria-selected="true"] { color: #00d4ff !important; border-bottom-color: #00d4ff !important; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("""
    <div style='padding:10px 0 20px;'>
        <div style='font-size:1.3rem;font-weight:800;color:#00d4ff;'>🏢 SmartGate</div>
        <div style='font-size:.7rem;color:#3a5a70;margin-top:2px;'>Enterprise Attendance System</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🚪 Entry Gate",
        "📊 Dashboard",
        "👥 Employees",
        "📋 Attendance Log",
        "⚙️ Settings"
    ])

    st.markdown("---")
    st.markdown("""
    <div style='font-size:.65rem;color:#3a5a70;'>
    <b style='color:#c8dce8'>SmartGate v1.0</b><br>
    Face + Voice Verification<br>
    Built by Md Azhar Ansari<br>
    Infosys Intern 2025
    </div>
    """, unsafe_allow_html=True)

# Page routing
if "🚪 Entry Gate" in page:
    from pages.gate import show; show()
elif "📊 Dashboard" in page:
    from pages.dashboard import show; show()
elif "👥 Employees" in page:
    from pages.employees import show; show()
elif "📋 Attendance Log" in page:
    from pages.attendance_log import show; show()
elif "⚙️ Settings" in page:
    from pages.settings import show; show()
