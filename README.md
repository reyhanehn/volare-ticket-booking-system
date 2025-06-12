# Volare Ticket Booking System 🎟️

This is a ticket booking system built with **Django REST Framework**, designed for managing trips, tickets, reservations, payments, and user accounts across different transportation types like buses, trains, and airplanes.

---

## 🧭 Project Structure

The project is divided into four core Django apps:

### 1. `accounts`  
Manages user accounts, authentication, and wallet systems.

- **Models**:  
  - `Account` (custom user model)  
  - `Wallet`  
  - `WalletTransactions`

### 2. `companies`  
Handles companies, their vehicles, and services.

- **Models**:  
  - `Company`  
  - `Vehicle`  
  - `VehicleSection`  
  - `Service`  
  - `VehicleService`

### 3. `bookings`  
Covers all aspects of the booking lifecycle including trips, tickets, locations, and reservations.

- **Models**:  
  - `Location`, `Station`  
  - `Route`, `Trip`, `TripStop`  
  - `Ticket`  
  - `Reservation`, `Passenger`, `Payment`

### 4. `report`  
Manages user-submitted reports and admin resolutions.

- **Model**:  
  - `Report`

---

## 🔐 Authentication APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/accounts/send-otp/` | Send login OTP |
| POST | `/api/accounts/verify-otp/` | Verify OTP |
| POST | `/api/accounts/refresh-otp/` | Refresh OTP |
| POST | `/api/accounts/login/` | Login using OTP |
| POST | `/api/accounts/register/` | Register new user |
| POST | `/api/accounts/send-jwt-token/` | Send JWT token after registration |

---

## 👤 User Profile APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/profile/` | Get user profile |
| PUT | `/api/accounts/profile/` | Update full profile |
| PATCH | `/api/accounts/profile/` | Partial update |
| GET | `/api/accounts/transactions/` | Wallet transactions |
| GET | `/api/accounts/wallet/` | Wallet details |
| POST | `/api/accounts/wallet/charge/` | Charge wallet (creates transaction) |

---

## 🏢 Company and Vehicle Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/companies/create/` | Create a company |
| GET | `/api/companies/my-company/` | View logged-in company info |
| PUT | `/api/companies/my-company/` | Update company details |
| POST | `/api/vehicles/create/` | Create vehicle and sections |
| POST | `/api/vehicles/<vehicle_id>/sections/` | Add sections to vehicle |
| POST | `/api/vehicles/<vehicle_id>/services/` | Add services to vehicle |
| GET | `/api/vehicles/<vehicle_id>/` | Get full vehicle details |

---

## 📍 Location and Station Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/locations/create/` | Add new location |
| GET | `/api/locations/` | List locations |
| POST | `/api/stations/create/` | Add new station |
| GET | `/api/stations/` | List stations |

---

## 🛣️ Route and Trip Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/routes/create/` | Create a new route |
| GET | `/api/routes/search/` | Search routes |
| POST | `/api/trips/create/` | Create trip with tickets |
| POST | `/api/trips/<trip_id>/tickets/` | Add tickets to trip |
| POST | `/api/trips/<trip_id>/stops/` | Add stops to trip |
| GET | `/api/trips/search/` | Search trips |
| GET | `/api/tickets/<ticket_id>/` | Ticket detail by ID |

---

## 🧍 Passenger and Reservation Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/passengers/create/` | Create passenger |
| GET | `/api/passengers/my-passenger/` | Get own passenger info |
| PUT | `/api/passengers/my-passenger/` | Update own passenger info |
| GET | `/api/passengers/` | List all passengers |
| POST | `/api/reservations/create/` | Create a reservation |
| GET | `/api/reservations/my/` | Get current user's reservations |
| POST | `/api/reservations/<id>/cancel-preview/` | Preview refund for cancel |
| POST | `/api/reservations/<id>/cancel/` | Confirm cancel reservation |

---

## 💰 Payments

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/payments/pay/` | Pay for reservation |
| GET | `/api/payments/<reservation_id>/status/` | Check payment status |
| GET | `/api/payments/history/` | View user's payment history (filterable) |

---

## 📢 Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/report/submit/` | Submit a report |
| GET | `/api/report/my/` | View own reports |

---

## 🛡️ Admin APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admins/service/` | Create a new service (admin only) |
| POST | `/api/admin/reservations/<id>/cancel/` | Admin cancels reservation (full refund) |
| POST | `/api/admin/reservations/cleanup/` | Cancel expired unpaid reservations |
| POST | `/api/admin/trips/<trip_id>/cancel/` | Cancel entire trip and refund all |
| PUT | `/api/admin/tickets/<ticket_id>/edit/` | Edit ticket info (price etc.) |
| PUT | `/api/admin/tickets/<ticket_id>/cancel/` | Cancel a specific ticket |
| PUT | `/api/admin/trips/<trip_id>/edit/` | Edit trip (e.g. date/time) |
| GET | `/api/admin/report/manage/` | View all unresolved reports |
| PUT | `/api/admin/report/<id>/resolve/` | Resolve a specific report |
| GET | `/api/admin/reservations/manage/` | View all reservations (admin scope) |
| PUT | `/api/admin/reservations/<id>/edit/` | Edit reservation (seat number etc.) |

---

## 📦 Technologies Used

- Python 3.10+
- Django 5+
- Django REST Framework
- PostgreSQL
- Redis (for caching)
- HTML Email Templates
- Raw SQL for optimized performance

---


# Running The Project
# Clone the repo
git clone https://github.com/yourusername/volare-ticket-booking-system.git
cd volare-ticket-booking-system

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Contact


Let me know if you'd like this in a downloadable file or want to modify/add deployment instructions, license, or database schema!

