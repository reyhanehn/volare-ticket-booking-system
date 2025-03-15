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
  "Name" VARCHAR(50) NOT NULL UNIQUE,
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

-- Vehicle Types
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
  "Seats_Count" SMALLINT NOT NULL CHECK("Seats_Count" > 0),
  "Seats_In_Row" VARCHAR(10) NOT NULL CHECK("Seats_In_Row" IN ('1+2', '2+2')),
  "With_Bed" BOOLEAN NOT NULL,
  "Internet" BOOLEAN NOT NULL,
  "Entertainment_Screen" BOOLEAN NOT NULL,
  "Air_Conditioning" BOOLEAN NOT NULL
) INHERITS ("Vehicle");

CREATE TABLE "Train" (
  "Type" VARCHAR(8) NOT NULL CHECK ("Type" IN ('Compartment', 'Coach')),
  "Stars" SMALLINT NOT NULL CHECK ("Stars" BETWEEN 1 AND 5),
  "Seats_Count" SMALLINT NOT NULL CHECK("Seats_Count" > 0),
  "Seats_In_Cabin" SMALLINT CHECK("Seats_In_Cabin" > 0),
  "With_Bed" BOOLEAN NOT NULL,
  "Internet" BOOLEAN NOT NULL,
  "Entertainment_Screen" BOOLEAN NOT NULL,
  "Air_Conditioning" BOOLEAN NOT NULL,
  "Freight_Wagons_Count" SMALLINT NOT NULL
) INHERITS ("Vehicle");

-- Ticket Table
CREATE TABLE "Ticket" (
  "Ticket_ID" BIGSERIAL PRIMARY KEY,
  "Vehicle_ID" BIGINT NOT NULL REFERENCES "Vehicle"("Vehicle_ID") ON DELETE CASCADE,
  "Origin" VARCHAR(50) NOT NULL,
  "Destination" VARCHAR(50) NOT NULL,
  "Departure_Date" DATE NOT NULL,
  "Arrival_Date" DATE NOT NULL,
  "Departure_Time" TIME NOT NULL,
  "Arrival_Time" TIME NOT NULL,
  "Price" DECIMAL(10,2) NOT NULL CHECK ("Price" > 0),
  "Remaining_Capacity" SMALLINT NOT NULL CHECK ("Remaining_Capacity" >= 0),
  CONSTRAINT check_departure_is_before_arrival
    CHECK  ("Departure_Date" < "Arrival_Date" OR 
      ("Departure_Date" = "Arrival_Date" AND "Departure_Time" < "Arrival_Time"))
);

-- Ticket Types (Flight, Train Ride, Bus Ride)
CREATE TABLE "Flight" (
  "Vacation_Class_Code" VARCHAR(20) NOT NULL CHECK ("Vacation_Class_Code" IN ('First_Class', 'Business_Class', 'Economy_Class')),
  "Service" BOOLEAN NOT NULL,
  "Number_of_Stops" SMALLINT NOT NULL CHECK ("Number_of_Stops" >= 0),
  "Stops" TEXT,
  "Origin_Airport" VARCHAR(50) NOT NULL,
  "Destination_Airport" VARCHAR(50) NOT NULL,
  "Type" VARCHAR(15) NOT NULL CHECK("Type" IN ('Domestic', 'International')),
  CONSTRAINT check_stops_validity CHECK 
         (("Number_of_Stops" = 0 AND "Stops" IS NULL) 
       OR ("Number_of_Stops" > 0 AND "Stops" IS NOT NULL))
) INHERITS ("Ticket");

CREATE TABLE "Train_Ride" (
  "Has_Private_Compartment" BOOLEAN NOT NULL,
  "Service" BOOLEAN NOT NULL,
  "Number_Of_Stops" SMALLINT NOT NULL CHECK ("Number_Of_Stops" >= 0),
  "Stops" TEXT,
  "Origin_Station" VARCHAR(50) NOT NULL,
  "Destination_Station" VARCHAR(50) NOT NULL,
  "Freight_Wagons_Left" SMALLINT NOT NULL,
  CONSTRAINT check_stops_validity CHECK 
         (("Number_Of_Stops" = 0 AND "Stops" IS NULL) 
       OR ("Number_Of_Stops" > 0 AND "Stops" IS NOT NULL))
) INHERITS ("Ticket");

CREATE TABLE "Bus_Ride" (
  "Service" BOOLEAN NOT NULL,
  "Number_of_Meal_Stops" SMALLINT NOT NULL CHECK ("Number_of_Meal_Stops" >= 0),
  "Meal_Stops" TEXT,
  "Number_of_Stops" SMALLINT NOT NULL CHECK ("Number_of_Stops" >= 0),
  "Stops" TEXT,
  "Origin_Station" VARCHAR(50) NOT NULL,
  "Destination_Station" VARCHAR(50) NOT NULL,
  CONSTRAINT check_stops_validity CHECK 
         (("Number_of_Stops" = 0 AND "Stops" IS NULL) 
       OR ("Number_of_Stops" > 0 AND "Stops" IS NOT NULL)),
  CONSTRAINT check_meal_stops_validity CHECK 
         (("Number_of_Meal_Stops" = 0 AND "Meal_Stops" IS NULL) 
       OR ("Number_of_Meal_Stops" > 0 AND "Meal_Stops" IS NOT NULL))
) INHERITS ("Ticket");

-- Reservation Table
CREATE TABLE "Reservation" (
  "Reservation_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT NOT NULL REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Ticket_ID" BIGINT NOT NULL REFERENCES "Ticket"("Ticket_ID") ON DELETE CASCADE,
  "Seat_Number" VARCHAR(10) NOT NULL,
  "Status" VARCHAR(20) NOT NULL CHECK ("Status" IN ('Pending', 'Confirmed', 'Cancelled')),
  "Reservation_Date" DATE NOT NULL DEFAULT CURRENT_DATE,
  "Reservation_Time" TIME NOT NULL DEFAULT CURRENT_TIME,
  "Expiration" INTERVAL NOT NULL
);

-- Payment Table
CREATE TABLE "Payment" (
  "Payment_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT NOT NULL REFERENCES "User"("User_ID") ON DELETE CASCADE,
  "Reservation_ID" BIGINT NOT NULL UNIQUE REFERENCES "Reservation"("Reservation_ID") ON DELETE CASCADE,
  "Amount" DECIMAL(10,2) NOT NULL CHECK ("Amount" > 0),
  "Payment_Method" VARCHAR(20) NOT NULL CHECK ("Payment_Method" IN ('Credit Card', 'PayPal', 'Bank Transfer', 'Cash')),
  "Status" VARCHAR(20) NOT NULL CHECK ("Status" IN ('Pending', 'Completed', 'Failed', 'Refunded')),
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
  "Transaction_Type" VARCHAR(20) NOT NULL CHECK ("Transaction_Type" IN ('Charge', 'Payment', 'Refund')),
  "Transaction_Date" DATE NOT NULL DEFAULT CURRENT_DATE,
  "Transaction_Time" TIME NOT NULL DEFAULT CURRENT_TIME
);

-- Cancellation Table
CREATE TABLE "Cancelation" (
  "Cancelation_ID" BIGSERIAL PRIMARY KEY,
  "Reservation_ID" BIGINT NOT NULL UNIQUE REFERENCES "Reservation"("Reservation_ID") ON DELETE CASCADE,
  "Transaction_ID" BIGINT NOT NULL UNIQUE REFERENCES "Wallet_Transactions"("Transaction_ID") ON DELETE SET NULL,
  "Cancel_Date" DATE NOT NULL DEFAULT CURRENT_DATE,
  "Cancel_Time" TIME NOT NULL DEFAULT CURRENT_TIME,
  "Refund_Amount" DECIMAL(10,2) CHECK ("Refund_Amount" >= 0)
);

CREATE TABLE "Report" (
  "Report_ID" BIGSERIAL PRIMARY KEY,
  "User_ID" BIGINT NOT NULL REFERENCES "User"("User_ID"),
  "Payment_ID" BIGINT UNIQUE REFERENCES "Payment"("Payment_ID"),
  "Reservation_ID" BIGINT UNIQUE REFERENCES "Reservation"("Reservation_ID"),
  "Ticket_ID" BIGINT UNIQUE REFERENCES "Ticket"("Ticket_ID"),
  "Type" VARCHAR(10) NOT NULL CHECK("Type" IN ('Payment', 'Reservation', 'Ticket')),
  "Status" VARCHAR(10) NOT NULL CHECK ("Status" IN ('Pending', 'Checked')),
  "Text" TEXT NOT NULL,
  "Answer" TEXT,
  CONSTRAINT check_meal_stops_validity CHECK 
         (("Type" = 'Reservation' AND "Reservation_ID" IS NOT NULL) 
       OR ("Type" = 'Payment' AND "Payment_ID" IS NOT NULL)
       OR ("Type" = 'Ticket' AND "Ticket_ID" IS NOT NULL))
);

CREATE TABLE "Passenger" (
  "Passenger_ID" BIGSERIAL PRIMARY KEY,
  "Name" VARCHAR(50) NOT NULL,
  "Lastname" VARCHAR(50) NOT NULL,
  "SSN" VARCHAR(10) UNIQUE CHECK (
      "SSN" ~ '^\d{10}$'
  ),
  "Birthdate" DATE NOT NULL
);
