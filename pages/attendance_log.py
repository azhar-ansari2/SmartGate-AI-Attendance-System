import streamlit as st
import pandas as pd
import datetime
from utils.attendance import (
    get_all_attendance,
    get_today_attendance,
    clear_attendance
)


def show():
    st.markdown(
        '<div class="main-title">📋 Attendance Log</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="sub-title">View and export attendance records</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["📅 Today", "🗓️ All Records"])

    with tab1:
        st.markdown(
            f"### Today — {datetime.date.today().strftime('%d %B %Y')}"
        )

        today = get_today_attendance()

        if not today:
            st.info("No attendance marked today yet.")
        else:
            df = pd.DataFrame(today)

            df["time"] = pd.to_datetime(
                df["timestamp"]
            ).dt.strftime("%H:%M:%S")

            df = df[
                ["name", "emp_id", "gender", "confidence", "time"]
            ].copy()

            df.columns = [
                "Name",
                "Emp ID",
                "Gender",
                "Confidence %",
                "Check-in Time"
            ]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            csv = df.to_csv(index=False)

            st.download_button(
                "⬇️ Export Today's Attendance (CSV)",
                csv,
                f"attendance_{datetime.date.today()}.csv",
                "text/csv"
            )

    with tab2:
        st.markdown("### All Attendance Records")

        all_records = get_all_attendance()

        if not all_records:
            st.info("No attendance records found.")
            return

        df_all = pd.DataFrame(all_records)

        df_all["date"] = pd.to_datetime(
            df_all["timestamp"]
        ).dt.strftime("%Y-%m-%d")

        df_all["time"] = pd.to_datetime(
            df_all["timestamp"]
        ).dt.strftime("%H:%M:%S")

        col1, col2, col3 = st.columns(3)

        dates = sorted(
            df_all["date"].unique(),
            reverse=True
        )

        selected_date = col1.selectbox(
            "Filter by Date",
            ["All"] + list(dates)
        )

        genders = ["All", "Male", "Female"]

        selected_gender = col2.selectbox(
            "Filter by Gender",
            genders
        )

        search_name = col3.text_input(
            "Search by Name",
            ""
        )

        filtered = df_all.copy()

        if selected_date != "All":
            filtered = filtered[
                filtered["date"] == selected_date
            ]

        if selected_gender != "All":
            filtered = filtered[
                filtered["gender"] == selected_gender
            ]

        if search_name:
            filtered = filtered[
                filtered["name"].str.contains(
                    search_name,
                    case=False,
                    na=False
                )
            ]

        display = filtered[
            ["name", "emp_id", "gender",
             "confidence", "date", "time"]
        ].copy()

        display.columns = [
            "Name",
            "Emp ID",
            "Gender",
            "Confidence %",
            "Date",
            "Time"
        ]

        st.markdown(f"**{len(display)} records**")

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

        csv_all = display.to_csv(index=False)

        st.download_button(
            "⬇️ Export All Records (CSV)",
            csv_all,
            "all_attendance.csv",
            "text/csv"
        )

        st.markdown("---")

        if st.button(
            "🗑️ Clear All Records",
            type="secondary"
        ):
            clear_attendance()
            st.success("All records cleared.")
            st.rerun()