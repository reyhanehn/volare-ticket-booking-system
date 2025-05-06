-- 1. Find users who have never reserved a ticket
SELECT P."Name", P."Lastname"
FROM "Profile" P
JOIN "User" U ON P."User_ID" = U."User_ID"
WHERE U."Role" = 'Customer' 
AND NOT EXISTS (
    SELECT 1 
    FROM "Reservation" R 
    WHERE R."User_ID" = P."User_ID"
);


SELECT DISTINCT U."User_ID"
FROM "User" U
JOIN "Reservation" R ON R."User_ID" = U."User_ID"


-- 2. Find users who have reserved at least one ticket
SELECT P."Name", P."Lastname"
    FROM "Profile" P
    WHERE EXISTS (
        SELECT 1 
        FROM "Reservation" R
        WHERE R."User_ID" = P."User_ID" AND R."Status" = 'confirmed'
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
    WHERE Re."Status" = 'confirmed'
    GROUP BY Ro."Origin", P."User_ID"
    HAVING COUNT(Re."Reservation_ID") = 1;

-- 5. Find the user who purchased the newest ticket
SELECT P."User_ID", R."Reservation_Date", R."Reservation_Time"
    FROM "Profile" P
    JOIN "Reservation" R ON P."User_ID" = R."User_ID"   
    WHERE R."Status" = 'confirmed'
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
WHERE R."Status" = 'confirmed'

UNION ALL

SELECT 'Train' AS "Transportation", COUNT(R."Reservation_ID") AS "Tickets_Sold"
FROM "Reservation" R
JOIN "Train_Ride" T ON R."Ticket_ID" = T."Ticket_ID"
WHERE R."Status" = 'confirmed'

UNION ALL

SELECT 'Bus' AS "Transportation", COUNT(R."Reservation_ID") AS "Tickets_Sold"
FROM "Reservation" R
JOIN "Bus_Ride" B ON R."Ticket_ID" = B."Ticket_ID"
WHERE R."Status" = 'confirmed';

-- 8. List the top 3 users who bought the most tickets in the past week
SELECT P."User_ID", COUNT(R."Reservation_ID") AS "Tickets_Bought"
    FROM "User" P
    JOIN "Reservation" R ON P."User_ID" = R."User_ID"
    WHERE R."Reservation_Date" >= CURRENT_DATE - INTERVAL '7 days' AND R."Status" = 'confirmed'
    GROUP BY P."User_ID"
    ORDER BY "Tickets_Bought" DESC
    LIMIT 3;


-- 9. List number of tickets sold in Iran, grouped by city
SELECT L."City", COUNT(RE."Reservation_ID") AS "Tickets_Sold"
    FROM "Reservation" RE
    JOIN "Ticket" T ON T."Ticket_ID" = RE."Ticket_ID"
    JOIN "Route" RO ON T."Route_ID" = RO."Route_ID"
    JOIN "Location" L ON L."Location_ID" = RO."Origin"
    WHERE L."Country" = 'Iran' AND RE."Status" = 'confirmed'
    GROUP BY L."City"
    ORDER BY "Tickets_Sold" DESC;


-- 10. List cities where the oldest registered user has made a purchase
SELECT DISTINCT L."City"
    FROM "Profile" P
    JOIN "User" U ON U."User_ID" = P."User_ID"
    JOIN "Reservation" RE ON RE."User_ID" = P."User_ID"
    JOIN "Ticket" T ON T."Ticket_ID" = RE."Ticket_ID"
    JOIN "Route" RO ON T."Route_ID" = RO."Route_ID"
    JOIN "Location" L ON L."Location_ID" = RO."Origin"
    WHERE P."Registration_Date" = (
    SELECT MIN(P2."Registration_Date")
    FROM "Profile" P2
    ) AND RE."Status" = 'confirmed' AND U."Role" = 'Customer'


-- 11. List support users (admins) of the website
SELECT U."User_ID", U."Name", U."Lastname"
    FROM "User" U
    WHERE U."Role" = 'Admin';



-- 12. List users who have purchased at least 2 tickets
SELECT P."User_ID", P."Name", P."Lastname"
    FROM "Profile" P
    JOIN "Reservation" R ON R."User_ID" = P."User_ID"
    WHERE R."Status" = 'confirmed'
    GROUP BY P."User_ID", P."Name", P."Lastname"
    HAVING COUNT(R."Reservation_ID") >= 2;


-- 13. List users who bought at most 2 one type tickets
SELECT P."User_ID", P."Name", P."Lastname"
    FROM "Profile" P
    JOIN "Reservation" R ON R."User_ID" = P."User_ID"
    JOIN "Ticket" T ON R."Ticket_ID" = T."Ticket_ID"
    JOIN "Train_Ride" TR ON TR."Ticket_ID" = T."Ticket_ID"
    WHERE R."Status" = 'confirmed'
    GROUP BY P."User_ID", P."Name", P."Lastname"
    HAVING COUNT(R."Reservation_ID") <= 2;

INTERSECT

SELECT P."User_ID", P."Name", P."Lastname"
    FROM "Profile" P
    JOIN "Reservation" R ON R."User_ID" = P."User_ID"
    JOIN "Ticket" T ON R."Ticket_ID" = T."Ticket_ID"
    JOIN "Flight" F ON F."Ticket_ID" = T."Ticket_ID"
    WHERE R."Status" = 'confirmed'
    GROUP BY P."User_ID", P."Name", P."Lastname"
    HAVING COUNT(R."Reservation_ID") <= 2;

INTERSECT

SELECT P."User_ID", P."Name", P."Lastname"
    FROM "Profile" P
    JOIN "Reservation" R ON R."User_ID" = P."User_ID"
    JOIN "Ticket" T ON R."Ticket_ID" = T."Ticket_ID"
    JOIN "Bus_Ride" BR ON BR."Ticket_ID" = T."Ticket_ID"
    WHERE R."Status" = 'confirmed'
    GROUP BY P."User_ID", P."Name", P."Lastname"
    HAVING COUNT(R."Reservation_ID") <= 2;


-- 14. Users who bought at least one ticket from all 3 vehicle types
-- Users who bought a Flight
SELECT DISTINCT U."Email", U."Phone_Number"
    FROM "User" U
    JOIN "Reservation" R ON R."User_ID" = U."User_ID"
    JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
    JOIN "Flight" F ON F."Ticket_ID" = T."Ticket_ID"
    WHERE R."Status" = 'confirmed'

INTERSECT

-- Users who bought a Train ticket
SELECT DISTINCT U."Email", U."Phone_Number"
    FROM "User" U
    JOIN "Reservation" R ON R."User_ID" = U."User_ID"
    JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
    JOIN "Train_Ride" TR ON TR."Ticket_ID" = T."Ticket_ID"
    WHERE R."Status" = 'confirmed'

INTERSECT

-- Users who bought a Bus ticket
SELECT DISTINCT U."Email", U."Phone_Number"
    FROM "User" U
    JOIN "Reservation" R ON R."User_ID" = U."User_ID"
    JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID"
    JOIN "Bus_Ride" B ON B."Ticket_ID" = T."Ticket_ID"
    WHERE R."Status" = 'confirmed';


-- 15. Get confirmed reservations made for today, ordered by time
SELECT R."Reservation_ID", R."Reservation_Time"
    FROM "Reservation" R 
    WHERE R."Status" = 'Confirmed' AND R."Reservation_Date" = CURRENT_DATE
    ORDER BY R."Reservation_Time";

-- 16. Get the second most reserved ticket and its price
SELECT T."Ticket_ID", T."Price"
    FROM "Ticket" T 
    JOIN "Reservation" R ON R."Ticket_ID" = T."Ticket_ID"
    WHERE R."Status" = 'confirmed'
    GROUP BY T."Ticket_ID", T."Price"
    ORDER BY COUNT(R."Reservation_ID") DESC
    OFFSET 1 LIMIT 1;


-- 17. Get the name of the admin who canceled the most reservations and their percentage
WITH Admin_Cancellation_Count AS (
    SELECT C."Admin_ID", COUNT(*) AS cancel_count
    FROM "Cancellation" C
    JOIN "User" U ON U."User_ID" = C."Admin_ID"
    WHERE U."Role" = 'Admin'
    GROUP BY C."Admin_ID"
    ORDER BY cancel_count DESC
    LIMIT 1
),

Total AS (
    SELECT COUNT(*) AS total
    FROM "Cancellation"
)

SELECT P."Name",
       ROUND((ACC.cancel_count * 100.0) / T.total, 2) AS "Cancel_Percentage"
FROM Admin_Cancellation_Count ACC
JOIN "Profile" P ON P."User_ID" = ACC."Admin_ID"
JOIN Total T ON true;



-- 18. Update the last name of the user with the most cancelled reservations
WITH Most_Cancelled_Reservations AS (
    SELECT P."User_ID"
        FROM "Profile" P
        JOIN "Reservation" R ON R."User_ID" = P."User_ID"
        WHERE R."Status" = 'cancelled'
        GROUP BY P."User_ID"
        ORDER BY COUNT(R."Reservation_ID") DESC
        LIMIT 1
)

UPDATE "Profile" P
    SET "Lastname" = 'redington'
    FROM Most_Cancelled_Reservations MCR
    FROM 
    WHERE MCR."User_ID" = P."User_ID";


-- 19. Delete all reservations of the user with the most cancelled reservations
DELETE FROM "Reservation"
    USING Most_Cancelled_Reservations MCR
    WHERE "Reservation"."User_ID" = MCR."User_ID";



-- 20. Delete all cancelled reservations
DELETE FROM "Reservation"
    WHERE "Reservation"."Status" = 'cancelled';



-- 21. Decrease ticket prices by 10% for tickets sold yesterday by Mahan Airlines
UPDATE "Ticket" T
    SET "Price" = "Price" * 0.9
    FROM "Reservation" R, "Vehicle" V, "Company" C
    WHERE T."Ticket_ID" = R."Ticket_ID"
        AND T."Vehicle_ID" = V."Vehicle_ID"
        AND C."Company_ID" = V."Company_ID"
        AND C."Name" = 'Mahan'
        AND R."Status" = 'confirmed'
        AND R."Reservation_Date" = CURRENT_DATE - INTERVAL '1 day';

    
-- 22. get reports for the most reported ticket
SELECT R."Report_ID", R."Type"
    FROM "Report" R
    JOIN "Report_Ticket" RT ON R."Report_ID" = RT."Report_ID"
    JOIN "Ticket" T ON T."Ticket_ID" = RT."Ticket_ID"
    WHERE T."Ticket_ID" = (
        SELECT Ti."Ticket_ID"
        FROM "Ticket" Ti
        JOIN "Report_Ticket" RTi ON Ti."Ticket_ID" = RTi."Ticket_ID"
        GROUP BY Ti."Ticket_ID"
        ORDER BY COUNT(*) DESC
        LIMIT 1)



