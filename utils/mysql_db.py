import mysql.connector
import streamlit as st

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["${{RAILWAY_PRIVATE_DOMAIN}}"],
        port=int(st.secrets["3306"]),
        user=st.secrets["root"],
        password=st.secrets["${{MYSQL_ROOT_PASSWORD}}"],
        database=st.secrets["${{MYSQL_DATABASE}}"]
    )