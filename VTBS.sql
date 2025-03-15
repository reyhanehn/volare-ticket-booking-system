-- User Table
CREATE TABLE "User" (
  "User_ID" BIGSERIAL PRIMARY KEY,
  "Phone_Number" VARCHAR(15) UNIQUE CHECK (
      "Phone_Number" ~ '^\+989\d{2}\d{7}$' OR "Phone_Number" IS NULL
  ),
  "Email" VARCHAR(100) UNIQUE CHECK (
      "Email" ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$' OR "Email" IS NULL
  ),
  "Role" VARCHAR(20) NOT NULL CHECK ("Role" IN ('Customer', 'Admin')),
  "Status" VARCHAR(20) NOT NULL CHECK ("Status" IN ('Active', 'Banned')),
  "Password" TEXT NOT NULL,
  CONSTRAINT at_least_one_not_null CHECK (
      "Email" IS NOT NULL OR "Phone_Number" IS NOT NULL
  )
);

-- Profile Table
CREATE TABLE "Profile" (
  "User_ID" BIGSERIAL PRIMARY KEY REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Name" VARCHAR(50) NOT NULL,
  "Lastname" VARCHAR(50) NOT NULL,
  "City" VARCHAR(50) NOT NULL,
  "Registration_Date" DATE NOT NULL DEFAULT CURRENT_DATE
);

-- Company Table
CREATE TABLE "Company" (
  "Company_ID" BIGSERIAL PRIMARY KEY,
  "Name" VARCHAR(50) NOT NULL,
  "Headquarters" TEXT,
  "Year_Of_Establishment" SMALLINT CHECK ("Year_Of_Establishment" > 1800),
  "Contact_Number" VARCHAR(15) NOT NULL UNIQUE CHECK ("Contact_Number" ~ '^021\d{8}$') 
);

-- Vehicle Table
CREATE TABLE "Vehicle" (
  "Vehicle_ID" BIGSERIAL PRIMARY KEY,
  "Company_ID" BIGINT REFERENCES "Company"("Company_ID") ON DELETE CASCADE,
  "Name" VARCHAR(50) 
);

-- Transportation Types (Airplane, Bus, Train) inheriting Vehicle
CREATE TABLE "Airplane" (
  "First_Class_Capacity" SMALLINT NOT NULL CHECK ("First_Class_Capacity" >= 0),
  "Business_Class_Capacity" SMALLINT NOT NULL CHECK ("Business_Class_Capacity" >= 0),
  "Economy_Class_Capacity" SMALLINT NOT NULL CHECK ("Economy_Class_Capacity" >= 0),
  "With_Bed" BOOLEAN NOT NULL,
  "Internet" BOOLEAN NOT NULL,
  "Entertainment_Screen" BOOLEAN NOT NULL,
  CONSTRAINT check_positive_seats CHECK (("First_Class_Capacity" + "Business_Class_Capacity" + "Economy_Class_Capacity") > 0)
) INHERITS ("Vehicle");

CREATE TABLE "Bus" (
  "Type" VARCHAR(10) NOT NULL CHECK("Type" IN ('VIP', 'Normal')),
  "Seats_Count" SMALLINT,
  "Seats_In_Row" VARCHAR(10),
  "With_Bed" BOOLEAN,
  "Internet" BOOLEAN,
  "Entertainment_Screen" BOOLEAN,
  "Air_Conditioning" BOOLEAN
) INHERITS ("Vehicle");

CREATE TABLE "Train" (
  "Type" VARCHAR(8),
  "Stars" SMALLINT CHECK ("Stars" BETWEEN 1 AND 5),
  "Seats_Count" SMALLINT,
  "Seats_In_Cabin" SMALLINT,
  "With_Bed" BOOLEAN,
  "Internet" BOOLEAN,
  "Entertainment_Screen" BOOLEAN,
  "Air_Conditioning" BOOLEAN,
  "Freight_Wagons_Count" SMALLINT
) INHERITS ("Vehicle");

-- Ticket Table
CREATE TABLE "Ticket" (
  "Ticket_ID" BIGSERIAL PRIMARY KEY,
  "Vehicle_ID" BIGINT REFERENCES "Vehicle"("Vehicle_ID") ON DELETE CASCADE,
  "Origin" VARCHAR(50),
  "Destination" VARCHAR(50),
  "Departure_Date" DATE,
  "Arrival_Date" DATE,
  "Departure_Time" TIME,
  "Arrival_Time" TIME,
  "Price" DECIMAL(10,2) CHECK ("Price" > 0),
  "Remaining_Capacity" SMALLINT CHECK ("Remaining_Capacity" >= 0)
);

-- Ticket Types (Flight, Train Ride, Bus Ride)
CREATE TABLE "Flight" (
  "Vacation_Class_Code" VARCHAR(10),
  "Service" BOOLEAN,
  "Number_of_Stops" SMALLINT,
  "Stops" TEXT,
  "Origin_Airport" VARCHAR(50),
  "Destination_Airport" VARCHAR(50),
  "Type" VARCHAR(10)
) INHERITS ("Ticket");

CREATE TABLE "Train_Ride" (
  "Has_Private_Compartment" BOOLEAN,
  "Service" BOOLEAN,
  "Number_Of_Stops" SMALLINT,
  "Stops" TEXT,
  "Origin_Station" VARCHAR(50),
  "Destination_Station" VARCHAR(50),
  "Freight_Wagons_Left" SMALLINT
) INHERITS ("Ticket");

CREATE TABLE "Bus_Ride" (
  "Service" BOOLEAN,
  "Meal_Stops" VARCHAR(50),
  "Number_of_Stops" SMALLINT,
  "Stops" TEXT,
  "Origin_Station" VARCHAR(50),
  "Destination_Station" VARCHAR(50)
) INHERITS ("Ticket");

-- Reservation Table
CREATE TABLE "Reservation" (
  "Reservation_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Ticket_ID" BIGINT REFERENCES "Ticket"("Ticket_ID") ON DELETE CASCADE,
  "Seat_Number" VARCHAR(10),
  "Status" VARCHAR(20) CHECK ("Status" IN ('Pending', 'Confirmed', 'Cancelled')),
  "Reservation_Date" DATE DEFAULT CURRENT_DATE,
  "Reservation_Time" TIME DEFAULT CURRENT_TIME,
  CONSTRAINT check_expiration_after_reservation_time
    CHECK ("Expiration" > ("Reservation_Date" + "Reservation_Time")),
  "Expiration" INTERVAL
);

-- Payment Table
CREATE TABLE "Payment" (
  "Payment_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Reservation_ID" BIGINT REFERENCES "Reservation"("Reservation_ID") ON DELETE CASCADE,
  "Amount" DECIMAL(10,2) CHECK ("Amount" > 0),
  "Payment_Method" VARCHAR(20) CHECK ("Payment_Method" IN ('Credit Card', 'PayPal', 'Bank Transfer', 'Cash')),
  "Status" VARCHAR(20) CHECK ("Status" IN ('Pending', 'Completed', 'Failed', 'Refunded')),
  "Payment_Time" TIME DEFAULT CURRENT_TIME,
  "Payment_Date" DATE DEFAULT CURRENT_DATE
);

-- Wallet Table
CREATE TABLE "Wallet" (
  "Wallet_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT UNIQUE REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Balance" DECIMAL(10,2) CHECK ("Balance" >= 0)
);

-- Wallet Transactions Table
CREATE TABLE "Wallet_Transactions" (
  "Transaction_ID" BIGSERIAL PRIMARY KEY,
  "Wallet_ID" BIGINT REFERENCES "Wallet"("Wallet_ID") ON DELETE CASCADE,
  "Related_Payment_ID" BIGINT REFERENCES "Payment"("Payment_ID") ON DELETE SET NULL,
  "Amount" DECIMAL(10,2) CHECK ("Amount" > 0),
  "Transaction_Type" VARCHAR(20),
  "Transaction_Date" DATE DEFAULT CURRENT_DATE,
  "Transaction_Time" TIME DEFAULT CURRENT_TIME
);

-- Cancellation Table
CREATE TABLE "Cancelation" (
  "Cancelation_ID" BIGSERIAL PRIMARY KEY,
  "Reservation_ID" BIGINT REFERENCES "Reservation"("Reservation_ID") ON DELETE CASCADE,
  "Transaction_ID" BIGINT REFERENCES "Wallet_Transactions"("Transaction_ID") ON DELETE SET NULL,
  "Cancel_Date" DATE DEFAULT CURRENT_DATE,
  "Cancel_Time" TIME DEFAULT CURRENT_TIME,
  "Refund_Amount" DECIMAL(10,2) CHECK ("Refund_Amount" >= 0)
);
CREATE TABLE "Report" (
  "Report_ID" BIGSERIAL,
  "User_ID" BIGINT REFERENCES "User"("User_ID"),
  "Payment_ID" BIGINT REFERENCES "Payment"("Payment_ID"),
  "Reservation_ID" BIGINT REFERENCES "Reservation"("Reservation_ID"),
  "Ticket_ID" BIGINT REFERENCES "Ticket"("Ticket_ID"),
  "Type" VARCHAR(10),
  "Status" VARCHAR(10),
  "Text" TEXT,
  "Answer" TEXT,
  PRIMARY KEY ("Report_ID")
);

CREATE TABLE "Passenger" (
  "Passenger_ID" BIGSERIAL,
  "Name" VARCHAR(50),
  "Lastname" VARCHAR(50),
  "SSN" VARCHAR(10),
  "Birthdate" DATE,
  PRIMARY KEY ("Passenger_ID")
);

