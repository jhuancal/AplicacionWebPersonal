import os
import mysql.connector
import time

def wait_for_db():
    retries = 30
    host = os.getenv('MYSQL_HOST', os.getenv('MYSQLHOST', 'db'))
    print(f"Connecting to database at {host}...")
    
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=host,
                user=os.getenv('MYSQL_USER', os.getenv('MYSQLUSER', 'user')),
                password=os.getenv('MYSQL_PASSWORD', os.getenv('MYSQLPASSWORD', 'userpass')),
                port=int(os.getenv('MYSQL_PORT', os.getenv('MYSQLPORT', 3306)))
            )
            print("Database connection successful.")
            return conn
        except mysql.connector.Error as err:
            print(f"Waiting for database... ({err})")
            time.sleep(2)
            retries -= 1
    return None

def init_db():
    print("Starting Database Verification and Initialization...")
    conn = wait_for_db()
    if not conn:
        print("Could not connect to database for initialization.")
        return

    db_name = os.getenv('MYSQL_DATABASE', os.getenv('MYSQLDATABASE', 'tienda'))
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database schema '{db_name}' verified.")
    except Exception as e:
        print(f"Info: Checked database existence ({e})")

    conn.database = db_name
    def run_script(filename):
        print(f"Executing schema script: {filename}")
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                statements = content.split(';')
                for statement in statements:
                    stmt = statement.strip()
                    if stmt:
                        try:
                            cursor.execute(stmt)
                        except mysql.connector.Error as err:
                            print(f"[Schema Update] {err}")
            conn.commit()
            print(f"Schema script {filename} executed successfully.")
        except FileNotFoundError:
            print(f"File {filename} not found.")
    try:
        # Always run the script to ensure new tables are created
        # The script uses IF NOT EXISTS and INSERT IGNORE so it is safe
        print("Ensuring database schema is up to date...")
        run_script('/app/db/init.sql')
            
    except Exception as e:
            
    except Exception as e:
        print(f"Error checking schema: {e}")

    cursor.close()
    conn.close()
    print("Database initialization logic completed.")

if __name__ == "__main__":
    init_db()


