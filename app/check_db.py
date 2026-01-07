from db import get_db_connection
try:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print("Tables:", tables)
    
    if 'Gam_MatchPvP' in tables:
        print("Gam_MatchPvP exists.")
        cursor.execute("DESCRIBE Gam_MatchPvP")
        print(cursor.fetchall())
    else:
        print("Gam_MatchPvP MISSING!")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
