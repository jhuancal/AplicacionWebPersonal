import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host='db',
        user='jhoans',
        password='jhoansPass',
        database='mates'
    )
    return connection
