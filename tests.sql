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

