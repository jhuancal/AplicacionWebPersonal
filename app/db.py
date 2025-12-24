import mysql.connector
import os

def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('MYSQLHOST'),
        user=os.getenv('MYSQLUSER'),
        password=os.getenv('MYSQLPASSWORD'),
        database=os.getenv('MYSQLDATABASE'),
        port=int(os.getenv('MYSQLPORT'))
    )
    return connection
