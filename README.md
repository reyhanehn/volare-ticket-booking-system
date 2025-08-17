# Volare: The Ultimate Ticket Booking System

Welcome to Volare, a comprehensive ticket booking platform designed to make travel seamless and enjoyable. Whether it's a **ticket, billet, boletos, or biglietto**, our platform has you covered. Built with a robust and modular backend, this system handles the entire lifecycle of a travel booking, from user authentication to trip completion.

-----

### ✨ Key Features

  * **Advanced User Management:** Secure user registration and profile management with a dedicated wallet system. Authentication options include JWT for both password-based and OTP-based login.
  * **Comprehensive Booking Engine:** Users can search for trips, reserve seats, and process payments. The system also manages cancellations and refunds based on predefined penalty rules.
  * **Multi-Role System:** The platform supports distinct user roles with specific permissions:
      * **Customer:** Can search for tickets, manage their profile, make reservations, and submit reports.
      * **Company Owner:** Can manage their transportation company, register vehicles, define services, and create trips and tickets.
      * **Admin:** Has full oversight of the system, including managing companies, services, locations, routes, and user-submitted reports.
  * **Company & Vehicle Management:** An easy-to-use interface for transportation companies to manage their fleet (planes, trains, and buses) and services.
  * **Reporting System:** A straightforward way for users to report issues, with a dedicated system for admins to track and resolve them.
  * **Optimized Performance:** Uses **Redis** for caching frequently accessed data and managing OTPs, ensuring a speedy and responsive user experience.
  * **Asynchronous Task Handling:** **Celery** manages background tasks, such as automatically canceling unpaid reservations after their expiration time.

-----

### 🏛️ Project Architecture

The backend is built with **Django REST Framework** and follows a modular design, separating the logic into four distinct applications for better maintainability and scalability.

  * **accounts:** Manages user identity, authentication, profiles, wallets, and financial transactions.
  * **companies:** Handles all aspects of transportation providers, including company profiles, vehicle fleets, and services.
  * **bookings:** The core of the platform, orchestrating the entire booking process from defining locations and routes to managing tickets, reservations, and payments.
  * **reports:** Provides the functionality for user feedback and administrative issue resolution.

-----

### 🗂️ Database Schema

Our database is built on **PostgreSQL**, with a logical schema organized within their respective applications.

**Accounts App**

  * **Account:** Stores user profiles, authentication details, and roles.
  * **Wallet:** Manages user financial balances.
  * **Wallet\_Transactions:** Records all financial transactions.

**Companies App**

  * **Company:** Details of transportation companies.
  * **Vehicle:** Information on vehicles (trains, buses, airplanes).
  * **Vehicle\_Section:** Defines vehicle sections (e.g., First Class, Economy) and seat capacity.
  * **Service:** A list of available services (e.g., Wi-Fi, Meal).
  * **Vehicle\_Service:** Links vehicles to their provided services.

**Bookings App**

  * **Location:** Stores countries and cities.
  * **Station:** Represents specific travel stations.
  * **Route:** Defines travel paths between stations.
  * **Trip:** Represents a specific scheduled journey.
  * **Trip\_Stop:** Stores information about intermediate stops.
  * **Ticket:** A purchasable unit for a trip.
  * **Passenger:** Stores passenger information.
  * **Reservation:** Represents a user's booking with a status (e.g., Pending, Confirmed).
  * **Payment:** Records the financial transaction for a reservation.

**Reports App**

  * **Report:** Stores user-submitted reports and administrative responses.

-----

### 💻 Tech Stack

  * **Backend:** Django REST Framework
  * **Database:** PostgreSQL
  * **Caching & OTP:** Redis
  * **Authentication:** JWT (JSON Web Tokens)
  * **Asynchronous Tasks:** Celery
  * **Programming Language:** Python

-----

### 🚀 Getting Started

#### Prerequisites

  * Python
  * pip
  * PostgreSQL
  * Redis

#### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/reyhanehn/volare-ticket-booking-system.git
    cd volare-ticket-booking-system
    git checkout server
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up the database:**
    Connect to your PostgreSQL instance and run the `create_tables_second_try.sql` script.
4.  **Configure environment variables:**
    Create a `.env` file in the root directory of each of the four apps (`accounts`, `bookings`, `companies`, `reports`) and add your database and Redis connection details.
5.  **Run the Django server:**
    ```bash
    cd volare
    python manage.py runserver
    ```
6.  **Start Celery for background tasks:**
    Open two new terminals in the `volare` directory.
    ```bash
    # Terminal 2: Celery Worker
    celery -A volare worker --pool=solo --loglevel=info
    ```
    ```bash
    # Terminal 3: Celery Beat (Scheduler)
    celery -A volare beat --loglevel=info
    ```

-----

### 🤝 Contributors

  * Hedie Tahmouresi
  * Ali Alavi Nikoo
  * Reyhane Nemati

*Made with ❤️ and a love for travel\!*
