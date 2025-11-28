import random
from datetime import datetime, timedelta

AIRLINES = [
    {"name": "IndiGo", "code": "6E", "color": "#00529B"},
    {"name": "Air India", "code": "AI", "color": "#ED1B24"},
    {"name": "SpiceJet", "code": "SG", "color": "#F7941D"},
    {"name": "Vistara", "code": "UK", "color": "#581540"},
    {"name": "AirAsia", "code": "I5", "color": "#ED1C24"}
]

def generate_flights(from_city, to_city, date):
    """Generates mock flights for a given route and date."""
    flights = []
    num_flights = random.randint(5, 10)
    
    base_times = [6, 8, 10, 13, 16, 18, 20, 22] # Hour of day
    
    for _ in range(num_flights):
        airline = random.choice(AIRLINES)
        flight_num = f"{airline['code']}-{random.randint(100, 999)}"
        
        # Random departure time based on base hours + random minutes
        hour = random.choice(base_times)
        minute = random.choice([0, 15, 30, 45])
        dep_time = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour, minutes=minute)
        
        # Duration: 1h 15m to 1h 45m for HYD-GOA usually
        duration_mins = random.randint(75, 105)
        arr_time = dep_time + timedelta(minutes=duration_mins)
        
        stops = random.choices(["Non-stop", "1 Stop"], weights=[0.8, 0.2])[0]
        if stops == "1 Stop":
            duration_mins += random.randint(60, 120) # Layover
            arr_time = dep_time + timedelta(minutes=duration_mins)

        flights.append({
            "id": flight_num,
            "airline": airline["name"],
            "flight_number": flight_num,
            "departure_time": dep_time,
            "arrival_time": arr_time,
            "duration": duration_mins,
            "stops": stops,
            "from_city": from_city,
            "to_city": to_city,
            "base_price": 3500 # Base reference price, will be adjusted dynamically
        })
        
    return sorted(flights, key=lambda x: x['departure_time'])
