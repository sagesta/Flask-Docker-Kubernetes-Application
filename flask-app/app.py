from flask import Flask
import psycopg2
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        logging.debug("Attempting to connect to the database")
        conn = psycopg2.connect(
            dbname=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ['POSTGRES_HOST']
        )
        logging.debug("Database connection successful")
        cur = conn.cursor()
        cur.execute('SELECT version();')
        version = cur.fetchone()
        conn.close()
        logging.debug(f"PostgreSQL version: {version}")
        return f"PostgreSQL version: {version}"
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
