import random
import string
from datetime import datetime, timedelta
from fpdf import FPDF

def generate_pnr(length=6):
    """Generates a random alphanumeric PNR."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def format_currency(amount):
    """Formats amount as INR currency."""
    return f"₹{amount:,.0f}"

def format_duration(minutes):
    """Formats duration in minutes to Xh Ym."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m"

def get_day_name(date_obj):
    """Returns the day name for a given date."""
    return date_obj.strftime("%A")

def generate_ticket_pdf(booking_data, pnr, fare_breakdown):
    """Generates a PDF ticket for the booking."""
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 20)
            self.set_text_color(0, 82, 155) # SkyConnect Blue
            self.cell(0, 10, 'SkyConnect', 0, 1, 'C')
            self.set_font('Arial', '', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 5, 'Your Premium Gateway', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.set_text_color(128)
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    pdf = PDF()
    pdf.add_page()
    
    # Booking Info
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f'Booking Confirmation - PNR: {pnr}', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f'Date: {datetime.now().strftime("%Y-%m-%d")}', 0, 1)
    pdf.ln(5)
    
    # Flight Details
    def add_flight_section(title, flight):
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, title, 1, 1, 'L', 1)
        pdf.set_font('Arial', '', 10)
        
        pdf.cell(40, 8, f"Airline: {flight['airline']}", 0, 0)
        pdf.cell(40, 8, f"Flight: {flight['flight_number']}", 0, 1)
        
        pdf.cell(40, 8, f"From: {flight['from_city']}", 0, 0)
        pdf.cell(40, 8, f"To: {flight['to_city']}", 0, 1)
        
        pdf.cell(40, 8, f"Dep: {flight['departure_time'].strftime('%Y-%m-%d %H:%M')}", 0, 0)
        pdf.cell(40, 8, f"Arr: {flight['arrival_time'].strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.ln(5)

    add_flight_section("Outbound Flight", booking_data['selected_outbound'])
    add_flight_section("Return Flight", booking_data['selected_return'])
    
    # Passengers
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Passenger Details", 1, 1, 'L', 1)
    pdf.set_font('Arial', '', 10)
    
    for p in booking_data['passenger_details']:
        pdf.cell(0, 6, f"- {p['first_name']} {p['last_name']} ({p['gender']})", 0, 1)
    pdf.ln(5)
    
    # Payment
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, "Payment Summary", 1, 1, 'L', 1)
    pdf.set_font('Arial', '', 10)
    
    def fmt_price(amount):
        return f"INR {amount:,.0f}"
    
    pdf.cell(100, 6, "Base Fare", 0, 0)
    pdf.cell(0, 6, fmt_price(fare_breakdown['base_fare']), 0, 1, 'R')
    
    pdf.cell(100, 6, "Taxes & Fees", 0, 0)
    pdf.cell(0, 6, fmt_price(fare_breakdown['convenience_fee'] + fare_breakdown['psf'] + fare_breakdown['fuel_surcharge'] + fare_breakdown['gst']), 0, 1, 'R')
    
    pdf.cell(100, 6, "Add-ons", 0, 0)
    pdf.cell(0, 6, fmt_price(fare_breakdown['addons']), 0, 1, 'R')
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(100, 8, "Total Amount", 'T', 0)
    pdf.cell(0, 8, fmt_price(fare_breakdown['total']), 'T', 1, 'R')
    
    return pdf.output(dest='S').encode('latin-1')
