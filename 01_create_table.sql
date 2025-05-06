--ENUMS
CREATE TYPE user_role AS ENUM ('Customer', 'Admin');
CREATE TYPE user_status AS ENUM ('Active', 'Banned');
CREATE TYPE seats_layout AS ENUM ('1+2', '2+2');
CREATE TYPE train_type AS ENUM ('Compartment', 'Coach');
CREATE TYPE payment_method AS ENUM ('Credit Card','PayPal','Bank Transfer','Cash', 'Wallet');
CREATE TYPE payment_status AS ENUM ('Pending','Completed','Failed','Refunded');
CREATE TYPE transaction_type AS ENUM ('Charge', 'Payment', 'Refund');
CREATE TYPE station_type AS ENUM ('Train_Station', 'Bus_Station', 'Airport');
CREATE TYPE flight_type AS ENUM ('Domestic', 'International');
CREATE TYPE transport_type AS ENUM ('Train', 'Bus', 'Airplane');
CREATE TYPE stop_type AS ENUM ('Transit', 'Meal', 'Refuel', 'Layover');
CREATE TYPE reservation_status AS ENUM ('Pending', 'Confirmed', 'Cancelled');
CREATE TYPE report_status AS ENUM ('Pending', 'Checked');
CREATE TYPE vacation_class_code AS ENUM ('First_Class', 'Business_Class', 'Economy_Class');
CREATE TYPE bus_type AS ENUM ('VIP', 'Normal');


-- Location Table
CREATE TABLE "Location" (
    "Location_ID" SERIAL PRIMARY KEY,
    "Country" VARCHAR(50) NOT NULL CHECK ("Country" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
    "City" VARCHAR(50) NOT NULL CHECK ("City" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
    UNIQUE("Country", "City")
);

-- User Table
CREATE TABLE "User" (
  "User_ID" BIGSERIAL PRIMARY KEY,
  "Phone_Number" VARCHAR(15) UNIQUE CHECK (
      "Phone_Number" ~ '^\+989\d{2}\d{7}$' OR "Phone_Number" IS NULL
  ),
  "Email" VARCHAR(100) UNIQUE CHECK (
      "Email" ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' OR "Email" IS NULL
  ),
  "Role" user_role NOT NULL,
  "Status" user_status NOT NULL DEFAULT 'Active',
  "Password_Hash" TEXT NOT NULL,
  CONSTRAINT at_least_one_not_null CHECK (
      "Email" IS NOT NULL OR "Phone_Number" IS NOT NULL
  )
);

-- Profile Table
CREATE TABLE "Profile" (
  "User_ID" BIGINT PRIMARY KEY REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Name" VARCHAR(50) NOT NULL CHECK ("Name" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
  "Lastname" VARCHAR(50) NOT NULL CHECK ("Lastname" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
  "City_ID" BIGINT REFERENCES "Location"("Location_ID") NOT NULL,
  "Registration_Date" DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Company Table
CREATE TABLE "Company" (
  "Company_ID" BIGSERIAL PRIMARY KEY,
  "Name" VARCHAR(50) NOT NULL UNIQUE CHECK ("Name" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
  "Contact_Number" VARCHAR(15) NOT NULL UNIQUE CHECK ("Contact_Number" ~ '^021\d{8}$'),
  "Logo_URL" TEXT,
  "Headquarters" TEXT,
    "Year_Of_Establishment" SMALLINT CHECK (
    "Year_Of_Establishment" > 1800 AND
    "Year_Of_Establishment" <= EXTRACT(YEAR FROM CURRENT_DATE)
  )
);

-- Service Table
CREATE TABLE "Service" (
  "Service_ID" SERIAL PRIMARY KEY,
  "Name" VARCHAR(50) UNIQUE NOT NULL
);

-- Vehicle Table
CREATE TABLE "Vehicle" (
  "Vehicle_ID" BIGSERIAL PRIMARY KEY,
  "Company_ID" BIGINT REFERENCES "Company"("Company_ID") ON DELETE CASCADE,
  "Name" VARCHAR(50)
);

-- Junction table to link Service and Vehicle
CREATE TABLE "Vehicle_Service" (
  "Vehicle_ID" BIGINT REFERENCES "Vehicle"("Vehicle_ID") ON DELETE CASCADE,
  "Service_ID" INT REFERENCES "Service"("Service_ID") ON DELETE CASCADE,
  PRIMARY KEY ("Vehicle_ID", "Service_ID")
);

-- Vehicle Types
-- Inheritance causes a lot of problems so we are using composition instead
CREATE TABLE "Airplane" (
  "Vehicle_ID" BIGINT PRIMARY KEY REFERENCES "Vehicle"("Vehicle_ID") ON DELETE CASCADE,
  "First_Class_Capacity" SMALLINT NOT NULL CHECK ("First_Class_Capacity" >= 0),
  "Business_Class_Capacity" SMALLINT NOT NULL CHECK ("Business_Class_Capacity" >= 0),
  "Economy_Class_Capacity" SMALLINT NOT NULL CHECK ("Economy_Class_Capacity" >= 0),
  CONSTRAINT check_positive_seats CHECK (("First_Class_Capacity" + "Business_Class_Capacity" + "Economy_Class_Capacity") > 0)
);

CREATE TABLE "Bus" (
  "Vehicle_ID" BIGINT PRIMARY KEY REFERENCES "Vehicle"("Vehicle_ID") ON DELETE CASCADE,
  "Type" bus_type NOT NULL,
  "Seats_Count" SMALLINT NOT NULL CHECK("Seats_Count" > 0),
  "Seats_In_Row" seats_layout NOT NULL
);

CREATE TABLE "Train" (
  "Vehicle_ID" BIGINT PRIMARY KEY REFERENCES "Vehicle"("Vehicle_ID") ON DELETE CASCADE,
  "Type" train_type NOT NULL,
  "Stars" SMALLINT NOT NULL CHECK ("Stars" BETWEEN 1 AND 5),
  "Seats_Count" SMALLINT NOT NULL CHECK("Seats_Count" > 0),
  "Seats_In_Cabin" SMALLINT CHECK("Seats_In_Cabin" > 0),
  "Freight_Wagons_Count" SMALLINT NOT NULL CHECK ("Freight_Wagons_Count" >= 0),
  CHECK (
    "Type" != 'Coach' OR "Seats_In_Cabin" = "Seats_Count"
  )
);

-- Station Table
CREATE TABLE "Station" (
    "Station_ID" SERIAL PRIMARY KEY,
    "Name" VARCHAR(100) NOT NULL CHECK ("Name" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$'),
    "Type" station_type NOT NULL,
    "Location_ID" INT REFERENCES "Location"("Location_ID") ON DELETE CASCADE,
    UNIQUE("Name", "Location_ID")
);

-- Route Table
CREATE TABLE "Route" (
  "Route_ID" BIGSERIAL PRIMARY KEY,
  "Origin" INT NOT NULL REFERENCES "Location"("Location_ID"),
  "Destination" INT NOT NULL REFERENCES "Location"("Location_ID"),
  "Origin_Station" INT REFERENCES "Station"("Station_ID"),
  "Destination_Station" INT REFERENCES "Station"("Station_ID"),
  "Departure_Date" DATE NOT NULL,
  "Departure_Time" TIME NOT NULL,
  "Arrival_Date" DATE NOT NULL,
  "Arrival_Time" TIME NOT NULL,
  CONSTRAINT check_departure_before_arrival
    CHECK (("Departure_Date" < "Arrival_Date")
            OR 
          ("Departure_Date" = "Arrival_Date" AND "Departure_Time" < "Arrival_Time")),
  CONSTRAINT different_origin_and_station 
    CHECK ("Origin" <> "Destination")
);

-- Ticket Table
CREATE TABLE "Ticket" (
  "Ticket_ID" BIGSERIAL PRIMARY KEY,
  "Vehicle_ID" BIGINT NOT NULL REFERENCES "Vehicle"("Vehicle_ID"),
  "Route_ID" BIGINT NOT NULL REFERENCES "Route"("Route_ID"),
  "Price" DECIMAL(10,2) NOT NULL CHECK ("Price" > 0),
  "Remaining_Capacity" SMALLINT NOT NULL CHECK ("Remaining_Capacity" >= 0)
);

-- Valid Stop Type Table
CREATE TABLE "Valid_Stop_Type" (
  "Valid_Stop_Type_ID" SERIAL PRIMARY KEY,
  "Transport_Mode" transport_type NOT NULL,
  "Stop_Type" stop_type NOT NULL,
  UNIQUE ("Transport_Mode", "Stop_Type")
);

-- Junction Table to connect Ticket to its stops
CREATE TABLE "Ticket_Stop" (
  "Ticket_ID" BIGINT NOT NULL REFERENCES "Ticket"("Ticket_ID") ON DELETE CASCADE,
  "Station_ID" INT NOT NULL REFERENCES "Station"("Station_ID") ON DELETE CASCADE,
  "Stop_Order" SMALLINT NOT NULL CHECK ("Stop_Order" > 0),
  "Stop_ID" INT NOT NULL REFERENCES "Valid_Stop_Type"("Valid_Stop_Type_ID"),
  PRIMARY KEY("Ticket_ID", "Station_ID"),
  UNIQUE("Ticket_ID", "Stop_Order")
);

-- Ticket Types (Flight, Train Ride, Bus Ride)
-- Inheritance cause a lot of problems so we are using composition instead
CREATE TABLE "Flight" (
  "Ticket_ID" BIGINT PRIMARY KEY REFERENCES "Ticket"("Ticket_ID") ON DELETE CASCADE,
  "Class_Code" vacation_class_code NOT NULL,
  "Type" flight_type NOT NULL,
  UNIQUE ("Ticket_ID", "Class_Code")
);

CREATE TABLE "Train_Ride" (
  "Ticket_ID" BIGINT PRIMARY KEY REFERENCES "Ticket"("Ticket_ID") ON DELETE CASCADE,
  "Has_Private_Compartment" BOOLEAN NOT NULL DEFAULT FALSE,
  "Freight_Wagons_Left" SMALLINT NOT NULL
);


-- Passenger Table
CREATE TABLE "Passenger" (
  "Passenger_ID" BIGSERIAL PRIMARY KEY,
  "Name" VARCHAR(50) NOT NULL CHECK ("Name" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$')
  ,
  "Lastname" VARCHAR(50) NOT NULL CHECK ("Lastname" ~ '^[A-Za-z]+(\s[A-Za-z]+)*$')
  ,
  "SSN" VARCHAR(10) UNIQUE CHECK (
      "SSN" ~ '^\d{10}$'
  ),
  "Birthdate" DATE NOT NULL CHECK ("Birthdate" <= CURRENT_DATE),
  "Picture_URL" TEXT CHECK ("Picture_URL" ~* '^https?://.+\.(jpg|jpeg|png|gif)$')
);

-- Reservation Table
CREATE TABLE "Reservation" (
  "Reservation_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT NOT NULL REFERENCES "User"("User_ID") ON DELETE CASCADE, --the user who reserved it
  "Passenger_ID" BIGINT NOT NULL REFERENCES "Passenger" ("Passenger_ID") ON DELETE CASCADE, -- the passenger whom the reservation is for 
  "Ticket_ID" BIGINT NOT NULL REFERENCES "Ticket"("Ticket_ID") ON DELETE CASCADE,
  "Seat_Number" VARCHAR(10) NOT NULL CHECK ("Seat_Number" ~ '^[0-9]{1,2}[A-Z]$'),
  "Status" reservation_status NOT NULL DEFAULT 'Pending',
  "Reservation_Date" DATE NOT NULL DEFAULT CURRENT_DATE,
  "Reservation_Time" TIME NOT NULL DEFAULT CURRENT_TIME,
  "Expiration" INTERVAL NOT NULL,
  UNIQUE("Ticket_ID", "Seat_Number")
  -- UNIQUE("Ticket_ID", "Seat_Number")
);

-- Payment Table
CREATE TABLE "Payment" (
  "Payment_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT NOT NULL REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Reservation_ID" BIGINT NOT NULL UNIQUE REFERENCES "Reservation"("Reservation_ID") ON DELETE CASCADE,
  "Amount" DECIMAL(10,2) NOT NULL CHECK ("Amount" > 0),
  "Payment_Method" payment_method NOT NULL,
  "Status" payment_status NOT NULL DEFAULT 'Pending',
  "Payment_Time" TIME NOT NULL DEFAULT CURRENT_TIME,
  "Payment_Date" DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Wallet Table
CREATE TABLE "Wallet" (
  "Wallet_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT NOT NULL UNIQUE REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Balance" DECIMAL(10,2) NOT NULL CHECK ("Balance" >= 0)
);

-- Wallet Transactions Table
CREATE TABLE "Wallet_Transactions" (
  "Transaction_ID" BIGSERIAL PRIMARY KEY,
  "Wallet_ID" BIGINT NOT NULL REFERENCES "Wallet"("Wallet_ID") ON DELETE CASCADE,
  "Related_Payment_ID" BIGINT UNIQUE REFERENCES "Payment"("Payment_ID") ON DELETE SET NULL,
  "Amount" DECIMAL(10,2) NOT NULL CHECK ("Amount" > 0),
  "Type" transaction_type NOT NULL,
  "Transaction_Date" DATE NOT NULL DEFAULT CURRENT_DATE,
  "Transaction_Time" TIME NOT NULL DEFAULT CURRENT_TIME
);

-- Cancellation Table
CREATE TABLE "Cancellation" (
  "Cancellation_ID" BIGSERIAL PRIMARY KEY,
  "Reservation_ID" BIGINT NOT NULL UNIQUE REFERENCES "Reservation"("Reservation_ID") ON DELETE CASCADE,
  "Admin_ID" BIGINT NOT NULL UNIQUE REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Transaction_ID" BIGINT NOT NULL UNIQUE REFERENCES "Wallet_Transactions"("Transaction_ID") ON DELETE SET NULL,
  "Cancel_Date" DATE NOT NULL DEFAULT CURRENT_DATE,
  "Cancel_Time" TIME NOT NULL DEFAULT CURRENT_TIME,
  "Refund_Amount" DECIMAL(10,2) CHECK ("Refund_Amount" >= 0)
);

-- Report Table
CREATE TABLE "Report" (
  "Report_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT NOT NULL REFERENCES "User"("User_ID"),
  "Admin_ID" BIGINT NOT NULL UNIQUE REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Status" report_status NOT NULL DEFAULT 'Pending',
  "Text" TEXT NOT NULL,
  "Answer" TEXT,
  CONSTRAINT chk_different_user_admin
    CHECK ("User_ID" <> "Admin_ID"),
  CONSTRAINT chk_admin_required_if_checked
    CHECK (
            NOT ("Status" = 'Checked' AND "Admin_ID" IS NULL)
          )
);

-- Association Tables for Report
CREATE TABLE "Report_Reservation" (
  "Report_ID" BIGINT PRIMARY KEY REFERENCES "Report"("Report_ID") ON DELETE CASCADE,
  "Reservation_ID" BIGINT NOT NULL REFERENCES "Reservation"("Reservation_ID")
);

CREATE TABLE "Report_Payment" (
  "Report_ID" BIGINT PRIMARY KEY REFERENCES "Report"("Report_ID") ON DELETE CASCADE,
  "Payment_ID" BIGINT NOT NULL REFERENCES "Payment"("Payment_ID")
);

CREATE TABLE "Report_Ticket" (
  "Report_ID" BIGINT PRIMARY KEY REFERENCES "Report"("Report_ID") ON DELETE CASCADE,
  "Ticket_ID" BIGINT NOT NULL REFERENCES "Ticket"("Ticket_ID")
);
