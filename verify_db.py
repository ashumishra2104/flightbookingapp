import os
import psycopg2
import streamlit as st

# Load secrets
try:
    import toml
    secrets = toml.load(".streamlit/secrets.toml")
    db_url = secrets["DATABASE_URL"]
except Exception as e:
    print(f"Error loading secrets: {e}")
    exit(1)

print(f"Connecting to: {db_url.split('@')[1]}") # Print host only for security

try:
    conn = psycopg2.connect(db_url, sslmode='require')
    cur = conn.cursor()
    
    # Check tables
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    tables = cur.fetchall()
    print("\nTables found in DB:")
    for t in tables:
        print(f"- {t[0]}")
        
    if not tables:
        print("\nNo tables found! Attempting to create them...")
        # Copy-paste init logic from db.py
        cur.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                pnr VARCHAR(10) PRIMARY KEY,
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                outbound_flight_id VARCHAR(50),
                return_flight_id VARCHAR(50),
                total_amount DECIMAL(10, 2),
                contact_email VARCHAR(100),
                contact_phone VARCHAR(20),
                status VARCHAR(20)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS passengers (
                id SERIAL PRIMARY KEY,
                pnr VARCHAR(10) REFERENCES bookings(pnr),
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                gender VARCHAR(20),
                seat_outbound VARCHAR(10),
                seat_return VARCHAR(10)
            );
        """)
        conn.commit()
        print("Tables created successfully.")
        
    # Check for data
    cur.execute("SELECT count(*) FROM bookings;")
    count = cur.fetchone()[0]
    print(f"\nTotal Bookings: {count}")
    
    if count > 0:
        cur.execute("SELECT * FROM bookings LIMIT 5;")
        rows = cur.fetchall()
        print("\nRecent Bookings:")
        for r in rows:
            print(r)

    cur.close()
    conn.close()

except Exception as e:
    print(f"\nError: {e}")
