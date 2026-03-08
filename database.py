import os
from sqlalchemy import create_engine
import psycopg2
from dotenv import load_dotenv


#De la documentacion de Supabase
#URL: https://wgnxvoejhlwjzekkawww.supabase.co
#Publishable Key: sb_publishable_CoXJN8OsnEkIWd2nGH1Y9Q_ygxfNaEj
#Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Indnbnh2b2VqaGx3anpla2thd3d3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzI5Mzk2MDAsImV4cCI6MjA4ODUxNTYwMH0.9MuSTZ100kYIXy2Zu6RN6qcEh9n--IS4Mh9zPcQzNFI

load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
    