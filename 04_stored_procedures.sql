-- 1. Show all tickets purchased by a user using Email or Phone Number
CREATE OR REPLACE FUNCTION get_reservations_by_contact(input_identifier TEXT)
RETURNS TABLE (
    Reservation_ID INT,
    Ticket_ID INT,
    Seat_Number VARCHAR,
    Status VARCHAR,
    Reservation_Date DATE,
    Reservation_Time TIME,
    Expiration TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        R."Reservation_ID",
        R."Ticket_ID",
        R."Seat_Number",
        R."Status",
        R."Reservation_Date",
        R."Reservation_Time",
        R."Expiration"
    FROM "Reservation" R

    JOIN "User" U ON R."User_ID" = U."User_ID"
    WHERE U."Email" = input_identifier OR U."Phone_Number" = input_identifier
    ORDER BY R."Reservation_Date", R."Reservation_Time";
END;
$$ LANGUAGE plpgsql;


-- 2. Show users whose reservations were cancelled by a given admin (using Email or Phone Number)
CREATE OR REPLACE FUNCTION get_cancelled_by_admin(input_identifier TEXT)
RETURNS TABLE (
    User_ID BIGINT,
    Name TEXT,
    Lastname TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        P."User_ID",
        P."Name",
        P."Lastname"
    FROM "Profile" P

    JOIN "Reservation" R ON P."User_ID" = R."User_ID"
    JOIN "Cancellation" C ON C."Reservation_ID" = R."Reservation_ID"
    JOIN "User" U ON C."Admin_ID" = U."User_ID"
    WHERE U."Email" = input_identifier OR U."Phone_Number" = input_identifier;
END;
$$ LANGUAGE plpgsql;


-- 3. Show all tickets purchased for routes starting in a given city
CREATE OR REPLACE FUNCTION get_tickets_in_cities(input_identifier TEXT)
RETURNS TABLE (
    Reservation_ID INT,
    Ticket_ID INT,
    Seat_Number VARCHAR,
    Status VARCHAR,
    Reservation_Date DATE,
    Reservation_Time TIME,
    Expiration TIMESTAMP
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        R."Reservation_ID",
        R."Ticket_ID",
        R."Seat_Number",
        R."Status",
        R."Reservation_Date",
        R."Reservation_Time",
        R."Expiration"
    FROM "Reservation" R
    JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
    JOIN "Route" Ro ON T."Route_ID" = Ro."Route_ID"
    JOIN "Location" L ON L."Location_ID" = Ro."Origin"
    WHERE LOWER(L."City") = LOWER(input_identifier);  
END;
$$ LANGUAGE plpgsql;
