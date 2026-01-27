import mysql.connector

def create_connection():
    try:
        # My Localhost connection
        # connection = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     database="greenrider",
        #     password="offer@123",
        #     port = '3306',
        # )

        connection = mysql.connector.connect(
            host="mysql.railway.internal",
            user="root",
            database="railway",
            password="dQaFAcFDKLtUAjdXGgSccPxbzuabcrDt",
            port = '3306',
        )
        
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
