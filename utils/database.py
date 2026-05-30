from utils.mysql_db import get_connection
import json

def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return employees


def add_employee(employee):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO employees
    (id, emp_id, name, department, role, gender,
     email, registered_at, face_encoding)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        employee["id"],
        employee["emp_id"],
        employee["name"],
        employee["department"],
        employee["role"],
        employee["gender"],
        employee["email"],
        employee["registered_at"],
        json.dumps(employee["face_encoding"])
    )

    cursor.execute(query, values)

    conn.commit()

    cursor.close()
    conn.close()


def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM employees WHERE id=%s",
        (emp_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_employee_by_id(emp_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM employees WHERE emp_id=%s",
        (emp_id,)
    )

    employee = cursor.fetchone()

    cursor.close()
    conn.close()

    return employee