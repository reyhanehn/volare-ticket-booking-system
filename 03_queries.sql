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
