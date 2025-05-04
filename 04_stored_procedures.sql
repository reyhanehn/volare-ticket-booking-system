-- Given Email or Phone Number show all the tickets the user has bought
CREATE OR REPLACE FUNCTION get_reservations_by_contact(
    input_identifier VARCHAR()
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        r."Reservation_ID",
        r."Ticket_ID",
        r."Seat_Number",
        r."Status",
        r."Reservation_Date",
        r."Reservation_Time",
        r."Expiration"
    FROM
        "Reservation" r
        JOIN "User" u ON r."User_ID" = u."User_ID"
    WHERE
        (input_email IS NOT NULL AND u."Email" = input_email)
        OR
        (input_phone IS NOT NULL AND u."Phone_Number" = input_phone)
    ORDER BY
        r."Reservation_Date" ASC, r."Reservation_Time" ASC;
END;
$$ LANGUAGE plpgsql;
