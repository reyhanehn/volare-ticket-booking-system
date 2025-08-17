INSERT INTO "User" ("Phone_Number", "Email", "Role", "Status", "Password")
VALUES ('+989123456789', 'user1@example.com', 'Customer', 'Active', 'hashedpassword');

INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City")
VALUES (1, 'Ali', 'Rezaei', 'Tehran');

SELECT * FROM "User" WHERE "Role" = 'Customer';

INSERT INTO "Company" ("Name", "Headquarters", "Year_Of_Establishment", "Contact_Number")
VALUES ('IranAir', 'Tehran, Iran', 1961, '02112345678');

INSERT INTO "Airplane" ("Company_ID", "Name", "First_Class_Capacity", "Business_Class_Capacity", "Economy_Class_Capacity", "With_Bed", "Internet", "Entertainment_Screen")
VALUES (1, 'Boeing 747', 10, 30, 200, TRUE, TRUE, TRUE);

INSERT INTO "Location" ("Country", "City")
VALUES ('Iran', 'Tehran'), ('Iran', 'Mashhad'), ('Iran', 'Shiraz');

INSERT INTO "Station" ("Name", "Type", "Location_ID")
VALUES ('Tehran Imam Khomeini Airport', 'Airport', 1), ('Mashhad Airport', 'Airport', 2), ('');

INSERT INTO "Flight" ("Vehicle_ID", "Origin", "Destination", "Origin_Station", "Destination_Station",
                      "Departure_Date", "Arrival_Date", "Departure_Time", "Arrival_Time", "Price", "Remaining_Capacity",
                      "Has_Private_Compartment", "Service", "Number_of_Stops", "Stops", "Type")
VALUES (1, 1, 2, 1, 2, '2025-04-10', '2025-04-10', '08:00:00', '10:00:00', 500.00, 50,
        'Business_Class', TRUE, 0, NULL, 'Domestic');

INSERT INTO "Train_Ride" ("Vehicle_ID", "Origin", "Destination", "Origin_Station", "Destination_Station",
                      "Departure_Date", "Arrival_Date", "Departure_Time", "Arrival_Time", "Price", "Remaining_Capacity",
                      "Has_Private_Compartment", "Service", "Number_of_Stops", "Stops", "Freight_Wagons_Left")
VALUES (1, 1, 3, 1, 2, '2025-04-10', '2025-04-10', '08:00:00', '10:00:00', 500.00, 50,
        FALSE, TRUE, 0, NULL, 12);

INSERT INTO "Reservation" ("User_ID", "Ticket_ID", "Seat_Number", "Status", "Expiration")
VALUES (1, 1, '12A', 'Pending', '2 hours');

INSERT INTO "Payment" ("User_ID", "Reservation_ID", "Amount", "Payment_Method", "Status")
VALUES (1, 1, 500.00, 'Credit Card', 'Completed');

SELECT * FROM "Ticket" WHERE "Price" <= 500 AND "Remaining_Capacity" > 0;



-- For the new DATA
INSERT INTO "Location" ("Country", "City") VALUES
('Iran', 'Tehran'),
('Iran', 'Mashhad');

SELECT * FROM "Location"

INSERT INTO "User" ("Phone_Number", "Email", "Role", "Password_Hash")
VALUES
('+989121000001', 'alireza.rahimi@mail.com', 'Customer', 'AlirezaR@92');

SELECT * FROM "User"

INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City_ID") VALUES
(2, 'Alireza', 'Rahimi', 3);

INSERT INTO "Company" ("Name", "Headquarters", "Year_Of_Establishment", "Contact_Number") VALUES
('SkyTravel', 'Tehran', 1998, '02112345678');

SELECT * FROM "Company"

INSERT INTO "Vehicle" ("Company_ID", "Name", "Type") VALUES
(1, 'hahah', 'Airplane');

SELECT * FROM "Vehicle"

INSERT INTO "Airplane" ("Vehicle_ID", "First_Class_Capacity", "Business_Class_Capacity", "Economy_Class_Capacity") VALUES
(1, 20, 50, 300);

SELECT * FROM "Airplane"

INSERT INTO "Station" ("Name", "Type", "Location_ID") VALUES
('TehranAirport', 'Airport', 3),
('MashhadAirport', 'Airport', 4);

SELECT * FROM "Station"

INSERT INTO "Route" ("Origin", "Destination", "Origin_Station", "Destination_Station", "Departure_Date", "Departure_Time", "Arrival_Date", "Arrival_Time") VALUES
(3, 4, 1, 2, DATE '2025-05-10', TIME '15:30:00', DATE '2025-05-10', TIME '17:30:00');

SELECT * FROM "Route"

INSERT INTO "Ticket" ("Vehicle_ID", "Route_ID", "Price","Remaining_Capacity", "Type") VALUES
(1, 2, 10, 5, 'Flight');

SELECT * FROM "Ticket"

INSERT INTO "Flight" ("Ticket_ID", "Class_Code", "Type") VALUES
(1,'First_Class', 'Domestic');

SELECT * FROM "Flight"

INSERT INTO "Reservation" ("User_ID", "Passenger_ID", "Ticket_ID", "Seat_Number", "Status", "Expiration")
VALUES (2, 1, 1, '12A', 'Confirmed', INTERVAL '1 day');

SELECT * FROM "Reservation"

INSERT INTO "Passenger" ("Name", "Lastname", "SSN", "Birthdate") VALUES
('HEDI', 'tahmouresi', '0123456789', DATE '1989-05-10');

SELECT * FROM "Passenger"

SELECT * FROM "User"
SELECT * FROM "Location"
SELECT * FROM "Profile"
SELECT * FROM "Airplane"
SELECT * FROM "Company"
SELECT * FROM "Flight"
SELECT * FROM "Vehicle"
SELECT * FROM "Ticket"
SELECT * FROM "Route"
SELECT * FROM "Reservation"
SELECT * FROM "Station"

INSERT INTO "Service" ("Name")VALUES
('Internet'),
('With_Bed');

SELECT * FROM "Service"

INSERT INTO "Vehicle_Service" ("Vehicle_ID", "Service_ID") VALUES
(1, 1);


INSERT INTO "Valid_Stop_Type" ("Transport_Mode", "Stop_Type") VALUES
('Airplane', 'Layover');

SELECT * FROM "Valid_Stop_Type"

INSERT INTO "Ticket_Stop" ("Ticket_ID", "Station_ID", "Stop_Order", "Valid_Stop_Type_ID") VALUES
(1, 2, 1, 1);

SELECT * FROM "Valid_Stop_Type"

INSERT INTO "Wallet" ("User_ID", "Balance") VALUES
(2, 10);

SELECT * FROM "Wallet"

INSERT INTO "Payment" ("User_ID", "Reservation_ID", "Amount", "Payment_Method", "Status") VALUES
(2, 1, 5, 'Cash', 'Completed');

SELECT * FROM "Payment"

INSERT INTO "Wallet_Transactions" ("Wallet_ID", "Related_Payment_ID", "Amount", "Type") VALUES
(1, 1, 3, 'Refund');

SELECT * FROM "Wallet_Transactions"

INSERT INTO "User" ("Phone_Number", "Email", "Role", "Password_Hash")
VALUES
('+989121000051', 'samaneh.rahimi@mail.com', 'Admin', 'SamanehR@2025');

INSERT INTO "Cancellation" ("Reservation_ID", "Admin_ID", "Transaction_ID", "Refund_Amount") VALUES
(1, 3, 1, 3);

SELECT * FROM "Cancellation"

INSERT INTO "Report" ("User_ID", "Admin_ID", "Type", "Status", "Text", "Answer") VALUES
(2, 3, 'Payment', 'Checked', 'I hate your system', 'I dont give a shit');

SELECT * FROM "Report"

INSERT INTO "Report_Payment" ("Report_ID", "Payment_ID") VALUES
(1, 1);

SELECT * FROM "Report_Payment"