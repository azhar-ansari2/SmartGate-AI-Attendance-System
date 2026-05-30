from utils.mysql_db import get_connection

try:
    conn = get_connection()
    print("Connected Successfully")
    conn.close()

except Exception as e:
    print("Error:", e)