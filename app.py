import streamlit as st
from datetime import datetime, timedelta
import flight_data
import pricing
import utils

# Page Configuration
st.set_page_config(
    page_title="SkyConnect - Flight Booking",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Initialization
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'booking_data' not in st.session_state:
    st.session_state.booking_data = {
        'departure_city': 'Hyderabad (HYD)',
        'arrival_city': 'Goa (GOI)',
        'departure_date': datetime.now().date() + timedelta(days=1),
        'return_date': datetime.now().date() + timedelta(days=4),
        'passengers': {'adults': 1, 'children': 0, 'infants': 0},
        'travel_class': 'Economy',
        'selected_outbound': None,
        'selected_return': None,
        'passenger_details': [],
        'seats': {'outbound': [], 'return': []},
        'addons': {'meals': [], 'baggage': [], 'insurance': False}
    }

def next_step():
    st.session_state.step += 1

def prev_step():
    st.session_state.step -= 1

# Header
st.markdown("""
    <div class="main-header">
        <h1>✈️ SkyConnect</h1>
        <p>Your premium gateway between Hyderabad and Goa</p>
    </div>
""", unsafe_allow_html=True)

# Progress Indicator
steps = ["Search", "Select Flights", "Passengers", "Seats", "Add-ons", "Payment"]
current_step = st.session_state.step

st.markdown(f"""
    <div class="step-indicator">
        {''.join([f'<div class="step {"active" if i+1 == current_step else "completed" if i+1 < current_step else ""}">{step}</div>' for i, step in enumerate(steps)])}
    </div>
""", unsafe_allow_html=True)

# --- STEP 1: SEARCH ---
if st.session_state.step == 1:
    st.markdown("### 🔍 Search Flights")
    
    # Container for search form
    with st.container():
        st.markdown('<div style="background: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("From", value="Hyderabad (HYD)", disabled=True)
            
            # FIX: Ensure default departure date is valid (>= today)
            default_dep = st.session_state.booking_data['departure_date']
            min_dep = datetime.now().date()
            if default_dep < min_dep:
                default_dep = min_dep
                
            dep_date = st.date_input("Departure Date", 
                                   value=default_dep,
                                   min_value=min_dep)
            
        with col2:
            st.text_input("To", value="Goa (GOI)", disabled=True)
            
            # FIX: Ensure default return date is valid (>= dep_date)
            default_ret = st.session_state.booking_data['return_date']
            if default_ret < dep_date:
                default_ret = dep_date
                
            ret_date = st.date_input("Return Date", 
                                   value=default_ret,
                                   min_value=dep_date)
    
        col3, col4, col5 = st.columns(3)
        
        with col3:
            adults = st.number_input("Adults (12+)", min_value=1, max_value=9, value=st.session_state.booking_data['passengers']['adults'])
        with col4:
            children = st.number_input("Children (2-11)", min_value=0, max_value=9, value=st.session_state.booking_data['passengers']['children'])
        with col5:
            infants = st.number_input("Infants (<2)", min_value=0, max_value=9, value=st.session_state.booking_data['passengers']['infants'])
    
        travel_class = st.selectbox("Class", ["Economy", "Premium Economy", "Business"], index=0 if st.session_state.booking_data['travel_class'] == "Economy" else 1 if st.session_state.booking_data['travel_class'] == "Premium Economy" else 2)
    
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Search Flights ➔", use_container_width=True):
            st.session_state.booking_data.update({
                'departure_date': dep_date,
                'return_date': ret_date,
                'passengers': {'adults': adults, 'children': children, 'infants': infants},
                'travel_class': travel_class
            })
            next_step()
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 2: SELECT FLIGHTS ---
elif st.session_state.step == 2:
    st.markdown("### ✈️ Select Flights")
    
    # Generate flights (Cached to prevent randomization on rerun)
    @st.cache_data
    def get_flights(from_city, to_city, date):
        return flight_data.generate_flights(from_city, to_city, date)

    outbound_flights = get_flights("HYD", "GOI", st.session_state.booking_data['departure_date'])
    return_flights = get_flights("GOI", "HYD", st.session_state.booking_data['return_date'])
    
    tab1, tab2 = st.tabs(["Outbound: HYD → GOI", "Return: GOI → HYD"])
    
    def render_flight_header():
        st.markdown("""
        <div style="display: grid; grid-template-columns: 2fr 1.5fr 1.5fr 1.5fr 1.5fr; gap: 1rem; padding: 0.5rem 1.5rem; color: #6b7280; font-weight: 600; font-size: 0.9rem;">
            <div>AIRLINE</div>
            <div style="text-align: center;">DEPARTURE</div>
            <div style="text-align: center;">DURATION</div>
            <div style="text-align: center;">ARRIVAL</div>
            <div style="text-align: right;">PRICE</div>
        </div>
        """, unsafe_allow_html=True)

    def render_flight_card(flight, selected_id, key_prefix):
        price = pricing.calculate_price(flight['base_price'], flight, datetime.now().date(), st.session_state.booking_data['travel_class'], st.session_state.booking_data['passengers'])
        
        is_selected = selected_id == flight['id']
        card_class = "flight-card flight-card-selected" if is_selected else "flight-card"
        
        # HTML Structure matching CSS Grid
        card_html = f"""
        <div class="{card_class}">
            <div>
                <div class="fc-airline">{flight['airline']}</div>
                <div class="fc-sub">{flight['flight_number']}</div>
            </div>
            <div style="text-align: center;">
                <div class="fc-time">{flight['departure_time'].strftime('%H:%M')}</div>
                <div class="fc-sub">{flight['from_city']}</div>
            </div>
            <div style="text-align: center;">
                <div class="fc-duration">{utils.format_duration(flight['duration'])}</div>
                <div class="fc-sub">{flight['stops']}</div>
            </div>
            <div style="text-align: center;">
                <div class="fc-time">{flight['arrival_time'].strftime('%H:%M')}</div>
                <div class="fc-sub">{flight['to_city']}</div>
            </div>
            <div class="fc-price">
                {utils.format_currency(price)}
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        
        if st.button("Select", key=f"{key_prefix}_{flight['id']}", type="primary" if is_selected else "secondary", use_container_width=True):
            return flight, price
        return None, None

    with tab1:
        st.write(f"Flights for {utils.get_day_name(st.session_state.booking_data['departure_date'])}, {st.session_state.booking_data['departure_date']}")
        render_flight_header()
        
        # We need to track selection.
        selected_out = st.session_state.booking_data.get('selected_outbound')
        current_selected = selected_out.get('id') if selected_out else None
        
        for flight in outbound_flights:
            sel_flight, sel_price = render_flight_card(flight, current_selected, "out")
            if sel_flight:
                st.session_state.booking_data['selected_outbound'] = sel_flight
                st.session_state.booking_data['selected_outbound']['price'] = sel_price
                st.rerun()

    with tab2:
        st.write(f"Flights for {utils.get_day_name(st.session_state.booking_data['return_date'])}, {st.session_state.booking_data['return_date']}")
        render_flight_header()
        
        selected_ret = st.session_state.booking_data.get('selected_return')
        current_selected = selected_ret.get('id') if selected_ret else None
        
        for flight in return_flights:
            sel_flight, sel_price = render_flight_card(flight, current_selected, "ret")
            if sel_flight:
                st.session_state.booking_data['selected_return'] = sel_flight
                st.session_state.booking_data['selected_return']['price'] = sel_price
                st.rerun()

    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅ Back"):
            prev_step()
            st.rerun()
    with col_next:
        # Validation
        if not st.session_state.booking_data.get('selected_outbound') or not st.session_state.booking_data.get('selected_return'):
            st.warning("Please select both outbound and return flights.")
        else:
            if st.button("Continue to Passengers ➔"):
                next_step()
                st.rerun()

# --- STEP 3: PASSENGER DETAILS ---
elif st.session_state.step == 3:
    st.markdown("### 👤 Passenger Details")
    
    with st.form("passenger_form"):
        passengers = []
        total_pax = st.session_state.booking_data['passengers']['adults'] + st.session_state.booking_data['passengers']['children']
        
        for i in range(total_pax):
            st.markdown(f"**Passenger {i+1}**")
            c1, c2, c3 = st.columns(3)
            with c1:
                fname = st.text_input(f"First Name", key=f"fname_{i}")
            with c2:
                lname = st.text_input(f"Last Name", key=f"lname_{i}")
            with c3:
                gender = st.selectbox(f"Gender", ["Male", "Female", "Other"], key=f"gender_{i}")
            passengers.append({"first_name": fname, "last_name": lname, "gender": gender})
            st.markdown("---")
            
        c1, c2 = st.columns(2)
        with c1:
            email = st.text_input("Email Address")
        with c2:
            phone = st.text_input("Phone Number")
            
        if st.form_submit_button("Continue to Seats ➔"):
            st.session_state.booking_data['passenger_details'] = passengers
            st.session_state.booking_data['contact'] = {'email': email, 'phone': phone}
            next_step()
            st.rerun()
            
    if st.button("⬅ Back"):
        prev_step()
        st.rerun()

# --- STEP 4: SEAT SELECTION ---
elif st.session_state.step == 4:
    st.markdown("### 💺 Seat Selection")
    
    tab1, tab2 = st.tabs(["Outbound Seats", "Return Seats"])
    
    def render_seat_map(flight_type):
        st.markdown(f"**Select seats for {flight_type} flight**")
        
        # Column Headers
        cols = ["A", "B", "C", "D", "E", "F"]
        
        # Create a header row for column labels
        header_cols = st.columns(7) # 1 for row number, 6 for seats
        with header_cols[0]:
            st.write("") # Spacer
        for idx, c in enumerate(cols):
            with header_cols[idx+1]:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: #666;'>{c}</div>", unsafe_allow_html=True)

        # Mock seat map (6 columns: ABC - DEF)
        rows = 10
        
        selected_seats = st.session_state.booking_data['seats'][flight_type]
        
        # Simple grid for demo
        for r in range(1, rows + 1):
            cols_ui = st.columns(7)
            
            # Row Number
            with cols_ui[0]:
                st.markdown(f"<div style='display: flex; align-items: center; justify-content: center; height: 45px; font-weight: bold; color: #666;'>{r}</div>", unsafe_allow_html=True)
            
            for idx, c in enumerate(cols):
                seat_id = f"{r}{c}"
                is_selected = seat_id in selected_seats
                
                # Mock occupied logic
                is_occupied = (r * idx) % 7 == 0 
                
                # Determine button type/style via key/args, but styling is handled by CSS mostly.
                # Streamlit buttons don't support custom classes directly easily without hacks or component.
                # However, we can use the `type` arg for primary/secondary.
                # But for specific colors (Red/White), we rely on our CSS targeting the button.
                # We need to distinguish Occupied vs Available in CSS.
                # Since we can't add classes to st.button, we might need a workaround or just rely on `disabled` state for occupied.
                # If disabled, it gets a specific class in Streamlit we can target? 
                # Or we use `type="primary"` for selected, `type="secondary"` for available.
                # For occupied, we disable it.
                
                disabled = is_occupied
                btn_type = "primary" if is_selected else "secondary"
                
                # Tooltip via help
                tooltip = f"Seat {seat_id}"
                if is_occupied:
                    tooltip += " (Occupied)"
                elif is_selected:
                    tooltip += " (Selected)"
                else:
                    tooltip += " (Available)"

                # We use a unique key.
                # We use label=" " to make it a square box (styled by CSS).
                # But wait, if we use " ", the text is empty.
                # The user wants to "see the number" while floating. `help` does that.
                
                # CSS HACK: We need to target occupied seats to make them red.
                # Streamlit disabled buttons are grey by default.
                # We can try to inject specific CSS for this specific button ID? No, IDs are dynamic.
                # Alternative: Use `st.markdown` with HTML/CSS for the seat map instead of `st.button`?
                # But `st.button` handles state.
                # Let's stick to `st.button`.
                # We updated CSS `.seat.occupied`. But how to apply `.occupied` class to `st.button`? We can't.
                # We can only style based on `disabled` attribute in CSS.
                # `button:disabled` -> Red.
                
                with cols_ui[idx+1]:
                    if cols_ui[idx+1].button(" " if not is_selected else "✓", 
                                           key=f"{flight_type}_{seat_id}", 
                                           disabled=disabled, 
                                           type=btn_type,
                                           help=tooltip):
                        if is_selected:
                            st.session_state.booking_data['seats'][flight_type].remove(seat_id)
                        else:
                            # Limit selection to num passengers
                            total_pax = st.session_state.booking_data['passengers']['adults'] + st.session_state.booking_data['passengers']['children']
                            if len(st.session_state.booking_data['seats'][flight_type]) < total_pax:
                                st.session_state.booking_data['seats'][flight_type].append(seat_id)
                            else:
                                st.warning(f"You can only select {total_pax} seats.")
                        st.rerun()

    with tab1:
        render_seat_map('outbound')
        st.write(f"Selected: {', '.join(st.session_state.booking_data['seats']['outbound'])}")

    with tab2:
        render_seat_map('return')
        st.write(f"Selected: {', '.join(st.session_state.booking_data['seats']['return'])}")

    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅ Back"):
            prev_step()
            st.rerun()
    with col_next:
        if st.button("Continue to Add-ons ➔"):
            next_step()
            st.rerun()

# --- STEP 5: ADD-ONS ---
elif st.session_state.step == 5:
    st.markdown("### ➕ Add-ons")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 🍱 Meals")
        meal = st.checkbox("Add Veg Meal (₹350/pax)")
        if meal:
            if "Veg Meal" not in st.session_state.booking_data['addons']['meals']:
                st.session_state.booking_data['addons']['meals'].append("Veg Meal")
        else:
             if "Veg Meal" in st.session_state.booking_data['addons']['meals']:
                st.session_state.booking_data['addons']['meals'].remove("Veg Meal")

    with c2:
        st.markdown("#### 🧳 Baggage")
        baggage = st.checkbox("Add Extra 15kg (₹1200)")
        if baggage:
             if "Extra 15kg" not in st.session_state.booking_data['addons']['baggage']:
                st.session_state.booking_data['addons']['baggage'].append("Extra 15kg")
        else:
            if "Extra 15kg" in st.session_state.booking_data['addons']['baggage']:
                st.session_state.booking_data['addons']['baggage'].remove("Extra 15kg")

    st.markdown("#### 🛡️ Insurance")
    insurance = st.checkbox("Add Travel Insurance (₹299/pax)")
    st.session_state.booking_data['addons']['insurance'] = insurance

    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅ Back"):
            prev_step()
            st.rerun()
    with col_next:
        if st.button("Continue to Payment ➔"):
            next_step()
            st.rerun()

# --- STEP 6: PAYMENT ---
elif st.session_state.step == 6:
    st.markdown("### 💳 Payment & Confirmation")
    
    # Calculate Totals
    out_price = st.session_state.booking_data['selected_outbound']['price']
    ret_price = st.session_state.booking_data['selected_return']['price']
    
    addons_cost = 0
    num_pax = st.session_state.booking_data['passengers']['adults'] + st.session_state.booking_data['passengers']['children']
    
    if st.session_state.booking_data['addons']['insurance']:
        addons_cost += 299 * num_pax
    if "Veg Meal" in st.session_state.booking_data['addons']['meals']:
        addons_cost += 350 * num_pax
    if "Extra 15kg" in st.session_state.booking_data['addons']['baggage']:
        addons_cost += 1200
        
    fare_breakdown = pricing.calculate_total_fare(out_price, ret_price, st.session_state.booking_data['passengers'], addons_cost)
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("#### Flight Summary")
        st.info(f"**Outbound**: {st.session_state.booking_data['selected_outbound']['airline']} | {st.session_state.booking_data['selected_outbound']['flight_number']}")
        st.info(f"**Return**: {st.session_state.booking_data['selected_return']['airline']} | {st.session_state.booking_data['selected_return']['flight_number']}")
        
        st.markdown("#### Passenger Details")
        for p in st.session_state.booking_data['passenger_details']:
            st.write(f"- {p['first_name']} {p['last_name']} ({p['gender']})")
            
        st.markdown("#### Payment Method")
        pay_method = st.radio("Select Payment Method", ["Credit/Debit Card", "UPI", "Net Banking"], horizontal=True)
        
        if pay_method == "Credit/Debit Card":
            cc1, cc2 = st.columns(2)
            cc1.text_input("Card Number")
            cc2.text_input("CVV", type="password")
        elif pay_method == "UPI":
            st.text_input("UPI ID")
            
    with c2:
        st.markdown("#### Fare Breakdown")
        st.write(f"Base Fare: {utils.format_currency(fare_breakdown['base_fare'])}")
        st.write(f"Taxes & Fees: {utils.format_currency(fare_breakdown['convenience_fee'] + fare_breakdown['psf'] + fare_breakdown['fuel_surcharge'] + fare_breakdown['gst'])}")
        st.write(f"Add-ons: {utils.format_currency(fare_breakdown['addons'])}")
        st.markdown("---")
        st.markdown(f"### Total: {utils.format_currency(fare_breakdown['total'])}")
        
        if st.button("Pay & Book ➔", type="primary", use_container_width=True):
            st.success("Booking Confirmed! 🎉")
            st.balloons()
            pnr = utils.generate_pnr()
            st.markdown(f"### PNR: `{pnr}`")
            st.write("Your e-ticket has been sent to your email.")
            
            # PDF Download
            pdf_bytes = utils.generate_ticket_pdf(st.session_state.booking_data, pnr, fare_breakdown)
            st.download_button(
                label="📄 Download Ticket PDF",
                data=pdf_bytes,
                file_name=f"SkyConnect_Ticket_{pnr}.pdf",
                mime="application/pdf",
                type="primary"
            )
            
            # Reset button
            if st.button("Book Another Flight"):
                st.session_state.step = 1
                st.rerun()

    if st.button("⬅ Back"):
        prev_step()
        st.rerun()
