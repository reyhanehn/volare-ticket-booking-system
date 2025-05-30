--ENUMS
CREATE TYPE account_role AS ENUM ('Customer', 'Admin', 'Company_Owner');
CREATE TYPE account_status AS ENUM ('Active', 'Banned');
CREATE TYPE payment_method AS ENUM ('Credit Card','PayPal','Bank Transfer','Cash', 'Wallet');
CREATE TYPE payment_status AS ENUM ('Pending','Completed','Failed','Refunded');
CREATE TYPE transaction_type AS ENUM ('Charge', 'Payment', 'Refund');
CREATE TYPE station_type AS ENUM ('Train_Station', 'Bus_Station', 'Airport');
CREATE TYPE transport_type AS ENUM ('Train', 'Bus', 'Airplane');
CREATE TYPE stop_type AS ENUM ('Transit', 'Meal', 'Refuel', 'Layover');
CREATE TYPE reservation_status AS ENUM ('Pending', 'Confirmed', 'Cancelled');
CREATE TYPE report_status AS ENUM ('Pending', 'Checked');
CREATE TYPE report_type AS ENUM ('Reservation', 'Payment', 'Ticket');

-- location
CREATE TABLE Location (
    Location_ID SERIAL PRIMARY KEY,
    Country VARCHAR(50) NOT NULL CHECK (Country ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
    City VARCHAR(50) NOT NULL CHECK (City ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
    UNIQUE(Country, City)
);

-- Account
CREATE TABLE Account (
  Account_ID BIGSERIAL PRIMARY KEY,
  Phone_Number VARCHAR(15) UNIQUE CHECK (
      Phone_Number ~ '^((\+98)|(0))9\d{2}\d{7}$' OR Phone_Number IS NULL
  ),
  Email VARCHAR(100) UNIQUE CHECK (
      Email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' OR Email IS NULL
  ),
  Name VARCHAR(50) NOT NULL CHECK (Name ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
  Lastname VARCHAR(50) NOT NULL CHECK (Lastname ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
  Role account_role NOT NULL,
  Status account_status NOT NULL DEFAULT 'Active',
  Password_Hash TEXT NOT NULL,
  City_ID BIGINT REFERENCES Location(Location_ID) ON DELETE SET NULL,
  Registration_Date DATE NOT NULL DEFAULT CURRENT_DATE,
  Birth_Date DATE,
  CONSTRAINT at_least_one_not_null CHECK (
      Email IS NOT NULL OR Phone_Number IS NOT NULL
  )
);

-- Company
CREATE TABLE Company (
  Company_ID BIGSERIAL PRIMARY KEY,
  Owner BIGINT REFERENCES Account(Account_ID) ON DELETE CASCADE,
  Name VARCHAR(50) NOT NULL UNIQUE CHECK (Name ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
  Logo_URL TEXT,
  Website TEXT,
  Rating NUMERIC
);

-- Vehicle
CREATE TABLE Vehicle (
  Vehicle_ID BIGSERIAL PRIMARY KEY,
  Company_ID BIGINT REFERENCES Company(Company_ID) ON DELETE CASCADE,
  Name VARCHAR(50),
  Type transport_type NOT NULL,
  Class_Code SMALLINT NOT NULL CHECK (Class_Code BETWEEN 1 AND 5),
  Total_Seats INT NOT NULL CHECK (Total_Seats > 0),
  Layout VARCHAR(15) -- basically all the layouts like 1 + 2 for bus? or 15 + 5 for train and ...
);

CREATE TABLE Vehicle_Section (
  Section_ID BIGSERIAL PRIMARY KEY,
  Vehicle_ID BIGINT REFERENCES Vehicle(Vehicle_ID) ON DELETE CASCADE,
  Name VARCHAR(20), -- it specifies which section like first class and stuff?
  Seats_Count INT NOT NULL CHECK (Seats_Count > 0)
);

-- Service
CREATE TABLE Service (
  Service_ID SERIAL PRIMARY KEY,
  Name VARCHAR(50) UNIQUE NOT NULL
);

-- Junction table for Vehicle and Service
CREATE TABLE Vehicle_Service (
  Vehicle_ID BIGINT REFERENCES Vehicle(Vehicle_ID) ON DELETE CASCADE,
  Service_ID INT REFERENCES Service(Service_ID) ON DELETE CASCADE,
  PRIMARY KEY (Vehicle_ID, Service_ID)
);

-- Station
CREATE TABLE Station (
    Station_ID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL CHECK (Name ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
    Type station_type NOT NULL,
    Location_ID INT REFERENCES Location(Location_ID) ON DELETE CASCADE,
    UNIQUE(Name, Location_ID)
);

-- Route
CREATE TABLE Route (
  Route_ID BIGSERIAL PRIMARY KEY,
  Origin INT NOT NULL REFERENCES Location(Location_ID) ON DELETE CASCADE,
  Destination INT NOT NULL REFERENCES Location(Location_ID) ON DELETE CASCADE,
  Origin_Station INT REFERENCES Station(Station_ID) ON DELETE CASCADE,
  Destination_Station INT REFERENCES Station(Station_ID) ON DELETE CASCADE,
  CONSTRAINT different_origin_and_station
    CHECK (Origin <> Destination)
);

-- Trip
CREATE TABLE Trip (
  Trip_ID BIGSERIAL PRIMARY KEY,
  Vehicle_ID BIGINT NOT NULL REFERENCES Vehicle(Vehicle_ID) ON DELETE CASCADE,
  Route_ID BIGINT NOT NULL REFERENCES Route(Route_ID) ON DELETE CASCADE,
  Departure_DateAndTime TIMESTAMP,
  Duration INTERVAL,
  Remaining_Sections SMALLINT NOT NULL CHECK (Remaining_Sections >= 0),
  Remaining_Capacity SMALLINT NOT NULL CHECK (Remaining_Capacity >= 0)
);

-- Ticket (this specifies the section of the vehicle)
CREATE TABLE Ticket (
  Ticket_ID BIGSERIAL PRIMARY KEY,
  Trip_ID BIGINT REFERENCES Trip(Trip_ID) ON DELETE CASCADE,
  Section_ID BIGINT NOT NULL REFERENCES Vehicle_Section(Section_ID) ON DELETE CASCADE,
  Price DECIMAL(10,2) NOT NULL CHECK (Price > 0),
  Remaining_Seats SMALLINT DEFAULT 0,
  Seat_Start_Number SMALLINT DEFAULT 0,
  Seat_End_Number SMALLINT DEFAULT 0
);

-- Junction table for each Trip and their Stops
CREATE TABLE Trip_Stop (
  Trip_ID BIGINT REFERENCES Trip(Trip_ID) ON DELETE CASCADE,
  Stop_Order SMALLINT NOT NULL,
  Stop_Type stop_type NOT NULL,
  Station_ID BIGINT REFERENCES Station(Station_ID),
  Duration INTERVAL,
  PRIMARY KEY (Trip_ID, Stop_Order)
);

-- Passenger
CREATE TABLE Passenger (
  Passenger_ID BIGSERIAL PRIMARY KEY,
  Name VARCHAR(50) NOT NULL CHECK (Name ~ '^[A-Za-z]+(\s[A-Za-z]+)*$')
  ,
  Lastname VARCHAR(50) NOT NULL CHECK (Lastname ~ '^[A-Za-z]+(\s[A-Za-z]+)*$')
  ,
  SSN VARCHAR(10) UNIQUE CHECK (
      SSN ~ '^\d{10}$'
  ),
  Birthdate DATE NOT NULL CHECK (Birthdate <= CURRENT_DATE),
  Picture_URL TEXT CHECK (Picture_URL ~* '^https?://.+\.(jpg|jpeg|png|gif)$'),
  Related_Account_ID BIGINT REFERENCES Account(Account_ID)
);

-- Reservation
CREATE TABLE Reservation (
  Reservation_ID BIGSERIAL PRIMARY KEY,
  Account_ID BIGINT NOT NULL REFERENCES Account(Account_ID) ON DELETE CASCADE,
  --the account who reserved it
  Passenger_ID BIGINT NOT NULL REFERENCES Passenger (Passenger_ID) ON DELETE CASCADE,
  -- the passenger whom the reservation is for
  Ticket_ID BIGINT NOT NULL REFERENCES Ticket(Ticket_ID) ON DELETE CASCADE,
  Seat_Number VARCHAR(10) NOT NULL CHECK (Seat_Number ~ '^[0-9]{1,2}[A-Z]$'),
  Status reservation_status NOT NULL DEFAULT 'Pending',
  Reservation_Date DATE NOT NULL DEFAULT CURRENT_DATE,
  Reservation_Time TIME NOT NULL DEFAULT CURRENT_TIME,
  Expiration INTERVAL NOT NULL,
  Cncelled_By BIGINT REFERENCES Account(Account_ID),
  UNIQUE(Ticket_ID, Seat_Number)
);

-- Payment
CREATE TABLE Payment (
  Payment_ID BIGSERIAL PRIMARY KEY,
  Account_ID BIGINT NOT NULL REFERENCES Account(Account_ID) ON DELETE CASCADE,
  Reservation_ID BIGINT NOT NULL UNIQUE REFERENCES Reservation(Reservation_ID) ON DELETE CASCADE,
  Amount DECIMAL(10,2) NOT NULL CHECK (Amount > 0),
  Payment_Method payment_method NOT NULL,
  Status payment_status NOT NULL DEFAULT 'Pending',
  Payment_Time TIME NOT NULL DEFAULT CURRENT_TIME,
  Payment_Date DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Wallet
CREATE TABLE Wallet (
  Wallet_ID BIGSERIAL PRIMARY KEY,
  Account_ID BIGINT NOT NULL UNIQUE REFERENCES Account(Account_ID) ON DELETE CASCADE,
  Balance DECIMAL(10,2) NOT NULL CHECK (Balance >= 0)
);

-- Wallet Transactions
CREATE TABLE Wallet_Transactions (
  Transaction_ID BIGSERIAL PRIMARY KEY,
  Wallet_ID BIGINT NOT NULL REFERENCES Wallet(Wallet_ID) ON DELETE CASCADE,
  Related_Payment_ID BIGINT UNIQUE REFERENCES Payment(Payment_ID) ON DELETE CASCADE,
  Amount DECIMAL(10,2) NOT NULL CHECK (Amount > 0),
  Type transaction_type NOT NULL,
  Transaction_Date DATE NOT NULL DEFAULT CURRENT_DATE,
  Transaction_Time TIME NOT NULL DEFAULT CURRENT_TIME
);

-- Report
CREATE TABLE Report (
  Report_ID BIGSERIAL PRIMARY KEY,
  Account_ID BIGINT NOT NULL REFERENCES Account(Account_ID) ON DELETE SET NULL,
  Admin_ID BIGINT REFERENCES Account(Account_ID) ON DELETE SET NULL,
  Status report_status NOT NULL DEFAULT 'Pending',
  Text TEXT NOT NULL,
  Answer TEXT,
  Type report_type NOT NULL,
  Related_Report_ID BIGINT REFERENCES Ticket(Ticket_ID),
  CONSTRAINT chk_different_account_admin
    CHECK (Account_ID <> Admin_ID),
  CONSTRAINT chk_admin_required_if_checked
    CHECK (
            NOT (Status = 'Checked' AND Admin_ID IS NULL)
          )
);
