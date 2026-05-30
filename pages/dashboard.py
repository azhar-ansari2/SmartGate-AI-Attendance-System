import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from utils.attendance import get_today_attendance, get_weekly_attendance, get_monthly_attendance
from utils.database import get_all_employees
 
 
def show():
    st.markdown('<div class="main-title">📊 Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Real-time attendance insights</div>', unsafe_allow_html=True)
 
    employees = get_all_employees()
    today_att = get_today_attendance()
    weekly = get_weekly_attendance()
    monthly = get_monthly_attendance()
 
    total_emp = len(employees)
    present = len(today_att)
    absent = total_emp - present
    rate = (present / total_emp * 100) if total_emp > 0 else 0
 
    # ── KPI Cards ──
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f"""<div class="metric-card">
        <div class="metric-val">{total_emp}</div>
        <div class="metric-key">Total Employees</div></div>""", unsafe_allow_html=True)
    c2.markdown(f"""<div class="metric-card">
        <div class="metric-val" style="color:#00ff88">{present}</div>
        <div class="metric-key">Present Today</div></div>""", unsafe_allow_html=True)
    c3.markdown(f"""<div class="metric-card">
        <div class="metric-val" style="color:#ff4b4b">{absent}</div>
        <div class="metric-key">Absent Today</div></div>""", unsafe_allow_html=True)
    c4.markdown(f"""<div class="metric-card">
        <div class="metric-val" style="color:#ff6b35">{rate:.1f}%</div>
        <div class="metric-key">Attendance Rate</div></div>""", unsafe_allow_html=True)
 
    st.markdown("---")
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.markdown("#### 📈 Weekly Attendance Trend")
        if weekly:
            df_week = pd.DataFrame(weekly)
            fig = px.bar(df_week, x="date", y="count",
                         color_discrete_sequence=["#00d4ff"],
                         template="plotly_dark")
            fig.update_layout(
                plot_bgcolor="#080f18", paper_bgcolor="#080f18",
                font_color="#c8dce8", showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No weekly data yet.")
 
    with col2:
        st.markdown("#### 🥧 Gender Distribution")
        if employees:
            male_count = sum(1 for e in employees if e.get("gender") == "Male")
            female_count = sum(1 for e in employees if e.get("gender") == "Female")
            fig2 = go.Figure(go.Pie(
                labels=["Male", "Female"],
                values=[male_count, female_count],
                marker_colors=["#00d4ff", "#ff5fa0"],
                hole=0.5
            ))
            fig2.update_layout(
                plot_bgcolor="#080f18", paper_bgcolor="#080f18",
                font_color="#c8dce8",
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No employee data yet.")
 
    st.markdown("---")
    st.markdown("#### 🕐 Today's Check-in Timeline")
 
    if today_att:
        df_today = pd.DataFrame(today_att)
        df_today["time"] = pd.to_datetime(df_today["timestamp"]).dt.strftime("%H:%M")
        fig3 = px.scatter(df_today, x="time", y="name",
                          color="gender",
                          color_discrete_map={"Male": "#00d4ff", "Female": "#ff5fa0"},
                          template="plotly_dark",
                          size_max=12)
        fig3.update_traces(marker=dict(size=14))
        fig3.update_layout(
            plot_bgcolor="#080f18", paper_bgcolor="#080f18",
            font_color="#c8dce8",
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Check-in Time",
            yaxis_title=""
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No check-ins today yet.")