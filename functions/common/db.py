import os, psycopg2, psycopg2.extras
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", 5432),
        dbname=os.getenv("DB_NAME", "cofrap"),
        user=os.getenv("DB_USER", "faas"),
        password=os.getenv("DB_PASS", "faaspass"))