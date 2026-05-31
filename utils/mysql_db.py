import mysql.connector
import streamlit as st

def get_connection():
    return mysql.connector.connect(
        host=st.secrets["${{mysql.railway.internal}}"],
        port=int(st.secrets["3306"]),
        user=st.secrets["root"],
        password=st.secrets["${{rqZeaMMMxmOUosrSrwEgOcUKyKUgJPggYoot}}"],
        database=st.secrets["${{railway}}"]
    )