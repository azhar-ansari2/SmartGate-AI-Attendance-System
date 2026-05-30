import streamlit as st
import cv2
import numpy as np
import uuid
import datetime

from utils.database import (
    get_all_employees,
    add_employee,
    delete_employee
)

from utils.face_engine import encode_face


def show():

    st.markdown(
        '<div class="main-title">👥 Employee Management</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sub-title">Register and manage employees</div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs([
        "➕ Register New Employee",
        "📋 All Employees"
    ])

    # ==========================
    # REGISTER EMPLOYEE
    # ==========================

    with tab1:

        st.markdown("### Register New Employee")

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Full Name *",
                placeholder="e.g. Md Azhar Ansari"
            )

            emp_id = st.text_input(
                "Employee ID *",
                placeholder="e.g. INF2025001"
            )

            dept = st.selectbox(
                "Department",
                [
                    "Engineering",
                    "Data Science",
                    "HR",
                    "Finance",
                    "Operations",
                    "Marketing",
                    "IT Infrastructure"
                ]
            )

            role = st.text_input(
                "Job Role",
                placeholder="e.g. Data Science Intern"
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female"]
            )

            email = st.text_input(
                "Email",
                placeholder="name@company.com"
            )

        with col2:

            st.markdown("### 📷 Face Registration")

            face_img = st.camera_input(
                "Capture Face",
                key="reg_cam",
                label_visibility="collapsed"
            )

            if face_img:

                file_bytes = np.asarray(
                    bytearray(face_img.read()),
                    dtype=np.uint8
                )

                frame = cv2.imdecode(
                    file_bytes,
                    cv2.IMREAD_COLOR
                )

                gray = cv2.cvtColor(
                    frame,
                    cv2.COLOR_BGR2GRAY
                )

                cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades +
                    "haarcascade_frontalface_default.xml"
                )

                faces = cascade.detectMultiScale(
                    gray,
                    1.1,
                    5,
                    minSize=(60, 60)
                )

                if len(faces) > 0:
                    st.success(
                        "✅ Face detected successfully"
                    )
                else:
                    st.error(
                        "❌ No face detected. Please retake photo."
                    )

        st.markdown("---")

        if st.button("💾 Register Employee"):

            if not name:
                st.error("Please enter employee name")

            elif not emp_id:
                st.error("Please enter employee ID")

            elif face_img is None:
                st.error("Please capture a face photo")

            else:

                file_bytes = np.asarray(
                    bytearray(face_img.getvalue()),
                    dtype=np.uint8
                )

                frame = cv2.imdecode(
                    file_bytes,
                    cv2.IMREAD_COLOR
                )

                face_encoding = encode_face(frame)

                if face_encoding is None:

                    st.error(
                        "Could not encode face. Please retake photo."
                    )

                else:

                    employee = {

                        "id": str(uuid.uuid4()),

                        "emp_id": emp_id,

                        "name": name,

                        "department": dept,

                        "role": role,

                        "gender": gender,

                        "email": email,

                        "registered_at": datetime.datetime.now(),

                        "face_encoding": face_encoding
                    }

                    add_employee(employee)

                    st.success(
                        f"✅ {name} registered successfully!"
                    )

                    st.balloons()

    # ==========================
    # ALL EMPLOYEES
    # ==========================

    with tab2:

        st.markdown(
            "### All Registered Employees"
        )

        employees = get_all_employees()

        if not employees:

            st.info(
                "No employees registered yet."
            )

            return

        search = st.text_input(
            "🔍 Search by Name or Department",
            ""
        )

        if search:

            filtered = [

                emp

                for emp in employees

                if search.lower()
                in emp.get("name", "").lower()

                or

                search.lower()
                in emp.get("department", "").lower()
            ]

        else:

            filtered = employees

        st.markdown(
            f"**{len(filtered)} employees found**"
        )

        for emp in filtered:

            gender = emp.get(
                "gender",
                "Male"
            )

            tag_class = (
                "tag-male"
                if gender == "Male"
                else "tag-female"
            )

            with st.expander(
                f"👤 {emp.get('name')} — {emp.get('emp_id')}"
            ):

                c1, c2, c3 = st.columns(3)

                c1.markdown(
                    f"**Department:** {emp.get('department', '—')}"
                )

                c1.markdown(
                    f"**Role:** {emp.get('role', '—')}"
                )

                c2.markdown(
                    f"**Gender:** <span class='{tag_class}'>{gender}</span>",
                    unsafe_allow_html=True
                )

                c2.markdown(
                    f"**Email:** {emp.get('email', '—')}"
                )

                registered = emp.get(
                    "registered_at"
                )

                if registered:

                    try:

                        registered = registered.strftime(
                            "%Y-%m-%d"
                        )

                    except:

                        registered = str(
                            registered
                        )[:10]

                else:

                    registered = "—"

                c3.markdown(
                    f"**Registered:** {registered}"
                )

                if c3.button(
                    "🗑️ Remove",
                    key=f"del_{emp['id']}"
                ):

                    delete_employee(
                        emp["id"]
                    )

                    st.success(
                        "Employee removed."
                    )

                    st.rerun()