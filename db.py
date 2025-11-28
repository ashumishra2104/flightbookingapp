import os
import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

# Helper to get connection
def get_connection():
    # Try to get from Streamlit secrets first (for Cloud), then env var (for local)
    db_url = os.getenv("DATABASE_URL")
    if not db_url and "postgres" in st.secrets:
        # Construct from secrets if available in dictionary format
        # Or if user put the URL string directly in secrets
        pass
        
    # For simplicity, we expect DATABASE_URL env var or st.secrets["DATABASE_URL"]
    if not db_url:
        try:
            db_url = st.secrets["DATABASE_URL"]
        except:
            pass
            
    if not db_url:
        return None
        
    try:
        conn = psycopg2.connect(db_url, sslmode='require')
        return conn
    except Exception as e:
        st.error(f"DB Connection Error: {e}")
        return None

def init_db():
    """Initialize the database tables if they don't exist."""
    conn = get_connection()
    if not conn:
        return
        
    try:
        cur = conn.cursor()
        
        # Bookings Table
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
        
        # Passengers Table
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
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"DB Init Error: {e}")

def save_booking(booking_data, pnr, fare_breakdown):
    """Save booking details to the database."""
    conn = get_connection()
    if not conn:
        st.warning("Database connection not available. Booking saved locally only.")
        return False
        
    try:
        cur = conn.cursor()
        
        # Insert Booking
        cur.execute("""
            INSERT INTO bookings (pnr, outbound_flight_id, return_flight_id, total_amount, contact_email, contact_phone, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            pnr,
            booking_data['selected_outbound']['id'],
            booking_data['selected_return']['id'],
            fare_breakdown['total'],
            booking_data['contact']['email'],
            booking_data['contact']['phone'],
            'CONFIRMED'
        ))
        
        # Insert Passengers
        for idx, p in enumerate(booking_data['passenger_details']):
            # Get assigned seats if available
            seat_out = "N/A"
            seat_ret = "N/A"
            
            # Simple logic: Assign seats in order (This is a simplification)
            # In a real app, we'd map specific seats to specific passengers explicitly in the UI.
            # Here we just take the list of selected seats and assign them 1-to-1.
            if idx < len(booking_data['seats']['outbound']):
                seat_out = booking_data['seats']['outbound'][idx]
            if idx < len(booking_data['seats']['return']):
                seat_ret = booking_data['seats']['return'][idx]
                
            cur.execute("""
                INSERT INTO passengers (pnr, first_name, last_name, gender, seat_outbound, seat_return)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                pnr,
                p['first_name'],
                p['last_name'],
                p['gender'],
                seat_out,
                seat_ret
            ))
            
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving booking to DB: {e}")
        return False
