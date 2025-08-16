-- 1. Show all tickets purchased by a user using Email or Phone
CREATE OR REPLACE FUNCTION get_reservations_by_contacts(input_identifier TEXT)
RETURNS TABLE (
    Reservation_ID BIGINT,
    Ticket_ID BIGINT,
    Seat_Number VARCHAR,
    Status reservation_status,
    Reservation_Date DATE,
    Reservation_Time TIME,
    Expiration INTERVAL
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

-- TEST
SELECT * FROM get_reservations_by_contacts('alireza.rahimi@mail.com');
SELECT * FROM get_reservations_by_contacts('+989121000001');


-- 2. Show users whose reservations were cancelled by a given admin (using Email or Phone Number)
CREATE OR REPLACE FUNCTION get_cancelled_by_admins(input_identifier TEXT)
RETURNS TABLE (
    User_ID BIGINT,
    Name VARCHAR(50),
    Lastname VARCHAR(50)
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

-- TEST
SELECT * FROM get_cancelled_by_admins('zhurst@yahoo.com');
SELECT * FROM get_cancelled_by_admins('+989953658868');


-- 3. Show all tickets purchased for routes starting in a given city
CREATE OR REPLACE FUNCTION get_tickets_in_cit(input_identifier TEXT)
RETURNS TABLE (
    Reservation_ID BIGINT,
    Ticket_ID BIGINT,
    City VARCHAR(50)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        R."Reservation_ID",
        R."Ticket_ID",
        L."City"
    FROM "Reservation" R
    JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
    JOIN "Route" Ro ON T."Route_ID" = Ro."Route_ID"
    JOIN "Location" L ON L."Location_ID" = Ro."Origin"
    WHERE LOWER(L."City") = LOWER(input_identifier);
END;
$$ LANGUAGE plpgsql;

-- TEST
SELECT * FROM get_tickets_in_cit('Tabriz');


-- 4. Search tickets by input phrase matching passenger name, route city, or class
CREATE OR REPLACE FUNCTION search_tickets_by_phrase4(input_phrase TEXT)
RETURNS TABLE (
    Reservation_ID BIGINT,
    Ticket_ID BIGINT,
    Name VARCHAR(50),
    Lastname VARCHAR(50),
  Origin VARCHAR(50),
  Destination VARCHAR(50)
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        R."Reservation_ID",
        R."Ticket_ID",
    P."Name",
    P."Lastname",
        L1."City",
    L2."City"
  FROM "Reservation" R
    JOIN "User" U ON R."User_ID" = U."User_ID"
    JOIN "Profile" P ON P."User_ID" = U."User_ID"
    JOIN "Ticket" T ON R."Ticket_ID" = T."Ticket_ID"
  JOIN "Flight" F ON F."Ticket_ID" = R."Ticket_ID"
    JOIN "Route" Ro ON T."Route_ID" = Ro."Route_ID"
    JOIN "Location" L1 ON L1."Location_ID" = Ro."Origin"
    JOIN "Location" L2 ON L2."Location_ID" = Ro."Destination"
    WHERE
        LOWER(P."Name") LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(P."Lastname") LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(F."Class_Code" :: TEXT) LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(L1."City") LIKE LOWER('%' || input_phrase || '%')
        OR LOWER(L2."City") LIKE LOWER('%' || input_phrase || '%');
END;
$$ LANGUAGE plpgsql;

-- TEST
SELECT * FROM search_tickets_by_phrase4('ehra');



-- 5. Get other users who live in the same city as the given user (by phone or email)
CREATE OR REPLACE FUNCTION get_users_from_same_city2(input_identifier TEXT)
RETURNS TABLE (
    User_ID BIGINT,
    Name VARCHAR(50),
    Lastname VARCHAR(50),
    City VARCHAR(50)
)
AS $$
DECLARE
    target_city TEXT;
BEGIN
    SELECT L."City" INTO target_city
    FROM "User" U
    JOIN "Profile" P ON U."User_ID" = P."User_ID"
  JOIN "Location" L ON L."Location_ID" = P."City_ID"
    WHERE U."Email" = input_identifier OR U."Phone_Number" = input_identifier;

    RETURN QUERY
    SELECT
        P."User_ID",
        P."Name",
        P."Lastname",
        L."City"
    FROM "Profile" P
  JOIN "Location" L ON L."Location_ID" = P."City_ID"
    WHERE L."City" = target_city
    AND P."User_ID" NOT IN (
        SELECT U."User_ID"
        FROM "User" U
        WHERE U."Email" = input_identifier OR U."Phone_Number" = input_identifier
    );
END;
$$ LANGUAGE plpgsql;

-- TEST
SELECT * FROM get_users_from_same_city2('zhurst@yahoo.com')

-- 6. Get top n users with the most ticket purchases from a given date onward
CREATE OR REPLACE FUNCTION get_top_buyers_from_date2(start_date DATE, count_limit INT)
RETURNS TABLE (
    User_ID BIGINT,
    Name VARCHAR(50),
    Lastname VARCHAR(50),
    Ticket_Count BIGINT
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

-- TEST
SELECT * FROM get_top_buyers_from_date2('2025-02-01', 5);

-- 7. Show reservations that were cancelled for a specific vehicle type order by reservation date
CREATE OR REPLACE FUNCTION get_cancelled_reservations_by_vehicle_type1(vehicle_type TEXT)
RETURNS TABLE (
    Reservation_ID BIGINT,
    Ticket_ID BIGINT,
    Reservation_Date DATE,
    Reservation_Time TIME,
    Vehicle_Tp TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM (
        -- Airplanes
        SELECT
            R."Reservation_ID",
            R."Ticket_ID",
            R."Reservation_Date",
            R."Reservation_Time",
            'Airplane' AS Vehicle_Tp
        FROM "Reservation" R
        JOIN "Cancellation" C ON C."Reservation_ID" = R."Reservation_ID"
        JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
        JOIN "Route" Ro ON Ro."Route_ID" = T."Route_ID"
        JOIN "Vehicle" V ON V."Vehicle_ID" = T."Vehicle_ID"
        JOIN "Airplane" A ON A."Vehicle_ID" = V."Vehicle_ID"
        WHERE vehicle_type = 'Airplane'

        UNION ALL

        -- Buses
        SELECT
            R."Reservation_ID",
            R."Ticket_ID",
            R."Reservation_Date",
            R."Reservation_Time",
            'Bus' AS Vehicle_Tp
        FROM "Reservation" R
        JOIN "Cancellation" C ON C."Reservation_ID" = R."Reservation_ID"
        JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
        JOIN "Route" Ro ON Ro."Route_ID" = T."Route_ID"
        JOIN "Vehicle" V ON V."Vehicle_ID" = T."Vehicle_ID"
        JOIN "Bus" B ON B."Vehicle_ID" = V."Vehicle_ID"
        WHERE vehicle_type = 'Bus'

        UNION ALL

        -- Trains
        SELECT
            R."Reservation_ID",
            R."Ticket_ID",
            R."Reservation_Date",
            R."Reservation_Time",
            'Train' AS Vehicle_Tp
        FROM "Reservation" R
        JOIN "Cancellation" C ON C."Reservation_ID" = R."Reservation_ID"
        JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
        JOIN "Route" Ro ON Ro."Route_ID" = T."Route_ID"
        JOIN "Vehicle" V ON V."Vehicle_ID" = T."Vehicle_ID"
        JOIN "Train" Tn ON Tn."Vehicle_ID" = V."Vehicle_ID"
        WHERE vehicle_type = 'Train'
    ) AS combined_results
    ORDER BY Reservation_Date, Reservation_Time;
END;
$$ LANGUAGE plpgsql;

-- TEST
SELECT * FROM get_cancelled_reservations_by_vehicle_type1('Bus')

-- 8. Show users who have the most reports for a given topic
CREATE OR REPLACE FUNCTION get_top_reporters_by_topic(topic_input TEXT)
RETURNS TABLE (
    User_ID BIGINT,
    Name VARCHAR(50),
    Lastname VARCHAR(50),
    Report_Count BIGINT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        P."User_ID",
        P."Name",
        P."Lastname",
        COUNT(RP."Report_ID") AS Report_Count
    FROM "Report" RP
    JOIN "Profile" P ON RP."User_ID" = P."User_ID"
    WHERE RP."Type"::TEXT = topic_input
    GROUP BY P."User_ID", P."Name", P."Lastname"
    HAVING COUNT(RP."Report_ID") = (
        SELECT MAX(Sub_Count)
        FROM (
            SELECT COUNT(*) AS Sub_Count
            FROM "Report"
            WHERE "Type"::TEXT = topic_input
            GROUP BY "User_ID"
        ) AS Sub
    );
END;
$$ LANGUAGE plpgsql;

-- Test
SELECT * FROM "Report_Payment";