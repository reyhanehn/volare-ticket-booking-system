--  User and Profile Tables
CREATE INDEX idx_user_role ON "User"("Role");
CREATE INDEX idx_user_status ON "User"("Status");

--  Company and Vehicle Tables
CREATE INDEX idx_vehicle_company ON "Vehicle"("Company_ID");
CREATE INDEX idx_vehicle_service_vehicle ON "Vehicle_Service"("Vehicle_ID");

--  Location and Station Tables
CREATE INDEX idx_station_location ON "Station"("Location_ID");

--  Route Table
CREATE INDEX idx_route_origin ON "Route"("Origin");
CREATE INDEX idx_route_destination ON "Route"("Destination");
CREATE INDEX idx_route_departure ON "Route"("Depature_Date");
CREATE INDEX idx_route_arrival ON "Route"("Arrival_Date");
CREATE INDEX idx_route_origin_dest ON "Route"("Origin", "Destination");

--  Ticket Table
CREATE INDEX idx_ticket_vehicle ON "Ticket"("Vehicle_ID");
CREATE INDEX idx_ticket_route ON "Ticket"("Route_ID");
CREATE INDEX idxticket_price ON "Ticket"("Price");

--  Flight Table
CREATE INDEX idx_flight_class_code ON "Flight"("Class_Code");

--  Reservation Table
CREATE INDEX idx_reservation_user ON "Reservation"("User_ID");
CREATE INDEX idx_reservation_ticket ON "Reservation"("Ticket_ID");
CREATE INDEX idx_reservation_status ON "Reservation"("Status");

--  Payment and Wallet_Transaction Tables
CREATE INDEX idx_payment_user ON "Payment"("User_ID");
CREATE INDEX idx_payment_reservation ON "Payment"("Reservation_ID");
CREATE INDEX idx_payment_status ON "Payment"("Status");

CREATE INDEX idx_wallet_tx_wallet ON "Wallet_Transactions"("Wallet_ID");
CREATE INDEX idx_wallet_tx_payment ON "Wallet_Transactions"("Related_Payment_ID");

--  Cancellation Table
CREATE INDEX idx_cancellation_admin ON "Cancellation"("Admin_ID");
CREATE INDEX idx_cancellation_admin ON "Cancellation"("Reservation_ID");

--  Report Table
CREATE INDEX idx_report_user ON "Report"("User_ID");
CREATE INDEX idx_report_admin ON "Report"("Admin_ID");
CREATE INDEX idx_report_status ON "Report"("Status");

CREATE INDEX idx_user_active_status ON "User"("Status") WHERE "Status" = 'Active';

CREATE INDEX idx_reservation_confirmed ON "Reservation"("Status") WHERE "Status" = 'Confirmed';

CREATE INDEX idx_payment_success ON "Payment"("Status") WHERE "Status" = 'Success';