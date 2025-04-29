-- 1. Find users who have never reserved a ticket
SELECT P."Name", P."Lastname"
    FROM "Profile" P
    WHERE NOT EXISTS (
        SELECT 1 
        FROM "Reservation" R
        WHERE R."User_ID" = P."User_ID"
    );

-- 2. Find users who have reserved at least one ticket
SELECT P."Name", P."Lastname"
    FROM "Profile" P
    WHERE EXISTS (
        SELECT 1 
        FROM "Reservation" R
        WHERE R."User_ID" = P."User_ID"
    );

-- 3. Find total payments by each user per month
SELECT P."User_ID", DATE_TRUNC('month', P."Payment_Date") AS "Month", SUM(P."Amount")
    FROM "Payment" P   
    GROUP BY P."User_ID", DATE_TRUNC('month', P."Payment_Date")
    ORDER BY P."User_ID", "Month";

-- 4. Find users who purchased only one ticket per city
SELECT P."User_ID"
    FROM "Profile" P
    JOIN "Reservation" Re ON Re."User_ID" = P."User_ID"
    JOIN "Ticket" T ON T."Ticket_ID" = Re."Ticket_ID"
    JOIN "Route" Ro ON T."Route_ID" = Ro."Route_ID"  
    GROUP BY Ro."Origin", P."User_ID"
    HAVING COUNT(Re."Reservation_ID") = 1;

-- 5. Find user who purchased the newest ticket
SELECT P."User_ID", R."Reservation_Date", R."Reservation_Time"
    FROM "Profile" P
    JOIN "Reservation" R ON P."User_ID" = R."User_ID"   
    ORDER BY R."Reservation_Date" DESC, R."Reservation_Time" DESC
    LIMIT 1;



-- 6. Find users (phone number and email) whose total payment is above the average total payment
WITH User_Total_Payment AS (
    SELECT U."User_ID", SUM(P."Amount") AS Total_Payment
    FROM "User" U
    JOIN "Payment" P ON U."User_ID" = P."User_ID"
    GROUP BY U."User_ID"
)

SELECT U."Phone_Number", U."Email"
    FROM "User" U
    JOIN User_Total_Payment UTP ON U."User_ID" = UTP."User_ID"
    WHERE UTP.Total_Payment > (
        SELECT AVG(Total_Payment)
        FROM User_Total_Payment
    );


-- 7. Show the number of tickets sold for each transport type
SELECT 'Airplane' AS "Transportation", COUNT(R."Reservation_ID") AS "Tickets_Sold"
    FROM "Reservation" R
    JOIN "Flight" F ON R."Ticket_ID" = F."Ticket_ID"

UNION ALL

SELECT 'Train' AS "Transportation", COUNT(R."Reservation_ID") AS "Tickets_Sold"
    FROM "Reservation" R
    JOIN "Train_Ride" T ON R."Ticket_ID" = T."Ticket_ID"

UNION ALL

SELECT 'Bus' AS "Transportation", COUNT(R."Reservation_ID") AS "Tickets_Sold"
    FROM "Reservation" R
    JOIN "Bus_Ride" B ON R."Ticket_ID" = B."Ticket_ID";


-- 8. List the top 3 users who bought the most tickets in the past week
SELECT P."User_ID", COUNT(R."Reservation_ID") AS "Tickets_Bought"
    FROM "User" P
    JOIN "Reservation" R ON P."User_ID" = R."User_ID"
    WHERE R."Reservation_Date" >= CURRENT_DATE - INTERVAL '7 days'
    GROUP BY P."User_ID"
    ORDER BY "Tickets_Bought" DESC
    LIMIT 3;


-- 9. List number of tickets sold in Iran, grouped by city
SELECT L."City", COUNT(RE."Reservation_ID") AS "Tickets_Sold"
    FROM "Reservation" RE
    JOIN "Ticket" T ON T."Ticket_ID" = RE."Ticket_ID"
    JOIN "Route" RO ON T."Route_ID" = RO."Route_ID"
    JOIN "Location" L ON L."Location_ID" = RO."Origin"
    WHERE L."Country" = 'Iran'
    GROUP BY L."City"
    ORDER BY "Tickets_Sold" DESC;
