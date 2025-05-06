DO $$
DECLARE
    seq_name text;
BEGIN
    -- Loop through each sequence in the public schema
    FOR seq_name IN
        SELECT sequence_name
        FROM information_schema.sequences
        WHERE sequence_schema = 'public'
    LOOP
        -- Alter each sequence to restart with 1
        EXECUTE 'ALTER SEQUENCE "' || seq_name || '"RESTART WITH 1';
    END LOOP;
END $$;

-- Insert into location table
INSERT INTO "Location" ("Country", "City") VALUES
('Iran', 'Tehran'), 
('Iran', 'Mashhad'), 
('Iran', 'Shiraz'), 
('Turkey', 'Istanbul'), 
('France', 'Paris'), 
('Germany', 'Berlin'), 
('USA', 'New York'),
('UK', 'London'),
('Japan', 'Tokyo'),
('UAE', 'Dubai'),
('Iran', 'esfahan'),
('Iran', 'Ilam'),
('Iran', 'Bojnord'),
('Iran', 'Tabriz'),
('Iran', 'Ahvaz'),
('Iran', 'Qom'),
('Iran', 'Kerman'),
('Iran', 'Hamedan'),
('Iran', 'Rasht'),
('Iran', 'Kermanshah'),
('Iran', 'Urmia'),
('Iran', 'Yazd'),
('Iran', 'Arak'),
('Iran', 'Bandar Abbas'),
('Iran', 'Sari'),
('Iran', 'Sanandaj'),
('Iran', 'Zahedan'),
('Iran', 'Khorramabad'),
('Iran', 'Gorgan'),
('Iran', 'Karaj'),
('Iran', 'Zanjan'),
('Egypt', 'Cairo'),
('Iran', 'Anzali'),
('Iran', 'Alborz'),
('Russia', 'Moscow'),
('South Korea', 'Seoul'),
('Australia', 'Melbourne'),
('Turkey', 'Ankara'),
('Germany', 'Munich'),
('France', 'Lyon'),
('Brazil', 'Rio de Janeiro'),
('UK', 'Manchester'),
('Italy', 'Rome'),
('Italy', 'Milan'),
('Spain', 'Barcelona'),
('United States', 'Los Angeles'),
('Canada', 'Toronto'),
('Canada', 'Vancouver'),
('United Arab Emirates', 'Dubai'),
('United Arab Emirates', 'Abu Dhabi'),
('China', 'Beijing'),
('China', 'Shanghai'),
('India', 'Mumbai'),
('India', 'Delhi');

-- Insert into user table
INSERT INTO "User" ("Phone_Number", "Email", "Role", "Password_Hash")
VALUES
('+989121000001', 'alireza.rahimi@mail.com', 'Customer', 'AlirezaR@92'),
('+989121000051', 'samaneh.rahimi@mail.com', 'Customer', 'SamanehR@2025'),
('+989121000002', 'sara.karimi@mail.com', 'Customer', 'SaraKarimi!89'),
('+989121000003', 'mohammad.ahmadi@mail.com', 'Customer', 'MohammadA88'),
('+989121000004', 'fatemeh.hosseini@mail.com', 'Customer', 'FatiHoss!77'),
('+989121000005', 'reza.taheri@mail.com', 'Customer', 'RezaTaheri@66'),
('+989121000006', 'shirin.mohseni@mail.com', 'Customer', 'ShirinM@2024'),
('+989121000007', 'hamed.soleimani@mail.com', 'Customer', 'HamedSol99'),
('+989121000008', 'nasim.sadeghi@mail.com', 'Customer', 'NasimS@78'),
('+989121000009', 'ali.moradi@mail.com', 'Customer', 'AliMoradi!87'),
('+989121000010', 'mahsa.farhadi@mail.com', 'Customer', 'MahsaF!98'),
('+989121000011', 'kamran.heidari@mail.com', 'Customer', 'KamranH@77'),
('+989121000012', 'nazanin.esmaeili@mail.com', 'Customer', 'NazaninE@85'),
('+989121000013', 'milad.akbari@mail.com', 'Customer', 'MiladA!123'),
('+989121000014', 'sanaz.talebi@mail.com', 'Customer', 'SanazT99'),
('+989121000015', 'amir.javadi@mail.com', 'Customer', 'AmirJavad@55'),
('+989121000016', 'niloofar.abbasi@mail.com', 'Customer', 'NiloofarA@76'),
('+989121000017', 'hossein.kazemi@mail.com', 'Customer', 'HosseinK@64'),
('+989121000018', 'zahra.rahmani@mail.com', 'Customer', 'ZahraRah@85'),
('+989121000019', 'morteza.jalili@mail.com', 'Customer', 'MortezaJ@91'),
('+989121000020', 'parisa.bagheri@mail.com', 'Customer', 'ParisaB!2023'),
('+989121000021', 'yasin.shahbazi@mail.com', 'Customer', 'YasinS@77'),
('+989121000022', 'dorsa.nikzad@mail.com', 'Customer', 'DorsaN!88'),
('+989121000023', 'omid.behzadi@mail.com', 'Customer', 'OmidB@1990'),
('+989121000024', 'maryam.ebrahimi@mail.com', 'Customer', 'MaryamE!79'),
('+989121000025', 'shahram.mirzaei@mail.com', 'Customer', 'ShahramM@88'),
('+989121000026', 'samira.fattahi@mail.com', 'Customer', 'SamiraF!69'),
('+989121000027', 'behzad.ansari@mail.com', 'Customer', 'BehzadA@73'),
('+989121000028', 'tina.keshavarz@mail.com', 'Customer', 'TinaKesh@92'),
('+989121000029', 'navid.shafiei@mail.com', 'Customer', 'NavidS!95'),
('+989121000030', 'elham.noori@mail.com', 'Customer', 'ElhamN@91'),
('+989111234567', 'alireza.mohammadi@gmail.com', 'Customer','AliReza123'),
('+989121234568', 'sara.karimi@yahoo.com', 'Customer','SaraKari!'),
('+989131234569', 'mohsen.taheri@outlook.com', 'Customer', 'MohTaheri89'),
('+989141234560', 'fatemeh.ahmadi@gmail.com', 'Customer', 'Fati@1357'),
('+989151234561', 'hossein.hosseini@gmail.com', 'Customer','Hossein998'),
('+989161234562', 'maryam.jafari@yahoo.com', 'Customer','Maryam*78'),
('+989171234563', 'amir.rezai@outlook.com', 'Customer', 'AmirRez321'),
('+989181234564', 'zahra.sadeghi@gmail.com', 'Customer', 'ZahraS34'),
('+989191234565', 'milad.rashidi@yahoo.com', 'Customer', 'MiladR!22'),
('+989901234566', 'parisa.shahbazi@gmail.com', 'Customer', 'PariShz01'),
('+989021234567', 'arman.soltani@gmail.com', 'Customer', 'ArmanPass'),
('+989031234568', 'shirin.khademi@yahoo.com', 'Customer', 'Shirin12!'),
('+989041234569', 'ehsan.nikzad@outlook.com', 'Customer',  'EhsanN00'),
('+989051234560', 'simin.bagheri@gmail.com', 'Customer', 'SiminBagh@1'),
('+989061234561', 'omid.golzar@yahoo.com', 'Customer',  'Omid1234'),
('+989071234562', 'leila.rahimi@gmail.com', 'Customer',  'LeilaR99'),
('+989081234563', 'navid.shams@yahoo.com', 'Customer', 'NavidShams8'),
('+989091234564', 'taraneh.esmaili@outlook.com', 'Customer',  'TaraEs78'),
('+989101234565', 'kamran.abbasi@gmail.com', 'Customer', 'Kamran7!'),
('+989111234566', 'samira.yazdani@yahoo.com', 'Customer', 'SamiraYz9');

-- insert into profile table
INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City_ID") VALUES
(1, 'Alireza', 'Rahimi', 1),
(2, 'Samaneh', 'Rahimi', 1),
(3, 'Sara', 'Karimi', 2),
(4, 'Mohammad', 'Ahmadi', 3),
(5, 'Fatemeh', 'Hosseini', 14),
(6, 'Reza', 'Taheri', 15),
(7, 'Shirin', 'Mohseni', 16),
(8, 'Hamed', 'Soleimani', 17),
(9, 'Nasim', 'Sadeghi', 18),
(10, 'Ali', 'Moradi', 19),
(11, 'Mahsa', 'Farhadi', 20),
(12, 'Kamran', 'Heidari', 21),
(13, 'Nazanin', 'Esmaeili', 22),
(14, 'Milad', 'Akbari', 23),
(15, 'Sanaz', 'Talebi', 24),
(16, 'Amir', 'Javadi', 25),
(17, 'Niloofar', 'Abbasi', 26),
(18, 'Hossein', 'Kazemi', 27),
(19, 'Zahra', 'Rahmani', 28),
(20, 'Morteza', 'Jalili', 29),
(21, 'Parisa', 'Bagheri', 30),
(22, 'Yasin', 'Shahbazi', 31),
(23, 'Dorsa', 'Nikzad', 38),
(24, 'Omid', 'Behzadi', 39),
(25, 'Maryam', 'Ebrahimi', 34),
(26, 'Shahram', 'Mirzaei', 30),
(27, 'Samira', 'Fattahi', 10),
(28, 'Behzad', 'Ansari', 20),
(29, 'Tina', 'Keshavarz', 4),
(30, 'Navid', 'Shafiei', 13),
(31, 'Elham', 'Noori', 24),
(32, 'Alireza', 'Mohammadi', 15),
(33, 'Sara', 'Karimi', 1),
(34, 'Mohsen', 'Taheri', 1),
(35, 'Fatemeh', 'Ahmadi', 5),
(36, 'Hossein', 'Hosseini', 2),
(37, 'Maryam', 'Jafari', 1),
(38, 'Amir', 'Rezai', 2),
(39, 'Zahra', 'Sadeghi', 3),
(40, 'Milad', 'Rashidi', 14),
(41, 'Parisa', 'Shahbazi', 15),
(42, 'Arman', 'Soltani', 16),
(43, 'Shirin', 'Khademi', 17),
(44, 'Ehsan', 'Nikzad', 18),
(45, 'Simin', 'Bagheri', 19),
(46, 'Omid', 'Golzar', 20),
(47, 'Leila', 'Rahimi', 21),
(48, 'Navid', 'Shams', 22),
(49, 'Taraneh', 'Esmaili', 23),
(50, 'Kamran', 'Abbasi', 24),
(51, 'Samira', 'Yazdani', 25);

-- insert into company table
INSERT INTO "Company" ("Name", "Headquarters", "Year_Of_Establishment", "Contact_Number") VALUES
('SkyTravel', 'Tehran', 1998, '02112345678'),
('BlueBus', 'Mashhad', 2005, '02123456789'),
('RajaTrains', 'Isfahan', 1980, '02134567890'),
('SunWings', 'Shiraz', 2002, '02145678901'),
('GreenRoutes', 'Tabriz', 2010, '02156789012'),
('GlobalExpress', 'Yazd', 1995, '02167890123');

-- Insert vehicles into Vehicle table
INSERT INTO "Vehicle" ("Company_ID", "Name") VALUES
(1, 'Boeing 747'),
(1, 'Airbus A320'),
(4, 'Embraer 190'),
(1, 'Boeing 777'),
(4, 'Airbus A330'),
(6, 'Bombardier CRJ900'),
(6, 'Airbus A350'),
(1, 'Boeing 737'),
(4, 'ATR 72'),
(6, 'Gulfstream G650'),
(2, 'Volvo 9700'),
(2, 'Scania Touring'),
(5, 'Mercedes-Benz Travego'),
(2, 'MAN Lion''s Coach'),
(5, 'Setra S 431 DT'),
(2, 'Irizar i6'),
(5, 'Neoplan Cityliner'),
(2, 'King Long XMQ'),
(5, 'Yutong ZK6122'),
(5, 'Volvo B9R'),
(3, 'Raja Compartment'),
(3, 'Raja Coach 1'),
(4, 'Shiraz Express'),
(2, 'Mashhad Liner'),
(6, 'Desert Express'),
(5, 'Green Valley Rail'),
(1, 'Capital Coach'),
(6, 'Sunset Rail'),
(5, 'Royal Compartment'),
(1, 'Golden Line');


INSERT INTO "Airplane" ("Vehicle_ID", "First_Class_Capacity", "Business_Class_Capacity", "Economy_Class_Capacity") VALUES
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Boeing 747'), 20, 50, 300),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Airbus A320'), 10, 30, 150),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Embraer 190'), 5, 20, 80),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Boeing 777'), 30, 60, 250),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Airbus A330'), 15, 40, 220),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Bombardier CRJ900'), 4, 16, 70),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Airbus A350'), 25, 45, 270),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Boeing 737'), 8, 24, 130),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'ATR 72'), 2, 10, 60),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Gulfstream G650'), 5, 5, 10);

INSERT INTO "Bus" ("Vehicle_ID", "Type", "Seats_Count", "Seats_In_Row") VALUES
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Volvo 9700'), 'VIP', 30, '1+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Scania Touring'), 'Normal', 44, '2+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Mercedes-Benz Travego'), 'VIP', 32, '1+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'MAN Lion''s Coach'), 'Normal', 46, '2+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Setra S 431 DT'), 'VIP', 28, '1+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Irizar i6'), 'Normal', 48, '2+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Neoplan Cityliner'), 'VIP', 30, '1+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'King Long XMQ'), 'Normal', 50, '2+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Yutong ZK6122'), 'VIP', 32, '1+2'),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Volvo B9R'), 'Normal', 42, '2+2');


INSERT INTO "Train" ("Vehicle_ID", "Type", "Stars", "Seats_Count", "Seats_In_Cabin", "Freight_Wagons_Count") VALUES
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Raja Compartment'), 'Compartment', 4, 200, 40, 8),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Raja Coach 1'), 'Coach', 3, 250, 250, 10),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Shiraz Express'), 'Compartment', 5, 180, 30, 7),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Mashhad Liner'), 'Compartment', 4, 160, 40, 6),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Desert Express'), 'Compartment', 5, 140, 28, 5),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Green Valley Rail'), 'Compartment', 3, 180, 36, 8),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Capital Coach'), 'Coach', 4, 260, 260, 11),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Sunset Rail'), 'Compartment', 4, 200, 40, 7),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Royal Compartment'), 'Compartment', 5, 150, 30, 6),
((SELECT "Vehicle_ID" FROM "Vehicle" WHERE "Name" = 'Golden Line'), 'Coach', 3, 220, 220, 9);


-- update the passwords in user table
UPDATE "User"
SET "Password_Hash" = CASE
        WHEN "User_ID" = 1 THEN '$2b$12$RwhdqNNACUqIfOgbgNApf.FNLo1z1Gtq1yInaq1cGQq9o6CMTpY3i'
        WHEN "User_ID" = 2 THEN '$2b$12$EiwdzGalRndcshwwbqek7.r0M8f0.vOh40VSfmiYCoSPZZCqPg1aq'
        WHEN "User_ID" = 3 THEN '$2b$12$QAoO7Epw4VajVg2ADdK7wOOmxGhsu4ILWTouikSttetzUlg6qwWOq'
        WHEN "User_ID" = 4 THEN '$2b$12$dP.T06kmj6.FeKGEVKxnoOzuUHmxhq05jpDI4Gv0LhAoW2JPWjiou'
        WHEN "User_ID" = 5 THEN '$2b$12$R3JnGUdqXgudDQ2twPMEmOfJg2qF0kyCiOrIyPZBoxeHuAUv6Gdsq'
        WHEN "User_ID" = 6 THEN '$2b$12$sgK1b8prvBsfwM6729V3puvvXlMG8Q7Wv09mhzbDS07YHjGRbkcSe'
        WHEN "User_ID" = 7 THEN '$2b$12$A2Zpjs/ZOiDEWWYWMovS.OYkZ8Pku5lh54ZJXZHWpRNRqgBdeiZCm'
        WHEN "User_ID" = 8 THEN '$2b$12$m.PpXc4hD3xF37Pbd8Yp9.katKH9P1CacNT8Y38PYuy1tVrKepFsm'
        WHEN "User_ID" = 9 THEN '$2b$12$L7ewSLTjo4DdF9z0HKnT4ebUvyDvXIBUhUOS5RGQ1lf7p9j3fz..q'
        WHEN "User_ID" = 10 THEN '$2b$12$1BBTL/OocombGhRbsjCJUu5N4ebkPK6txjhzrD9lUu1sdZ3yS3eXe'
        WHEN "User_ID" = 11 THEN '$2b$12$yH04xV4nW70AGmPEp2L.M.w8u29aicB3QlCp4chEmByrH2fuvbAva'
        WHEN "User_ID" = 12 THEN '$2b$12$UbjhPi.II2Ea2Bbb4eQ/..KvfiKBzGlJdAs09SxDcRiJnVPgRHuTW'
        WHEN "User_ID" = 13 THEN '$2b$12$ZGj1x1nnwlHTPTo5mQ9g0OsSIB8dqf/.uYbLEdGInKII2yc.zFobi'
        WHEN "User_ID" = 14 THEN '$2b$12$r9IwTRHLtALUtL0ddwlPHO3ypGHuw//1q3GaM4RppBDPa2Htmnsue'
        WHEN "User_ID" = 15 THEN '$2b$12$RkAga0XOHVS.CjN0UV9Yk.l.u9tbS5.HDHzd4qyZ/sBJX1D22wGxO'
        WHEN "User_ID" = 16 THEN '$2b$12$Jn2gSTuhXYaWdTTp25YglufMfLuYvByC0yUNbPeXHGDB2h39TDY/G'
        WHEN "User_ID" = 17 THEN '$2b$12$5.0Oil90tEN9zK8G6ZZzGuB19FpWYgYDoHGGqRtf6vgUu07hcsrp6'
        WHEN "User_ID" = 18 THEN '$2b$12$meOMTWRMBS9ZFZUIeuoFxuGpsRDpNYSAQ0AhToWGJT3Fsh5geLAbK'
        WHEN "User_ID" = 19 THEN '$2b$12$3RxuT.43KHGwRYco3FRxPei/rHexibqd5ygUq8r4mzfik9DIzxMaG'
        WHEN "User_ID" = 20 THEN '$2b$12$q03ywkxk25uWll1k.EUdY.sB5lzDib0r3UoT1MT7sZRYa2ZGqyIXG'
        WHEN "User_ID" = 21 THEN '$2b$12$p44DdVV7Ly4XU7ZZo1h.nO2hQo.vmSI9YRY3YWboEERNR28rGAlye'
        WHEN "User_ID" = 22 THEN '$2b$12$ILL0Dn0gk4S6JGbEwDkwSOsAmFkjc5U92z16qFinMyquK94j0ukvi'
        WHEN "User_ID" = 23 THEN '$2b$12$.fuK8aa9jHLKH6beuKJB9OCE0rULPF9q1pgJHhW6R0W1f1Pxm5uHG'
        WHEN "User_ID" = 24 THEN '$2b$12$cCt49M5BNawklorye0i2b.n8tPivvhDcezwtfvcg15ztPY6A0t9zK'
        WHEN "User_ID" = 25 THEN '$2b$12$X5QxJXU0FSIq2DPHCNZLw.O/GVBvNr/yQF.RVbLC3PBdErGfmYMKa'
        WHEN "User_ID" = 26 THEN '$2b$12$CG4jkb9l8QN6i8LqdZcTgOZc8NtWdusA5MN3Qof/QSS18FZ9KDKUC'
        WHEN "User_ID" = 27 THEN '$2b$12$uC6NWMpyIg0QqxwDhAF0s.Ul99aswgF1Nt3NZP6xxFUOVpunY.OEK'
        WHEN "User_ID" = 28 THEN '$2b$12$S5fJZmZPmuWPEzDfyMMpmOkgbGreei6nFBddpkV26uXUonwuh8KyS'
        WHEN "User_ID" = 29 THEN '$2b$12$g1Hy13ZQIENGapMM9Fj0Z.Yuvurk.fWPy0Wm4cOpOkj1WXGN.YtKW'
        WHEN "User_ID" = 30 THEN '$2b$12$vmtDJHgSY7CQjq.r17zQPe8ORlMiKFC/Azi3d1u90mBaDWnkG7HZq'
        WHEN "User_ID" = 31 THEN '$2b$12$ba3gT45lFQmTdEmNcsXM2.n6hBbB/Hpa9YCHFX0Dl0ZlfCF36CuPi'
        WHEN "User_ID" = 32 THEN '$2b$12$.zgVhzY9Tsh69J1SIEzCKuhqzqdWTCVdgbJvtQxs44z89R72VUvH6'
        WHEN "User_ID" = 33 THEN '$2b$12$PTbALMV2x51Ix/EI2D6yxetE9obEjQnOn1nDNqRZoiKmdhMNhXl42'
        WHEN "User_ID" = 34 THEN '$2b$12$haVcUe1k.MYdIKxSd8Is3eybr/HpT3pANY9quiRskCXxrDtY.VE4u'
        WHEN "User_ID" = 35 THEN '$2b$12$eqBB2EZReQwEtZ/cJbEgKuLbjBJ3sjdSunvVvl0Zl4MPqumKzYs2u'
        WHEN "User_ID" = 36 THEN '$2b$12$2OzDWEn0xiNUzQAhmMNEeOGisMYB5lWTyUQAfRX92usT1Fbnf40Jy'
        WHEN "User_ID" = 37 THEN '$2b$12$z/1xwzW9lxGE9tR4mv0dMOxJMRxIURaiVI/A7z7xRY0F2RylrK0bq'
        WHEN "User_ID" = 38 THEN '$2b$12$t0FxcwD5V5E56e7t/4S9u.4b3/D95yBbULUs8rMpEWsn80TIYD9RC'
        WHEN "User_ID" = 39 THEN '$2b$12$/1yJQqDY1C1MXQQskOYI1uWP9CzG7De35ozWazyrrxAznu4zCEURG'
        WHEN "User_ID" = 40 THEN '$2b$12$rsUpPPEWQWGGyNuNogPHkOOPza4KVt/Ui3w/iExePw7DB9tWQsuw.'
        WHEN "User_ID" = 41 THEN '$2b$12$D83I9hcfZf.S5hGs/zAEL.o.v3XoGMKYOIQ/Br40dMLRiYBi//HmW'
        WHEN "User_ID" = 42 THEN '$2b$12$jIDO4ZZJbR5CmbcMVKRSKuPB7oUSsVUILVknxb4p6H9U6Hlxcsdb.'
        WHEN "User_ID" = 43 THEN '$2b$12$9YokOyzoHsuDoTQpWqaqveHrx1zoQLNv979To88HCeEWwc0E.Mqxi'
        WHEN "User_ID" = 44 THEN '$2b$12$54dGyThAY5rQulLz8IWhWuRK918LDDmgLGqLkNmE/nTnfIRqqFDZ.'
        WHEN "User_ID" = 45 THEN '$2b$12$Q.SqPLdQ1tt2kYfqjLch7.JUeo3LepwqGM2yqVcwNMbh1PdGhO.0m'
        WHEN "User_ID" = 46 THEN '$2b$12$acxCjlG1mB1mlwIgihqbM.D0VpLjewjhfGwY6FoLIqkvlHw8h2OIG'
        WHEN "User_ID" = 47 THEN '$2b$12$gjwUPmPisX/ik4oEfi8Oiuei.l0i0mGgrwlJG2/PQ/4XIFM9PWg/y'
        WHEN "User_ID" = 48 THEN '$2b$12$898iMIz6FNyJUkJUCo6U/.QucgXAM/e5k45syHWB7xYnQC8hWoO5O'
        WHEN "User_ID" = 49 THEN '$2b$12$vKOKzTidk54xw.B2g2/Q6esZjomoy9OQu/CNeAmudZ9E/NWueC58m'
        WHEN "User_ID" = 50 THEN '$2b$12$GNC36npqVTavGmoZLZ1Bze3QU7fLemQ1Uk.FNUT.Z34xhdFNg8VTG'
        WHEN "User_ID" = 51 THEN '$2b$12$wxOgvuphOJAQsuRC6a5lz.9GFc2CtjVAElxw736lymIasFdnIVulC'
        ELSE "Password_Hash"
END;

-- insert into station 
INSERT INTO "Station" ("Name", "Type", "Location_ID") VALUES
('Tehran Bus Station', 'Bus_Station', 1),
('Tehran Train Station', 'Train_Station', 1),
('Tehran Airport', 'Airport', 1),

('Mashhad Bus Station', 'Bus_Station', 2),
('Mashhad Train Station', 'Train_Station', 2),
('Mashhad Airport', 'Airport', 2),

('Shiraz Bus Station', 'Bus_Station', 3),
('Shiraz Train Station', 'Train_Station', 3),
('Shiraz Airport', 'Airport', 3),

('Istanbul Bus Station', 'Bus_Station', 4),
('Istanbul Train Station', 'Train_Station', 4),
('Istanbul Airport', 'Airport', 4),

('Paris Bus Station', 'Bus_Station', 5),
('Paris Train Station', 'Train_Station', 5),
('Paris Airport', 'Airport', 5),

('Berlin Bus Station', 'Bus_Station', 6),
('Berlin Train Station', 'Train_Station', 6),
('Berlin Airport', 'Airport', 6),

('New York Bus Station', 'Bus_Station', 7),
('New York Train Station', 'Train_Station', 7),
('New York Airport', 'Airport', 7),

('London Bus Station', 'Bus_Station', 8),
('London Train Station', 'Train_Station', 8),
('London Airport', 'Airport', 8),

('Tokyo Bus Station', 'Bus_Station', 9),
('Tokyo Train Station', 'Train_Station', 9),
('Tokyo Airport', 'Airport', 9),

('Dubai Bus Station', 'Bus_Station', 10),
('Dubai Train Station', 'Train_Station', 10),
('Dubai Airport', 'Airport', 10),

('Esfahan Bus Station', 'Bus_Station', 11),
('Esfahan Train Station', 'Train_Station', 11),
('Esfahan Airport', 'Airport', 11),

('Ilam Bus Station', 'Bus_Station', 12),
('Ilam Train Station', 'Train_Station', 12),
('Ilam Airport', 'Airport', 12),

('Bojnord Bus Station', 'Bus_Station', 13),
('Bojnord Train Station', 'Train_Station', 13),
('Bojnord Airport', 'Airport', 13),

('Tabriz Bus Station', 'Bus_Station', 14),
('Tabriz Train Station', 'Train_Station', 14),
('Tabriz Airport', 'Airport', 14),

('Ahvaz Bus Station', 'Bus_Station', 15),
('Ahvaz Train Station', 'Train_Station', 15),
('Ahvaz Airport', 'Airport', 15),

('Qom Bus Station', 'Bus_Station', 16),
('Qom Train Station', 'Train_Station', 16),
('Qom Airport', 'Airport', 16),

('Kerman Bus Station', 'Bus_Station', 17),
('Kerman Train Station', 'Train_Station', 17),
('Kerman Airport', 'Airport', 17),

('Hamedan Bus Station', 'Bus_Station', 18),
('Hamedan Train Station', 'Train_Station', 18),
('Hamedan Airport', 'Airport', 18),

('Rasht Bus Station', 'Bus_Station', 19),
('Rasht Train Station', 'Train_Station', 19),
('Rasht Airport', 'Airport', 19),

('Kermanshah Bus Station', 'Bus_Station', 20),
('Kermanshah Train Station', 'Train_Station', 20),
('Kermanshah Airport', 'Airport', 20),

('Urmia Bus Station', 'Bus_Station', 21),
('Urmia Train Station', 'Train_Station', 21),
('Urmia Airport', 'Airport', 21),

('Yazd Bus Station', 'Bus_Station', 22),
('Yazd Train Station', 'Train_Station', 22),
('Yazd Airport', 'Airport', 22),

('Arak Bus Station', 'Bus_Station', 23),
('Arak Train Station', 'Train_Station', 23),
('Arak Airport', 'Airport', 23),

('Bandar Abbas Bus Station', 'Bus_Station', 24),
('Bandar Abbas Train Station', 'Train_Station', 24),
('Bandar Abbas Airport', 'Airport', 24),

('Sari Bus Station', 'Bus_Station', 25),
('Sari Train Station', 'Train_Station', 25),
('Sari Airport', 'Airport', 25),

('Sanandaj Bus Station', 'Bus_Station', 26),
('Sanandaj Train Station', 'Train_Station', 26),
('Sanandaj Airport', 'Airport', 26),

('Zahedan Bus Station', 'Bus_Station', 27),
('Zahedan Train Station', 'Train_Station', 27),
('Zahedan Airport', 'Airport', 27),

('Khorramabad Bus Station', 'Bus_Station', 28),
('Khorramabad Train Station', 'Train_Station', 28),
('Khorramabad Airport', 'Airport', 28),

('Gorgan Bus Station', 'Bus_Station', 29),
('Gorgan Train Station', 'Train_Station', 29),
('Gorgan Airport', 'Airport', 29),

('Karaj Bus Station', 'Bus_Station', 30),
('Karaj Train Station', 'Train_Station', 30),
('Karaj Airport', 'Airport', 30),

('Zanjan Bus Station', 'Bus_Station', 31),
('Zanjan Train Station', 'Train_Station', 31),
('Zanjan Airport', 'Airport', 31),

('Cairo Bus Station', 'Bus_Station', 32),
('Cairo Train Station', 'Train_Station', 32),
('Cairo Airport', 'Airport', 32),

('Anzali Bus Station', 'Bus_Station', 33),
('Anzali Train Station', 'Train_Station', 33),
('Anzali Airport', 'Airport', 33),

('Alborz Bus Station', 'Bus_Station', 34),
('Alborz Train Station', 'Train_Station', 34),
('Alborz Airport', 'Airport', 34),

('Moscow Bus Station', 'Bus_Station', 35),
('Moscow Train Station', 'Train_Station', 35),
('Moscow Airport', 'Airport', 35),

('Seoul Bus Station', 'Bus_Station', 36),
('Seoul Train Station', 'Train_Station', 36),
('Seoul Airport', 'Airport', 36),

('Melbourne Bus Station', 'Bus_Station', 37),
('Melbourne Train Station', 'Train_Station', 37),
('Melbourne Airport', 'Airport', 37),


('Ankara Bus Station', 'Bus_Station', 38),
('Ankara Train Station', 'Train_Station', 38),
('Ankara Airport', 'Airport', 38),

('Munich Bus Station', 'Bus_Station', 39),
('Munich Train Station', 'Train_Station', 39),
('Munich Airport', 'Airport', 39),

('Lyon Bus Station', 'Bus_Station', 40),
('Lyon Train Station', 'Train_Station', 40),
('Lyon Airport', 'Airport', 40),

('Rio de Janeiro Bus Station', 'Bus_Station', 41),
('Rio de Janeiro Train Station', 'Train_Station', 41),
('Rio de Janeiro Airport', 'Airport', 41),

('Manchester Bus Station', 'Bus_Station', 42),
('Manchester Train Station', 'Train_Station', 42),
('Manchester Airport', 'Airport', 42),

('Rome Bus Station', 'Bus_Station', 43),
('Rome Train Station', 'Train_Station', 43),
('Rome Airport', 'Airport', 43),

('Milan Bus Station', 'Bus_Station', 44),
('Milan Train Station', 'Train_Station', 44),
('Milan Airport', 'Airport', 44),

('Barcelona Bus Station', 'Bus_Station', 45),
('Barcelona Train Station', 'Train_Station', 45),
('Barcelona Airport', 'Airport', 45),

('Los Angeles Bus Station', 'Bus_Station', 46),
('Los Angeles Train Station', 'Train_Station', 46),
('Los Angeles Airport', 'Airport', 46),

('Toronto Bus Station', 'Bus_Station', 47),
('Toronto Train Station', 'Train_Station', 47),
('Toronto Airport', 'Airport', 47),

('Vancouver Bus Station', 'Bus_Station', 48),
('Vancouver Train Station', 'Train_Station', 48),
('Vancouver Airport', 'Airport', 48),

('Dubai Bus Station', 'Bus_Station', 49),
('Dubai Train Station', 'Train_Station', 49),
('Dubai Airport', 'Airport', 49),

('Abu Dhabi Bus Station', 'Bus_Station', 50),
('Abu Dhabi Train Station', 'Train_Station', 50),
('Abu Dhabi Airport', 'Airport', 50),

('Beijing Bus Station', 'Bus_Station', 51),
('Beijing Train Station', 'Train_Station', 51),
('Beijing Airport', 'Airport', 51),

('Shanghai Bus Station', 'Bus_Station', 52),
('Shanghai Train Station', 'Train_Station', 52),
('Shanghai Airport', 'Airport', 52),

('Mumbai Bus Station', 'Bus_Station', 53),
('Mumbai Train Station', 'Train_Station', 53),
('Mumbai Airport', 'Airport', 53),

('Delhi Bus Station', 'Bus_Station', 54),
('Delhi Train Station', 'Train_Station', 54),
('Delhi Airport', 'Airport', 54);

--  insert into passenger 
INSERT INTO "Passenger" ("Name", "Lastname", "SSN", "Birthdate")
SELECT
  p."Name",
  p."Lastname",
  LPAD((ROW_NUMBER() OVER () + 1000000000)::TEXT, 10, '0') AS "SSN",
  DATE '1960-01-01' + (random() * 20000)::INT  -- birthdates between ~1960–2015
FROM "Profile" p;

INSERT INTO "Passenger" ("Name", "Lastname", "SSN", "Birthdate") VALUES
('Ali',        'Karimi',       '3000000001', DATE '1985-03-12'),
('Sara',       'Ahmadi',       '3000000002', DATE '1992-07-25'),
('Reza',       'Mohammadi',    '3000000003', DATE '1978-11-09'),
('Fatemeh',    'Hashemi',      '3000000004', DATE '1989-01-14'),
('Hossein',    'Ghorbani',     '3000000005', DATE '1995-04-02'),
('Narges',     'Alizadeh',     '3000000006', DATE '1970-10-20'),
('Mehdi',      'Rahimi',       '3000000007', DATE '1982-06-06'),
('Zahra',      'Kazemi',       '3000000008', DATE '1997-12-19'),
('Milad',      'Ebrahimi',     '3000000009', DATE '2000-08-08'),
('Leila',      'Najafi',       '3000000010', DATE '1986-05-27'),
('Amir',       'Rostami',      '3000000011', DATE '1993-09-15'),
('Maryam',     'Shahidi',      '3000000012', DATE '1975-04-30'),
('Pouya',      'Jafari',       '3000000013', DATE '1988-02-11'),
('Hanieh',     'Moradi',       '3000000014', DATE '1999-06-13'),
('Saeed',      'Farhadi',      '3000000015', DATE '1969-07-04'),
('Yasaman',    'Nouri',        '3000000016', DATE '1990-10-29'),
('Alireza',    'Kaviani',      '3000000017', DATE '1973-01-19'),
('Elham',      'Shahrami',     '3000000018', DATE '1983-03-03'),
('Sina',       'Tavakoli',     '3000000019', DATE '1996-08-23'),
('Arezoo',     'Taheri',       '3000000020', DATE '1977-12-01');

-- insert into route
WITH RandomStations AS (
    SELECT
        s1."Station_ID" AS origin_station,
        s2."Station_ID" AS destination_station,
        s1."Type", 
        l1."Location_ID" AS origin_location,  
        l2."Location_ID" AS destination_location  
    FROM
        "Station" s1  
    JOIN
        "Station" s2 ON s1."Type" = s2."Type"  
    JOIN
        "Location" l1 ON l1."Location_ID" = s1."Location_ID"  
    JOIN
        "Location" l2 ON l2."Location_ID" = s2."Location_ID"  
    WHERE
        s1."Station_ID" != s2."Station_ID"  
    ORDER BY
        RANDOM()
    LIMIT 40  
),
RandomDates AS (
   
    SELECT
        TO_DATE('2025-06-01', 'YYYY-MM-DD') + (RANDOM() * 90) * INTERVAL '1 day' AS random_date,
        TO_TIMESTAMP('2025-06-01 06:00:00', 'YYYY-MM-DD HH24:MI:SS') + (RANDOM() * (INTERVAL '12 hour')) AS departure_time,
        TO_TIMESTAMP('2025-06-01 09:00:00', 'YYYY-MM-DD HH24:MI:SS') + (RANDOM() * (INTERVAL '12 hour')) AS arrival_time
    FROM
        generate_series(1, 40)  
)

INSERT INTO "Route" ("Origin", "Destination", "Origin_Station", "Destination_Station", "Departure_Date", "Departure_Time", "Arrival_Date", "Arrival_Time")
SELECT
    rs.origin_location, rs.destination_location, rs.origin_station, rs.destination_station, rd.random_date, rd.departure_time, rd.random_date, rd.arrival_time
FROM
    RandomStations rs
JOIN
    RandomDates rd ON TRUE  
WHERE
    rd.departure_time < rd.arrival_time;  

-- Insert data into the Ticket table
WITH TicketData AS (
    INSERT INTO "Ticket" ("Vehicle_ID", "Route_ID", "Price", "Remaining_Capacity")
    SELECT 
        -- Select a vehicle based on the station type (Airport -> Airplane, Train_Station -> Train, Bus_Station -> Bus)
        CASE 
            WHEN s1."Type" = 'Airport' OR s2."Type" = 'Airport' THEN
                -- Select a random airplane vehicle
                (SELECT "Vehicle_ID" FROM "Airplane" ORDER BY RANDOM() LIMIT 1)
            WHEN s1."Type" = 'Train_Station' OR s2."Type" = 'Train_Station' THEN
                -- Select a random train vehicle
                (SELECT "Vehicle_ID" FROM "Train" ORDER BY RANDOM() LIMIT 1)
            WHEN s1."Type" = 'Bus_Station' OR s2."Type" = 'Bus_Station' THEN
                -- Select a random bus vehicle
                (SELECT "Vehicle_ID" FROM "Bus" ORDER BY RANDOM() LIMIT 1)
        END AS "Vehicle_ID",
        
        r."Route_ID",  -- From the Route table
        ROUND((RANDOM() * (500 - 50) + 50)::numeric, 2) AS "Price",  -- Random price between 50 and 500
        FLOOR(RANDOM() * (100 - 10) + 10) AS "Remaining_Capacity"  -- Random remaining capacity between 10 and 100
    FROM 
        "Route" r
    JOIN 
        "Station" s1 ON r."Origin_Station" = s1."Station_ID"
    JOIN 
        "Station" s2 ON r."Destination_Station" = s2."Station_ID"
    WHERE 
        s1."Type" IN ('Airport', 'Train_Station', 'Bus_Station') OR s2."Type" IN ('Airport', 'Train_Station', 'Bus_Station')
    RETURNING "Ticket_ID", "Vehicle_ID", "Route_ID", "Price", "Remaining_Capacity"
)
SELECT * FROM TicketData;


--insert into flight and train and bus table
SELECT 
    t."Ticket_ID",
    t."Vehicle_ID",
    CASE
        WHEN a."Vehicle_ID" IS NOT NULL THEN 'Airplane'
        WHEN b."Vehicle_ID" IS NOT NULL THEN 'Bus'
        WHEN tr."Vehicle_ID" IS NOT NULL THEN 'Train'
        ELSE 'Unknown'
    END AS "Vehicle_Type",  -- Determining vehicle type based on the vehicle table it belongs to
    t."Route_ID",
    t."Price",
    t."Remaining_Capacity",
    r."Departure_Date",
    r."Departure_Time",
    r."Arrival_Date",
    r."Arrival_Time",
    s1."Station_ID" AS "Origin_Station_ID",
    s1."Type" AS "Origin_Station_Type",
    s2."Station_ID" AS "Destination_Station_ID",
    s2."Type" AS "Destination_Station_Type"
FROM 
    "Ticket" t
JOIN 
    "Route" r ON t."Route_ID" = r."Route_ID"
JOIN 
    "Station" s1 ON r."Origin_Station" = s1."Station_ID"
JOIN 
    "Station" s2 ON r."Destination_Station" = s2."Station_ID"
LEFT JOIN 
    "Airplane" a ON t."Vehicle_ID" = a."Vehicle_ID"
LEFT JOIN 
    "Bus" b ON t."Vehicle_ID" = b."Vehicle_ID"
LEFT JOIN 
    "Train" tr ON t."Vehicle_ID" = tr."Vehicle_ID"
ORDER BY 
    t."Ticket_ID";


-- insert into Service
INSERT INTO "Service" ("Name") VALUES
('Internet'),
('With Bed'),
('Air Conditioner'),
('Service'),
('Entertainment Screen');

-- insert into wallet
INSERT INTO "Wallet" ("User_ID", "Balance")
SELECT 
  "User_ID",
  ROUND((10 + RANDOM() * 90)::numeric, 2) AS "Balance"
FROM "User"
WHERE "User_ID" NOT IN (SELECT "User_ID" FROM "Wallet");


-- insert into Valid Stop Type
INSERT INTO "Valid_Stop_Type" ("Transport_Mode", "Stop_Type") VALUES
('Airplane', 'Layover'),
('Bus', 'Meal'),
('Bus', 'Refuel'),
('Train', 'Transit'),
('Bus', 'Transit');

WITH Airplane_Tickets AS (
    SELECT
        t."Ticket_ID",
        t."Price",
        r."Origin",
        r."Destination",
        NTILE(3) OVER (ORDER BY t."Price") AS price_tier
    FROM "Ticket" t
    JOIN "Airplane" a ON t."Vehicle_ID" = a."Vehicle_ID"
    JOIN "Route" r ON t."Route_ID" = r."Route_ID"
    LEFT JOIN "Flight" f ON t."Ticket_ID" = f."Ticket_ID"
    WHERE f."Ticket_ID" IS NULL
),
Route_Countries AS (
    SELECT
        l."Location_ID",
        l."Country"
    FROM "Location" l
),
Classified AS (
    SELECT
        at."Ticket_ID",
        CASE
            WHEN at.price_tier = 1 THEN 'Economy_Class'::vacation_class_code
            WHEN at.price_tier = 2 THEN 'Business_Class'::vacation_class_code
            ELSE 'First_Class'::vacation_class_code
        END AS "Class_Code",
        CASE
            WHEN lo."Country" = ld."Country" THEN 'Domestic'::flight_type
            ELSE 'International'::flight_type
        END AS "Type"
    FROM Airplane_Tickets at
    JOIN Route_Countries lo ON at."Origin" = lo."Location_ID"
    JOIN Route_Countries ld ON at."Destination" = ld."Location_ID"
)

INSERT INTO "Flight" ("Ticket_ID", "Class_Code", "Type")
SELECT
    c."Ticket_ID",
    c."Class_Code",
    c."Type"
FROM Classified c;


INSERT INTO "Train_Ride" ("Ticket_ID", "Has_Private_Compartment", "Freight_Wagons_Left")
SELECT
    t."Ticket_ID",
    (random() < 0.5) AS "Has_Private_Compartment",
    (floor(random() * 11))::smallint AS "Freight_Wagons_Left"
FROM "Ticket" t
JOIN "Train" tr ON t."Vehicle_ID" = tr."Vehicle_ID"
LEFT JOIN "Train_Ride" trr ON t."Ticket_ID" = trr."Ticket_ID"
WHERE trr."Ticket_ID" IS NULL;

DO $$
DECLARE
    v_id BIGINT;
    s_id INT;
    svc_count INT;
    svc_ids INT[];
BEGIN
    SELECT array_agg("Service_ID") INTO svc_ids
    FROM "Service"
    WHERE "Name" IN ('Internet', 'With Bed', 'Air Conditioner', 'Service', 'Entertainment Screen');

    FOR v_id IN SELECT "Vehicle_ID" FROM "Vehicle" LOOP
        svc_count := FLOOR(1 + RANDOM() * 3);

        FOR i IN 1..svc_count LOOP
            s_id := svc_ids[1 + FLOOR(random() * array_length(svc_ids, 1))];

            BEGIN
                INSERT INTO "Vehicle_Service" ("Vehicle_ID", "Service_ID")
                VALUES (v_id, s_id);
            EXCEPTION WHEN unique_violation THEN
                CONTINUE;
            END;
        END LOOP;
    END LOOP;
END $$;


DO $$
DECLARE
    t RECORD;
    stop_count INT;
    stop_type RECORD;
    stop_order INT;
    stop_id INT;
    s RECORD;
    origin_loc INT;
    dest_loc INT;
BEGIN
    FOR t IN
        SELECT tk."Ticket_ID", tk."Route_ID",
               CASE
                 WHEN f."Vehicle_ID" IS NOT NULL THEN 'Airplane'
                 WHEN tr."Vehicle_ID" IS NOT NULL THEN 'Train'
                 WHEN b."Vehicle_ID" IS NOT NULL THEN 'Bus'
               END AS mode
        FROM "Ticket" tk
        LEFT JOIN "Flight" f ON tk."Vehicle_ID" = f."Vehicle_ID"
        LEFT JOIN "Train" tr ON tk."Vehicle_ID" = tr."Vehicle_ID"
        LEFT JOIN "Bus" b ON tk."Vehicle_ID" = b."Vehicle_ID"
    LOOP
        -- Get origin and destination location IDs from the route
        SELECT r."Origin_ID", r."Destination_ID"
        INTO origin_loc, dest_loc
        FROM "Route" r
        WHERE r."Route_ID" = t."Route_ID";

        -- Define the number of stops for the ticket (between 1 and 3 stops)
        stop_count := FLOOR(RANDOM() * 3 + 1);
        stop_order := 1;

        FOR stop_type IN
            SELECT "Valid_Stop_Type_ID"
            FROM "Valid_Stop_Type"
            WHERE "Transport_Mode" = t.mode
            ORDER BY RANDOM()
            LIMIT stop_count
        LOOP
            -- Get random station excluding origin and destination locations
            SELECT "Station_ID" INTO s
            FROM "Station"
            WHERE "Location_ID" NOT IN (origin_loc, dest_loc)
            ORDER BY RANDOM()
            LIMIT 1;

            -- Insert into Ticket_Stop table
            INSERT INTO "Ticket_Stop" (
                "Ticket_ID", "Station_ID", "Stop_Order", "Stop_ID"
            ) VALUES (
                t."Ticket_ID", s."Station_ID", stop_order, stop_type."Valid_Stop_Type_ID"
            );

            stop_order := stop_order + 1;
        END LOOP;
    END LOOP;
END$$;


WITH flight_tickets AS (
    SELECT tk."Ticket_ID"
    FROM "Ticket" tk
    LEFT JOIN "Flight" f ON tk."Ticket_ID" = f."Ticket_ID"
    WHERE f."Ticket_ID" IS NOT NULL
),
ticket_with_random_stops AS (
    SELECT ticket."Ticket_ID",
           FLOOR(RANDOM() * 4) AS num_stops
    FROM flight_tickets ticket
),
stop_data AS (
    SELECT DISTINCT ticket."Ticket_ID",
           station."Station_ID",
           ROW_NUMBER() OVER (PARTITION BY ticket."Ticket_ID" ORDER BY RANDOM()) AS stop_order
    FROM ticket_with_random_stops ticket
    CROSS JOIN "Station" station
),
filtered_stops AS (
    SELECT *
    FROM stop_data
    WHERE stop_order <= (SELECT num_stops FROM ticket_with_random_stops WHERE "Ticket_ID" = stop_data."Ticket_ID")
),
valid_stop_types AS (
    SELECT "Valid_Stop_Type_ID"
    FROM "Valid_Stop_Type"
    WHERE "Transport_Mode" = 'Airplane' AND "Stop_Type" = 'Layover'
)
INSERT INTO "Ticket_Stop" ("Ticket_ID", "Station_ID", "Stop_Order", "Stop_ID")
SELECT stop."Ticket_ID",
       stop."Station_ID",
       stop.stop_order,
       vst."Valid_Stop_Type_ID"
FROM filtered_stops stop
JOIN valid_stop_types vst ON TRUE
ORDER BY stop."Ticket_ID", stop.stop_order;



WITH train_tickets AS (
    SELECT tk."Ticket_ID"
    FROM "Ticket" tk
    LEFT JOIN "Train_Ride" tr ON tk."Ticket_ID" = tr."Ticket_ID"
    WHERE tr."Ticket_ID" IS NOT NULL
),
ticket_with_random_stops AS (
    SELECT ticket."Ticket_ID",
           FLOOR(RANDOM() * 4) AS num_stops  -- 0 to 3 stops
    FROM train_tickets ticket
),
stop_data AS (
    SELECT DISTINCT ticket."Ticket_ID",
           station."Station_ID",
           ROW_NUMBER() OVER (PARTITION BY ticket."Ticket_ID" ORDER BY RANDOM()) AS stop_order
    FROM ticket_with_random_stops ticket
    CROSS JOIN "Station" station
),
filtered_stops AS (
    SELECT *
    FROM stop_data
    WHERE stop_order <= (SELECT num_stops FROM ticket_with_random_stops WHERE "Ticket_ID" = stop_data."Ticket_ID")
),
valid_stop_types AS (
    SELECT "Valid_Stop_Type_ID"
    FROM "Valid_Stop_Type"
    WHERE "Transport_Mode" = 'Train' AND "Stop_Type" = 'Transit'
)
INSERT INTO "Ticket_Stop" ("Ticket_ID", "Station_ID", "Stop_Order", "Stop_ID")
SELECT stop."Ticket_ID",
       stop."Station_ID",
       stop.stop_order,
       vst."Valid_Stop_Type_ID"
FROM filtered_stops stop
JOIN valid_stop_types vst ON TRUE
ORDER BY stop."Ticket_ID", stop.stop_order;

WITH bus_tickets AS (
    SELECT tk."Ticket_ID"
    FROM "Ticket" tk
    LEFT JOIN "Bus_Ride" br ON tk."Ticket_ID" = br."Ticket_ID"
    WHERE br."Ticket_ID" IS NOT NULL
),
ticket_with_random_stops AS (
    SELECT ticket."Ticket_ID",
           FLOOR(RANDOM() * 4) AS num_stops
    FROM bus_tickets ticket
),
stop_data AS (
    SELECT DISTINCT ticket."Ticket_ID",
           station."Station_ID",
           stop_type."Stop_Type",
           ROW_NUMBER() OVER (PARTITION BY ticket."Ticket_ID" ORDER BY RANDOM()) AS stop_order
    FROM ticket_with_random_stops ticket
    CROSS JOIN "Station" station
    CROSS JOIN "Valid_Stop_Type" stop_type
    WHERE stop_type."Transport_Mode" = 'Bus'
),
filtered_stops AS (
    SELECT *
    FROM stop_data
    WHERE stop_order <= (SELECT num_stops FROM ticket_with_random_stops WHERE "Ticket_ID" = stop_data."Ticket_ID")
),
unique_station_stop_combinations AS (
    SELECT DISTINCT "Ticket_ID", "Station_ID", "Stop_Type", stop_order
    FROM filtered_stops
    ORDER BY "Ticket_ID", stop_order
)
INSERT INTO "Ticket_Stop" ("Ticket_ID", "Station_ID", "Stop_Order", "Stop_ID")
SELECT stop."Ticket_ID",
       stop."Station_ID",
       stop.stop_order,
       vst."Valid_Stop_Type_ID"
FROM unique_station_stop_combinations stop
JOIN "Valid_Stop_Type" vst
    ON vst."Transport_Mode" = 'Bus'
    AND vst."Stop_Type" = stop."Stop_Type"
ORDER BY stop."Ticket_ID", stop.stop_order;


INSERT INTO "User" ("Phone_Number", "Email", "Role", "Status", "Password_Hash")
SELECT
  '+989' || LPAD(FLOOR(RANDOM() * 1000000000)::TEXT, 9, '0') AS "Phone_Number",
  'banned_customer_' || gs::TEXT || '@example.com' AS "Email",
  'Customer'::user_role,
  'Banned'::user_status,
  md5('password' || gs::TEXT) AS "Password_Hash"
FROM generate_series(1, 10) AS gs;

INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City_ID") VALUES
(52, 'Alireza', 'Rahmati', 1),
(53, 'Saman', 'babaee', 1),
(54, 'Sarvenaz', 'Karimi', 2),
(55, 'hosein', 'Amiri', 3),
(56, 'Fatemeh', 'Asadi', 14),
(57, 'Hedie', 'Tahsom', 15),
(58, 'Shahram', 'shabpare', 16),
(59, 'Hamed', 'khare', 17),
(60, 'Niki', 'Nasimi', 18),
(61, 'Ali', 'Moradi', 19);

INSERT INTO "Wallet" ("User_ID", "Balance") VALUES
(52, 10),
(53, 0),
(54, 0),
(55, 30),
(56, 0),
(57, 14),
(58, 12.5),
(59, 0),
(60, 18.2),
(61, 45);

INSERT INTO "User" ("Phone_Number", "Email", "Role", "Password_Hash")
VALUES
('+989953658868', 'zhurst@yahoo.com', 'Admin', '2p(YQJ%G$R'),
('+989440211786', 'cartereric@gmail.com', 'Admin', '4tqAZQ+i+y'),
('+989217715343', 'rodriguezmichael@yahoo.com', 'Admin', 'w&NHiisN$0'),
('+989867434732', 'raymond57@hayes.com', 'Admin', '4^8Htp^sb)'),
('+989358103140', 'glee@hotmail.com', 'Admin', 'Mf&y5HNn62'),
('+989798452180', 'nancyjones@hotmail.com', 'Admin', 'nxuo0NUr@G'),
('+989401020191', 'jamesrobinson@gmail.com', 'Admin', 'B)N8R%Bo^x'),
('+989309786262', 'harveyrobert@cunningham.com', 'Admin', 'b$4hMezz^3'),
('+989292361221', 'justin78@turner.net', 'Admin', '8q7rJ+8v!c'),
('+989797044253', 'ccalderon@cook.com', 'Admin', '#!^7RwnV_)'),
('+989875507676', 'gomezanita@dickson-brady.com', 'Admin', '#uj2bN6adG'),
('+989743945329', 'jeffreykeller@yahoo.com', 'Admin', '^4HyCv(x1y'),
('+989438731403', 'jessica56@hotmail.com', 'Admin', '2sKQ1Mvg2('),
('+989393316329', 'snguyen@yahoo.com', 'Admin', 'bGh2UGnn3('),
('+989651820474', 'donnacampbell@hotmail.com', 'Admin', 'mhb92@Kco_'),
('+989296221379', 'dylanwatts@gmail.com', 'Admin', 'wQ$6oLFz&3'),
('+989824640650', 'juliawells@yahoo.com', 'Admin', 'Q$4Y98yR_5'),
('+989488753990', 'amy60@gmail.com', 'Admin', 'w@rYNvAs&6'),
('+989205338736', 'ryan06@caldwell-yates.com', 'Admin', '@*T#2Tr$G3'),
('+989331104161', 'currybrett@yahoo.com', 'Admin', '##1oYuN(w$'),
('+989541989806', 'tamirodriguez@hickman.biz', 'Admin', 'd3*joCsy&D'),
('+989967604102', 'tina54@webb.com', 'Admin', 'O0#Yqev2Zw'),
('+989325671709', 'rodriguezandrew@yahoo.com', 'Admin', 'gkKzx3LW9!'),
('+989758164129', 'adamsbrandy@hotmail.com', 'Admin', 'V3t#kMbCqG'),
('+989852203111', 'bthomas@yahoo.com', 'Admin', 'sN#eT4yrmZ'),
('+989655984840', 'samantha33@gmail.com', 'Admin', 'buv^2Jhz8O'),
('+989708900607', 'alexander20@hotmail.com', 'Admin', 'ZRm%3Pfq)H'),
('+989292850624', 'catherinejohnson@yahoo.com', 'Admin', 'LKq#r3^wU5'),
('+989636612020', 'kevin40@lang.com', 'Admin', 'X*t2!YqKk9'),
('+989614550979', 'ashley76@edwards.com', 'Admin', 'Wfy7pMv$3!');


INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City_ID", "Registration_Date")
VALUES
(62, 'Saeed', 'Nikbakht', 3, CURRENT_DATE),
(63, 'Parinaz', 'Ranjbar', 5, CURRENT_DATE),
(64, 'Hossein', 'Jalali', 1, CURRENT_DATE),
(65, 'Niloofar', 'Mehrabi', 8, CURRENT_DATE),
(66, 'Kian', 'Daneshvar', 4, CURRENT_DATE),
(67, 'Farideh', 'Asgari', 6, CURRENT_DATE),
(68, 'Amirhossein', 'Ghaffari', 2, CURRENT_DATE),
(69, 'Ladan', 'Rostami', 7, CURRENT_DATE),
(70, 'Babak', 'Nazari', 10, CURRENT_DATE),
(71, 'Sanaz', 'Khalili', 9, CURRENT_DATE),
(72, 'Milad', 'Shojaei', 12, CURRENT_DATE),
(73, 'Zahra', 'Rahbar', 11, CURRENT_DATE),
(74, 'Mehdi', 'Etemadi', 13, CURRENT_DATE),
(75, 'Shahrzad', 'Talebi', 14, CURRENT_DATE),
(76, 'Mahan', 'Sotoudeh', 15, CURRENT_DATE),
(77, 'Elham', 'Javadi', 16, CURRENT_DATE),
(78, 'Peyman', 'Moshiri', 17, CURRENT_DATE),
(79, 'Leila', 'Barzegar', 18, CURRENT_DATE),
(80, 'Kourosh', 'Ebadi', 19, CURRENT_DATE),
(81, 'Nasim', 'Kamali', 20, CURRENT_DATE),
(82, 'Reza', 'Kiani', 1, CURRENT_DATE),
(83, 'Sara', 'Vahidi', 3, CURRENT_DATE),
(84, 'Alireza', 'Farhadi', 4, CURRENT_DATE),
(85, 'Yasmin', 'Ramezani', 6, CURRENT_DATE),
(86, 'Hamid', 'Keshavarz', 7, CURRENT_DATE),
(87, 'Mahshid', 'Afshar', 8, CURRENT_DATE),
(88, 'Behnam', 'Rahimi', 2, CURRENT_DATE),
(89, 'Sepideh', 'Fazel', 5, CURRENT_DATE),
(90, 'Omid', 'Soleimani', 9, CURRENT_DATE),
(91, 'Roya', 'Mousavi', 10, CURRENT_DATE);


CREATE OR REPLACE FUNCTION insert_random_reservations(n INTEGER)
RETURNS VOID AS $$
DECLARE
  i             INTEGER := 0;
  v_user_id     BIGINT;
  v_passenger_id BIGINT;
  v_ticket_id   BIGINT;
  v_seat        VARCHAR(10);
  v_status      reservation_status;
  v_rand_ts     TIMESTAMP;
  v_res_date    DATE;
  v_res_time    TIME;
BEGIN
  FOR i IN 1..n LOOP
    -- 1) pick a random active customer
    SELECT "User_ID"
      INTO v_user_id
    FROM "User"
    WHERE "Status" = 'Active'
      AND "Role" = 'Customer'
    ORDER BY RANDOM()
    LIMIT 1;

    -- 2) pick a random passenger
    SELECT "Passenger_ID"
      INTO v_passenger_id
    FROM "Passenger"
    ORDER BY RANDOM()
    LIMIT 1;

    -- 3) pick a random ticket
    SELECT "Ticket_ID"
      INTO v_ticket_id
    FROM "Ticket"
    ORDER BY RANDOM()
    LIMIT 1;

    -- 4) generate a unique seat for that ticket
    LOOP
      v_seat :=
        LPAD((FLOOR(RANDOM() * 30) + 1)::TEXT, 2, '0')
        || CHR((65 + FLOOR(RANDOM() * 26))::INT);
      EXIT WHEN NOT EXISTS(
        SELECT 1 FROM "Reservation"
        WHERE "Ticket_ID" = v_ticket_id
          AND "Seat_Number" = v_seat
      );
    END LOOP;

    -- 5) random status
    v_status := (
      ARRAY['Pending','Confirmed','Cancelled']::reservation_status[]
    )[FLOOR(RANDOM() * 3 + 1)];

    -- 6) random timestamp within past year
    v_rand_ts := NOW()
      - ((FLOOR(RANDOM() * 365))::INT || ' days')::INTERVAL
      - ((FLOOR(RANDOM() * 86400))::INT || ' seconds')::INTERVAL;
    v_res_date := v_rand_ts::DATE;
    v_res_time := v_rand_ts::TIME;

    -- 7) insert
    INSERT INTO "Reservation" (
      "User_ID", "Passenger_ID", "Ticket_ID", "Seat_Number",
      "Status", "Reservation_Date", "Reservation_Time", "Expiration"
    ) VALUES (
      v_user_id, v_passenger_id, v_ticket_id, v_seat,
      v_status, v_res_date, v_res_time, INTERVAL '1 day'
    );
  END LOOP;
END;
$$ LANGUAGE plpgsql;


SELECT insert_random_reservations(1000);

UPDATE "Reservation"
SET "Status" = 'Cancelled'
WHERE "Status" = 'Pending'
  AND CURRENT_TIMESTAMP > ("Reservation_Date" + "Expiration")
  AND "Status" != 'Cancelled';


SELECT * FROM "Reservation" WHERE "Status" = 'Confirmed';


WITH confirmed_reservations AS (
    SELECT r."Reservation_ID", r."User_ID", r."Ticket_ID", t."Price", r."Reservation_Date", r."Reservation_Time"
    FROM "Reservation" r
    JOIN "Ticket" t ON r."Ticket_ID" = t."Ticket_ID"
    WHERE r."Status" = 'Confirmed'
)
INSERT INTO "Payment" ("User_ID", "Reservation_ID", "Amount", "Payment_Method", "Status", "Payment_Time", "Payment_Date")
SELECT
    r."User_ID",
    r."Reservation_ID",
    r."Price" AS "Amount",
    (ARRAY['Credit Card', 'PayPal', 'Bank Transfer', 'Cash', 'Wallet'])[FLOOR(RANDOM() * 5) + 1]::payment_method AS "Payment_Method",
    'Completed' AS "Status",
    r."Reservation_Time" AS "Payment_Time",
    r."Reservation_Date" AS "Payment_Date"
FROM confirmed_reservations r;


WITH pending_reservations AS (
    SELECT r."Reservation_ID", r."User_ID", r."Ticket_ID", t."Price", r."Reservation_Date", r."Reservation_Time"
    FROM "Reservation" r
    JOIN "Ticket" t ON r."Ticket_ID" = t."Ticket_ID"
    WHERE r."Status" = 'Pending'
    LIMIT 5
)
INSERT INTO "Payment" ("User_ID", "Reservation_ID", "Amount", "Payment_Method", "Status", "Payment_Time", "Payment_Date")
SELECT
    r."User_ID",
    r."Reservation_ID",
    r."Price" AS "Amount",
    (ARRAY['Credit Card', 'PayPal', 'Bank Transfer', 'Cash', 'Wallet'])[FLOOR(RANDOM() * 5) + 1]::payment_method AS "Payment_Method",
    'Pending' AS "Status",
    r."Reservation_Time" AS "Payment_Time",
    r."Reservation_Date" AS "Payment_Date"
FROM pending_reservations r;


WITH wallet_payments AS (
    SELECT p."Payment_ID", p."User_ID", p."Amount", p."Payment_Time", p."Payment_Date"
    FROM "Payment" p
    WHERE p."Payment_Method" = 'Wallet'
)
INSERT INTO "Wallet_Transactions" ("Wallet_ID", "Related_Payment_ID", "Amount", "Type", "Transaction_Time", "Transaction_Date")
SELECT
    w."Wallet_ID",
    p."Payment_ID" AS "Related_Payment_ID",
    p."Amount",
    'Payment' AS "Type",
    p."Payment_Time",
    p."Payment_Date"
FROM wallet_payments p
JOIN "Wallet" w ON w."User_ID" = p."User_ID";


WITH random_wallets AS (
    SELECT w."Wallet_ID", w."User_ID"
    FROM "Wallet" w
    ORDER BY RANDOM()
    LIMIT 100
)
INSERT INTO "Wallet_Transactions" ("Wallet_ID", "Related_Payment_ID", "Amount", "Type", "Transaction_Date", "Transaction_Time")
SELECT
    rw."Wallet_ID",
    NULL AS "Related_Payment_ID",
    ROUND((RANDOM() * 100 + 1)::numeric, 2) AS "Amount",  -- Explicitly casting RANDOM() to numeric
    'Charge' AS "Type",
    CURRENT_DATE - (FLOOR(RANDOM() * 30) + 1) * INTERVAL '1 day' AS "Transaction_Date",  -- Fix: casting to INTERVAL
    CURRENT_TIME - INTERVAL '1 hour' * FLOOR(RANDOM() * 24) AS "Transaction_Time"  -- Random time in the past 24 hours
FROM random_wallets rw;

