from utils.mysql_db import get_connection
import datetime
import random


def mark_attendance(emp_id, name, gender, confidence):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO attendance
        (id, emp_id, name, gender, confidence, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        random.randint(100000, 999999),
        emp_id,
        name,
        gender,
        confidence,
        datetime.datetime.now().date()
    ))

    conn.commit()

    cursor.close()
    conn.close()


def get_all_attendance():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM attendance
        ORDER BY timestamp DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_today_attendance():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM attendance
        WHERE DATE(timestamp)=CURDATE()
        ORDER BY timestamp DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_weekly_attendance():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT DATE(timestamp) as date,
               COUNT(*) as count
        FROM attendance
        GROUP BY DATE(timestamp)
        ORDER BY DATE(timestamp) DESC
        LIMIT 7
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return list(reversed(data))


def get_monthly_attendance():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT DATE_FORMAT(timestamp,'%Y-%m') as month,
               COUNT(*) as count
        FROM attendance
        GROUP BY DATE_FORMAT(timestamp,'%Y-%m')
        ORDER BY month
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def clear_attendance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM attendance")

    conn.commit()

    cursor.close()
    conn.close()