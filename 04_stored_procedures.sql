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

-- 4. Search tickets by input phrase matching passenger name, route city, or class
CREATE OR REPLACE FUNCTION search_tickets_by_phrase(input_phrase TEXT)
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
    JOIN "Profile" P ON P."User_ID" = U."User_ID"
    JOIN "Ticket" T ON R."Ticket_ID" = T."Ticket_ID"
    JOIN "Route" Ro ON T."Route_ID" = Ro."Route_ID"
    JOIN "Location" L1 ON L1."Location_ID" = Ro."Origin"
    JOIN "Location" L2 ON L2."Location_ID" = Ro."Destination"
    WHERE
        LOWER(P."Name") LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(P."Lastname") LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(T."Class") LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(L1."City") LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(L2."City") LIKE LOWER('%' || input_phrase || '%');
END;
$$ LANGUAGE plpgsql;


-- 5. Get other users who live in the same city as the given user (by phone or email)
CREATE OR REPLACE FUNCTION get_users_from_same_city(input_identifier TEXT)
RETURNS TABLE (
    User_ID BIGINT,
    Name TEXT,
    Lastname TEXT,
    City TEXT
)
AS $$
DECLARE
    target_city TEXT;
BEGIN
    SELECT P."City" INTO target_city
    FROM "User" U
    JOIN "Profile" P ON U."User_ID" = P."User_ID"
    WHERE U."Email" = input_identifier OR U."Phone_Number" = input_identifier;

    RETURN QUERY
    SELECT
        P."User_ID",
        P."Name",
        P."Lastname",
        P."City"
    FROM "Profile" P
    WHERE P."City" = target_city
    AND P."User_ID" NOT IN (
        SELECT U."User_ID"
        FROM "User" U
        WHERE U."Email" = input_identifier OR U."Phone_Number" = input_identifier
    );
END;
$$ LANGUAGE plpgsql;


-- 6. Get top n users with the most ticket purchases from a given date onward
CREATE OR REPLACE FUNCTION get_top_buyers_from_date(start_date DATE, count_limit INT)
RETURNS TABLE (
    User_ID BIGINT,
    Name TEXT,
    Lastname TEXT,
    Ticket_Count INT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        P."User_ID",
        P."Name",
        P."Lastname",
        COUNT(R."Ticket_ID") AS Ticket_Count
    FROM "Reservation" R
    JOIN "Profile" P ON R."User_ID" = P."User_ID"
    WHERE R."Reservation_Date" >= start_date
    GROUP BY P."User_ID", P."Name", P."Lastname"
    ORDER BY Ticket_Count DESC
    LIMIT count_limit;
END;
$$ LANGUAGE plpgsql;


-- 7. Show reservations (that were cancelled) for a specific vehicle type, ordered by reservation date
CREATE OR REPLACE FUNCTION get_cancelled_reservations_by_vehicle_type(vehicle_type TEXT)
RETURNS TABLE (
    Reservation_ID BIGINT,
    Ticket_ID BIGINT,
    Reservation_Date DATE,
    Reservation_Time TIME,
    Vehicle_Type TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        R."Reservation_ID",
        R."Ticket_ID",
        R."Reservation_Date",
        R."Reservation_Time",
        V."Type" AS Vehicle_Type
    FROM "Reservation" R
    JOIN "Cancellation" C ON C."Reservation_ID" = R."Reservation_ID"
    JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
    JOIN "Route" Ro ON Ro."Route_ID" = T."Route_ID"
    JOIN "Vehicle" V ON V."Vehicle_ID" = Ro."Vehicle_ID"
    WHERE V."Type" = vehicle_type
    ORDER BY R."Reservation_Date", R."Reservation_Time";
END;
$$ LANGUAGE plpgsql;
