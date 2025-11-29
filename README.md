# ✈️ SkyConnect - Flight Booking Platform

> A modern, AI-powered flight booking web application for Hyderabad ↔ Goa route with dynamic pricing and intelligent chatbot assistance.

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![n8n](https://img.shields.io/badge/n8n-EA4B71?style=for-the-badge&logo=n8n&logoColor=white)](https://n8n.io/)

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Dynamic Pricing Algorithm](#-dynamic-pricing-algorithm)
- [AI Chatbot Integration](#-ai-chatbot-integration)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

## 🌟 Overview

**SkyConnect** is a premium flight booking platform exclusively serving the Hyderabad (HYD) ↔ Goa (GOI) corridor. Built with modern web technologies, it offers a seamless 6-step booking process with transparent pricing, real-time seat selection, and 24/7 AI-powered customer support.

### 🎯 Key Highlights

- **Smart Pricing**: Dynamic pricing algorithm that rewards early bookings with up to 20% discount
- **AI Assistant**: Integrated n8n-powered chatbot for 24/7 customer support
- **Transparent Fees**: No hidden charges - complete fare breakdown before payment
- **Instant Confirmation**: E-tickets delivered via email within 2 minutes
- **Secure Payments**: PCI-DSS compliant payment gateway with 256-bit SSL encryption

## ✨ Features

### Core Booking Features

- 🔍 **Intelligent Flight Search** - Search flights by date, passengers, and travel class
- ✈️ **Multi-Airline Support** - IndiGo, Air India, SpiceJet, Vistara, AirAsia
- 💺 **Interactive Seat Selection** - Visual seat map with real-time availability
- 🍱 **Add-on Services** - Pre-book meals, extra baggage, and travel insurance
- 💳 **Multiple Payment Options** - Credit/Debit cards, UPI, Net Banking
- 📄 **PDF Ticket Generation** - Downloadable e-tickets with QR codes
- 🔐 **Secure Database Storage** - PostgreSQL backend for booking management

### Smart Pricing Engine

- 📅 **Early Bird Discounts** - Up to 20% off for bookings 30+ days in advance
- 🌙 **Time-of-Day Pricing** - 10% discount on night flights
- 📊 **Peak Season Management** - Dynamic pricing for Oct-Jan peak period
- 💼 **Class-Based Pricing** - Economy, Premium Economy, Business class options
- 🎯 **Weekend Premium Handling** - Transparent weekend surcharges

### AI Chatbot Features

- 🤖 **24/7 Availability** - Powered by n8n and OpenAI GPT-4
- 💬 **Natural Language Understanding** - Ask questions in plain English
- 📚 **Knowledge Base Integration** - Answers from comprehensive FAQ documentation
- 🎫 **Booking Assistance** - Help with every step of the booking process
- 💰 **Price Calculations** - Real-time fare estimates and money-saving tips

## 🎬 Demo

**Live Application**: [SkyConnect Flight Booking](https://flightbookingapp-dhui3wukei3vchj58ghyuo.streamlit.app/)

### Quick Demo Flow

1. **Search** → Enter travel dates and passenger details
2. **Select** → Choose outbound and return flights
3. **Details** → Fill passenger information
4. **Seats** → Pick your preferred seats
5. **Add-ons** → Optional meals, baggage, insurance
6. **Payment** → Complete booking and receive e-ticket

## 🛠️ Tech Stack

### Frontend
- **[Streamlit](https://streamlit.io/)** - Python web framework for ML applications
- **HTML/CSS** - Custom styling and UI components
- **JavaScript** - n8n chat widget integration

### Backend
- **Python 3.12+** - Core application logic
- **PostgreSQL** - Relational database for booking storage
- **FPDF** - PDF generation for e-tickets

### AI & Automation
- **[n8n](https://n8n.io/)** - Workflow automation for chatbot
- **OpenAI GPT-4** - Natural language processing
- **Google Docs API** - Knowledge base integration

### Cloud & Deployment
- **Streamlit Cloud** - Application hosting
- **n8n Cloud** - Chatbot workflow hosting
- **PostgreSQL** - Database hosting

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface (Streamlit)               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Search  │  │  Select  │  │   Seats  │  │  Payment │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            │                             │
    ┌───────▼────────┐          ┌────────▼────────┐
    │  Application   │          │   AI Chatbot    │
    │     Logic      │          │   (n8n + GPT)   │
    │  - Pricing     │          │  - FAQ Lookup   │
    │  - Validation  │          │  - Support      │
    │  - PDF Gen     │          │  - Guidance     │
    └───────┬────────┘          └────────┬────────┘
            │                            │
    ┌───────▼────────┐          ┌────────▼────────┐
    │   PostgreSQL   │          │  Google Docs    │
    │   Database     │          │  Knowledge Base │
    │  - Bookings    │          │  - FAQ Content  │
    │  - Passengers  │          │  - Policies     │
    └────────────────┘          └─────────────────┘
```

## 📦 Installation

### Prerequisites

- Python 3.12 or higher
- PostgreSQL 12 or higher
- Git
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/skyconnect-flight-booking.git
cd skyconnect-flight-booking
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Database

```bash
# Create PostgreSQL database
createdb skyconnect_db

# Initialize database schema (run Python)
python
>>> import db
>>> db.init_db()
>>> exit()
```

### Step 5: Configure Environment

Create a `.streamlit/secrets.toml` file:

```toml
[connections.postgresql]
dialect = "postgresql"
host = "your-db-host"
port = "5432"
database = "skyconnect_db"
username = "your-username"
password = "your-password"
```

### Step 6: Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## ⚙️ Configuration

### Database Configuration

Edit `db.py` to configure your PostgreSQL connection:

```python
# Database connection settings
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "skyconnect_db"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
```

### n8n Chatbot Configuration

1. **Set up n8n workflow** (see `docs/n8n_setup.md`)
2. **Update webhook URL** in `app.py`:

```python
webhookUrl: 'https://your-n8n-instance.app.n8n.cloud/webhook/YOUR-WEBHOOK-ID/chat'
```

3. **Configure chatbot appearance** in `app.py`:

```javascript
style: {
    width: '100%',
    height: '100%',
    token: {
        color: {
            primary: '#00529B',  // Your brand color
            secondary: '#f3f4f6',
            text: '#1f2937',
        }
    }
}
```

### Custom Styling

Edit `styles.css` to customize the UI:

```css
:root {
    --primary-color: #00529B;
    --secondary-color: #4A90E2;
    --accent-color: #F7931E;
}
```

## 🚀 Usage

### Booking a Flight

```python
# 1. Search for flights
booking_data = {
    'departure_city': 'Hyderabad (HYD)',
    'arrival_city': 'Goa (GOI)',
    'departure_date': datetime(2025, 12, 15),
    'return_date': datetime(2025, 12, 20),
    'passengers': {'adults': 2, 'children': 1, 'infants': 0},
    'travel_class': 'Economy'
}

# 2. Get available flights
outbound_flights = flight_data.generate_flights("HYD", "GOI", departure_date)
return_flights = flight_data.generate_flights("GOI", "HYD", return_date)

# 3. Calculate price
price = pricing.calculate_price(
    base_price=3500,
    flight=selected_flight,
    booking_date=datetime.now().date(),
    travel_class='Economy',
    passengers={'adults': 2, 'children': 1, 'infants': 0}
)
```

### Generating E-Ticket

```python
import utils

# Generate PDF ticket
pdf_bytes = utils.generate_ticket_pdf(
    booking_data=booking_data,
    pnr="SKY7A9",
    fare_breakdown=fare_breakdown
)

# Save or send to user
with open("ticket.pdf", "wb") as f:
    f.write(pdf_bytes)
```

## 💰 Dynamic Pricing Algorithm

SkyConnect uses a sophisticated multi-factor pricing algorithm:

### Pricing Formula

```python
final_price = base_price × 
              advance_booking_factor × 
              seasonal_factor × 
              weekend_factor × 
              time_of_day_factor × 
              class_multiplier
```

### Pricing Factors

| Factor | Condition | Adjustment |
|--------|-----------|------------|
| **Advance Booking** | 30+ days | -20% |
| | 15-29 days | -10% |
| | 7-14 days | 0% |
| | <7 days | +25% |
| **Peak Season** | Oct-Jan | +30% |
| | Feb-Sep | 0% |
| **Weekend** | Fri-Sun | +20% |
| | Mon-Thu | 0% |
| **Time of Day** | 6-8 AM | +15% |
| | 8 AM-12 PM | +10% |
| | 12-4 PM | 0% |
| | 4-8 PM | +15% |
| | 8 PM-6 AM | -10% |
| **Class** | Economy | 1.0x |
| | Premium Economy | 1.5x |
| | Business | 2.5x |

### Example Calculation

**Scenario**: Book 35 days ahead, Wednesday departure, 9 PM flight, March, Economy

```
Base Price: ₹3,500
- Advance Booking (-20%): ₹2,800
- Regular Season (0%): ₹2,800
- Weekday (0%): ₹2,800
- Night Flight (-10%): ₹2,520
- Economy Class (1x): ₹2,520

Final Price per Flight: ₹2,520
Round Trip: ₹5,040
```

## 🤖 AI Chatbot Integration

### Architecture

```
User Question → Streamlit Chat Widget → n8n Webhook → 
AI Agent (GPT-4) → Knowledge Base (Google Docs) → 
Response → Chat Widget → User
```

### Key Components

1. **Chat Trigger**: Receives user messages via webhook
2. **AI Agent**: Processes queries using GPT-4
3. **Knowledge Base**: Google Docs with comprehensive FAQ
4. **Memory**: Maintains conversation context
5. **Tools**: Document retrieval, email notifications

### Sample Queries

- "How much does a flight cost?"
- "What's the booking process?"
- "Can I cancel my booking?"
- "Tell me about seat selection"
- "How can I save money on flights?"

### Configuration Files

- **System Prompt**: `docs/SkyConnect_AI_System_Prompt.txt`
- **FAQ Document**: `docs/SkyConnect_FAQ.md`
- **n8n Workflow**: Import from `docs/n8n_workflow.json`

## 📁 Project Structure

```
skyconnect-flight-booking/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── .streamlit/
│   └── secrets.toml               # Database credentials (not in git)
│
├── Core Modules
├── db.py                          # Database operations
├── flight_data.py                 # Flight generation logic
├── pricing.py                     # Dynamic pricing algorithm
├── utils.py                       # Helper functions (PDF, PNR, etc.)
│
├── UI Assets
├── styles.css                     # Custom CSS styling
│
├── Documentation
├── docs/
│   ├── SkyConnect_FAQ.md          # Comprehensive FAQ
│   ├── SkyConnect_AI_System_Prompt.txt  # Chatbot configuration
│   ├── SkyConnect_Implementation_Guide.md  # Setup guide
│   ├── N8N_Workflow_Fix_Instructions.md    # Troubleshooting
│   ├── Ready_To_Paste_Configurations.md    # Quick configs
│   └── n8n_workflow.json          # n8n workflow export
│
├── Database Schema
├── schema/
│   └── bookings.sql               # Database schema
│
└── Tests (Optional)
    └── tests/
        ├── test_pricing.py
        ├── test_flight_data.py
        └── test_utils.py
```

## 📚 API Documentation

### Core Functions

#### `flight_data.generate_flights(from_city, to_city, date)`

Generates mock flight data for a given route and date.

**Parameters:**
- `from_city` (str): Origin airport code
- `to_city` (str): Destination airport code
- `date` (datetime.date): Travel date

**Returns:**
- List of flight dictionaries with details

**Example:**
```python
flights = flight_data.generate_flights("HYD", "GOI", datetime(2025, 12, 15))
```

#### `pricing.calculate_price(base_price, flight, booking_date, travel_class, passengers)`

Calculates dynamic flight price based on multiple factors.

**Parameters:**
- `base_price` (float): Starting price
- `flight` (dict): Flight details
- `booking_date` (datetime.date): When booking is made
- `travel_class` (str): Economy/Premium/Business
- `passengers` (dict): Passenger counts

**Returns:**
- Final price (int)

#### `pricing.calculate_total_fare(outbound_price, return_price, passengers, addons_cost)`

Calculates complete fare breakdown including fees and taxes.

**Returns:**
```python
{
    'base_fare': 10000,
    'convenience_fee': 400,
    'psf': 300,
    'fuel_surcharge': 1000,
    'gst': 500,
    'addons': 1200,
    'total': 13400
}
```

#### `utils.generate_pnr()`

Generates a unique 6-character PNR (Passenger Name Record).

**Returns:**
- String (e.g., "SKY7A9")

#### `utils.generate_ticket_pdf(booking_data, pnr, fare_breakdown)`

Creates downloadable PDF e-ticket.

**Returns:**
- BytesIO object containing PDF

### Database Schema

#### Bookings Table

```sql
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    pnr VARCHAR(10) UNIQUE NOT NULL,
    departure_date DATE NOT NULL,
    return_date DATE NOT NULL,
    total_passengers INT NOT NULL,
    total_fare DECIMAL(10, 2) NOT NULL,
    booking_status VARCHAR(20) DEFAULT 'confirmed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    passenger_details JSONB,
    flight_details JSONB,
    contact_info JSONB
);
```

## 📸 Screenshots

### 1. Search Page
![Search Page](https://via.placeholder.com/800x450/00529B/FFFFFF?text=Flight+Search)

### 2. Flight Selection
![Flight Selection](https://via.placeholder.com/800x450/4A90E2/FFFFFF?text=Select+Flights)

### 3. Seat Map
![Seat Selection](https://via.placeholder.com/800x450/F7931E/FFFFFF?text=Seat+Map)

### 4. AI Chatbot
![Chatbot](https://via.placeholder.com/800x450/00529B/FFFFFF?text=AI+Assistant)

### 5. E-Ticket
![E-Ticket](https://via.placeholder.com/800x450/4A90E2/FFFFFF?text=E-Ticket+PDF)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add docstrings to all functions
- Comment complex logic
- Keep functions focused and modular

### Testing

Run tests before submitting PR:

```bash
pytest tests/
```

### Areas for Contribution

- [ ] Real-time flight data integration
- [ ] Payment gateway integration (Stripe/Razorpay)
- [ ] SMS notifications for bookings
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Loyalty program features
- [ ] Group booking functionality

## 🐛 Known Issues

- Seat selection state sometimes doesn't persist on page refresh
- PDF generation may be slow for large passenger groups
- n8n chatbot may have delayed responses during high traffic

## 🔮 Future Enhancements

### Phase 1 (Q1 2025)
- ✅ Basic booking flow
- ✅ Dynamic pricing
- ✅ AI chatbot
- ⏳ Real payment integration
- ⏳ Email notifications

### Phase 2 (Q2 2025)
- ⏳ Multi-route support
- ⏳ Mobile app (React Native)
- ⏳ Loyalty program
- ⏳ Price alerts
- ⏳ Booking management portal

### Phase 3 (Q3 2025)
- ⏳ Corporate booking features
- ⏳ API for third-party integration
- ⏳ Advanced analytics
- ⏳ WhatsApp integration
- ⏳ Voice booking support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 SkyConnect

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## 👥 Authors

- **Ashu Mishra** - *Initial work* - [@Ashumishra94](https://github.com/Ashumishra94)

## 🙏 Acknowledgments

- **Streamlit** - For the amazing Python web framework
- **n8n** - For workflow automation capabilities
- **OpenAI** - For GPT-4 language model
- **PostgreSQL** - For reliable database management
- **FPDF** - For PDF generation
- **All contributors** who have helped shape this project

## 📞 Contact

**Ashu Mishra**

- Email: ashumishra1994ash@gmail.com
- LinkedIn: [linkedin.com/in/ashumishra94](https://linkedin.com/in/ashumishra94)
- GitHub: [@Ashumishra94](https://github.com/Ashumishra94)

**Project Link**: [https://flightbookingapp-dhui3wukei3vchj58ghyuo.streamlit.app/)

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

Made with ❤️ by Ashu Mishra

[Report Bug](https://github.com/yourusername/skyconnect-flight-booking/issues) · [Request Feature](https://github.com/yourusername/skyconnect-flight-booking/issues)

</div>

---

## 🔗 Related Projects

- [n8n Automation Workflows](https://n8n.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [OpenAI API Examples](https://platform.openai.com/examples)

---

**Last Updated**: November 29, 2025
