import mysql.connector

def create_connection():
    try:
        # My Localhost connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            database="greenrider",
            password="offer@123",
            port = '3306',
        )
        
        # New Database Start ---
        # connection = mysql.connector.connect(
        #     host="10.0.0.60",
        #     user="hrm_user",
        #     database="hrm_db",
        #     password="D&7We{dcA6uB",
        #     port = '3306',
        # )
        # New database End --
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
