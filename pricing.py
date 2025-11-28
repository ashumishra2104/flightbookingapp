from datetime import datetime

def calculate_price(base_price, flight, booking_date, travel_class, passengers):
    """
    Calculates the final price based on dynamic factors.
    """
    price = base_price
    
    # 1. Advance Booking Discount/Surcharge
    days_to_travel = (flight['departure_time'].date() - booking_date).days
    
    if days_to_travel >= 30:
        price *= 0.80 # -20%
    elif 15 <= days_to_travel < 30:
        price *= 0.90 # -10%
    elif 7 <= days_to_travel < 15:
        pass # 0%
    else:
        price *= 1.25 # +25%
        
    # 2. Peak Season (Oct-Jan)
    month = flight['departure_time'].month
    if month in [10, 11, 12, 1]:
        price *= 1.30
        
    # 3. Weekend Surcharge (Fri, Sat, Sun)
    weekday = flight['departure_time'].weekday() # 0=Mon, 6=Sun
    if weekday in [4, 5, 6]:
        price *= 1.20
        
    # 4. Time of Day
    hour = flight['departure_time'].hour
    if 6 <= hour < 8:
        price *= 1.15 # Early Morning
    elif 8 <= hour < 12:
        price *= 1.10 # Morning
    elif 16 <= hour < 20:
        price *= 1.15 # Evening
    elif 20 <= hour or hour < 6:
        price *= 0.90 # Night
        
    # 5. Class Multiplier
    if travel_class == "Premium Economy":
        price *= 1.5
    elif travel_class == "Business":
        price *= 2.5
        
    return round(price)

def calculate_total_fare(outbound_price, return_price, passengers, addons_cost=0):
    """
    Calculates total breakdown including taxes and fees.
    """
    num_pax = passengers['adults'] + passengers['children'] # Infants usually flat fee or tax only, simplifying here
    
    base_fare = (outbound_price + return_price) * num_pax
    
    # Fees
    convenience_fee = 200 * num_pax
    psf = 150 * num_pax
    fuel_surcharge = 500 * num_pax
    
    # GST (5% of base)
    gst = base_fare * 0.05
    
    total = base_fare + convenience_fee + psf + fuel_surcharge + gst + addons_cost
    
    return {
        "base_fare": base_fare,
        "convenience_fee": convenience_fee,
        "psf": psf,
        "fuel_surcharge": fuel_surcharge,
        "gst": gst,
        "addons": addons_cost,
        "total": round(total)
    }
