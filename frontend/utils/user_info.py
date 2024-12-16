import mysql.connector
from mysql.connector import Error
from werkzeug.security import check_password_hash

MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "incident_nav_auth",
    "port": 3306
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        return connection
    except Error as e:
        return None
    
def verify_user(username, password):
    connection = get_db_connection()
    if not connection:
        return False
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE user = %s", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user['pwd'], password):
            return user, True
        return None, False
    finally:
        connection.close()