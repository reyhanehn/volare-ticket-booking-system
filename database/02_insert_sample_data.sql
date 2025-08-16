-- reset sequences
DO $$
DECLARE
    seq_name text;
BEGIN
    FOR seq_name IN
        SELECT sequence_name
        FROM information_schema.sequences
        WHERE sequence_schema = 'public'
    LOOP
        EXECUTE 'ALTER SEQUENCE "' || seq_name || '"RESTART WITH 1';
    END LOOP;
END $$;

-- insert into location table
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

-- insert into user table
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

-- Insert vehicles into vehicle table
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

-- insert into airplane's table
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

-- insert into bus table
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

-- insert into  train's table
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

-- insert into the ticket table
WITH TicketData AS (
    INSERT INTO "Ticket" ("Vehicle_ID", "Route_ID", "Price", "Remaining_Capacity")
    SELECT
        CASE 
            WHEN s1."Type" = 'Airport' OR s2."Type" = 'Airport' THEN
                (SELECT "Vehicle_ID" FROM "Airplane" ORDER BY RANDOM() LIMIT 1)
            WHEN s1."Type" = 'Train_Station' OR s2."Type" = 'Train_Station' THEN
                (SELECT "Vehicle_ID" FROM "Train" ORDER BY RANDOM() LIMIT 1)
            WHEN s1."Type" = 'Bus_Station' OR s2."Type" = 'Bus_Station' THEN
                (SELECT "Vehicle_ID" FROM "Bus" ORDER BY RANDOM() LIMIT 1)
        END AS "Vehicle_ID",
        
        r."Route_ID",
        ROUND((RANDOM() * (500 - 50) + 50)::numeric, 2) AS "Price",
        FLOOR(RANDOM() * (100 - 10) + 10) AS "Remaining_Capacity"
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

-- insert into service
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


-- insert into valid stop type
INSERT INTO "Valid_Stop_Type" ("Transport_Mode", "Stop_Type") VALUES
('Airplane', 'Layover'),
('Bus', 'Meal'),
('Bus', 'Refuel'),
('Train', 'Transit'),
('Bus', 'Transit');

-- insert into flight
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

-- insert into train ride
INSERT INTO "Train_Ride" ("Ticket_ID", "Has_Private_Compartment", "Freight_Wagons_Left")
SELECT
    t."Ticket_ID",
    (random() < 0.5) AS "Has_Private_Compartment",
    (floor(random() * 11))::smallint AS "Freight_Wagons_Left"
FROM "Ticket" t
JOIN "Train" tr ON t."Vehicle_ID" = tr."Vehicle_ID"
LEFT JOIN "Train_Ride" trr ON t."Ticket_ID" = trr."Ticket_ID"
WHERE trr."Ticket_ID" IS NULL;

-- insert into bus_ride
INSERT INTO "Bus_Ride" ("Ticket_ID")
SELECT t."Ticket_ID"
FROM "Ticket" t
JOIN "Bus" b ON t."Vehicle_ID" = b."Vehicle_ID"
LEFT JOIN "Bus_Ride" br ON t."Ticket_ID" = br."Ticket_ID"
WHERE br."Ticket_ID" IS NULL;

-- insert into vehicle_service
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

--insert into ticket stop

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
           FLOOR(RANDOM() * 4) AS num_stops  
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

--insert into user (banned customer)
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
    SELECT "User_ID"
      INTO v_user_id
    FROM "User"
    WHERE "Status" = 'Active'
      AND "Role" = 'Customer'
    ORDER BY RANDOM()
    LIMIT 1;

    SELECT "Passenger_ID"
      INTO v_passenger_id
    FROM "Passenger"
    ORDER BY RANDOM()
    LIMIT 1;

    SELECT "Ticket_ID"
      INTO v_ticket_id
    FROM "Ticket"
    ORDER BY RANDOM()
    LIMIT 1;

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

    v_status := (
      ARRAY['Pending','Confirmed','Cancelled']::reservation_status[]
    )[FLOOR(RANDOM() * 3 + 1)];

    v_rand_ts := NOW()
      - ((FLOOR(RANDOM() * 365))::INT || ' days')::INTERVAL
      - ((FLOOR(RANDOM() * 86400))::INT || ' seconds')::INTERVAL;
    v_res_date := v_rand_ts::DATE;
    v_res_time := v_rand_ts::TIME;

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

-- update expired reservations
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

-- insert pending payments
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

-- insert wallet transactions
-- payment
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
    ROUND((RANDOM() * 100 + 1)::numeric, 2) AS "Amount",
    'Charge' AS "Type",
    CURRENT_DATE - (FLOOR(RANDOM() * 30) + 1) * INTERVAL '1 day' AS "Transaction_Date",
    CURRENT_TIME - INTERVAL '1 hour' * FLOOR(RANDOM() * 24) AS "Transaction_Time"
FROM random_wallets rw;

-- update charged wallets
UPDATE "Wallet" w
SET "Balance" = "Balance" + sub.total_charge
FROM (
    SELECT "Wallet_ID", SUM("Amount") AS total_charge
    FROM "Wallet_Transactions"
    WHERE "Type" = 'Charge'
    GROUP BY "Wallet_ID"
) sub
WHERE w."Wallet_ID" = sub."Wallet_ID";

-- insert payments for cancelled reservations for cancellation
INSERT INTO "Payment" (
    "User_ID",
    "Reservation_ID",
    "Amount",
    "Payment_Method",
    "Status",
    "Payment_Time",
    "Payment_Date"
)
SELECT
    r."User_ID",
    r."Reservation_ID",
    t."Price" AS "Amount",
    (ARRAY['Credit Card','PayPal','Bank Transfer','Cash', 'Wallet'])[FLOOR(RANDOM() * 5 + 1)]::payment_method,
    'Completed'::payment_status,
    r."Reservation_Time",
    r."Reservation_Date"
FROM (
    SELECT *
    FROM "Reservation"
    WHERE "Status" = 'Cancelled'
      AND "Reservation_ID" NOT IN (SELECT "Reservation_ID" FROM "Payment")
    ORDER BY RANDOM()
    LIMIT 100
) r
JOIN "Ticket" t ON r."Ticket_ID" = t."Ticket_ID";

-- insert refunds for cancellations
INSERT INTO "Wallet_Transactions" (
    "Wallet_ID",
    "Related_Payment_ID",
    "Amount",
    "Type",
    "Transaction_Date",
    "Transaction_Time"
)
SELECT
    w."Wallet_ID",
    p."Payment_ID",
    p."Amount",
    'Refund'::transaction_type,
    p."Payment_Date" + (FLOOR(RANDOM() * 3 + 1)) * INTERVAL '1 day',
    (p."Payment_Time" + (INTERVAL '1 hour' * FLOOR(RANDOM() * 24)))::time
FROM "Payment" p
JOIN "Reservation" r ON p."Reservation_ID" = r."Reservation_ID"
JOIN "Wallet" w ON p."User_ID" = w."User_ID"
WHERE r."Status" = 'Cancelled'
  AND p."Payment_ID" NOT IN (
    SELECT "Related_Payment_ID" FROM "Wallet_Transactions"
    WHERE "Type" = 'Refund'
  );

-- insert_cancellation
CREATE OR REPLACE PROCEDURE insert_cancellations()
LANGUAGE plpgsql
AS $$
DECLARE
    rec RECORD;
    admin_id BIGINT;
BEGIN
    FOR rec IN
        SELECT r."Reservation_ID", wt."Transaction_ID", wt."Transaction_Date", wt."Transaction_Time", wt."Amount"
        FROM "Reservation" r
        JOIN "Payment" p ON r."Reservation_ID" = p."Reservation_ID"
        JOIN "Wallet_Transactions" wt ON p."Payment_ID" = wt."Related_Payment_ID"
        WHERE r."Status" = 'Cancelled'
          AND wt."Type" = 'Refund'
          AND NOT EXISTS (
              SELECT 1 FROM "Cancellation" c WHERE c."Reservation_ID" = r."Reservation_ID"
          )
    LOOP
        SELECT "User_ID"
        INTO admin_id
        FROM "User"
        WHERE "Role" = 'Admin'
        ORDER BY RANDOM()
        LIMIT 1;

        INSERT INTO "Cancellation" (
            "Reservation_ID",
            "Admin_ID",
            "Transaction_ID",
            "Cancel_Date",
            "Cancel_Time",
            "Refund_Amount"
        ) VALUES (
            rec."Reservation_ID",
            admin_id,
            rec."Transaction_ID",
            rec."Transaction_Date" - INTERVAL '0 day',
            rec."Transaction_Time" - INTERVAL '1 hour',
            rec."Amount"
        );
    END LOOP;
END;
$$;


CALL insert_cancellations();


-- insert into reports

-- reservation
DO $$
DECLARE
  report_id BIGINT;
  reservation_rec RECORD;
BEGIN
  FOR reservation_rec IN
    SELECT r."Reservation_ID", r."User_ID", c."Admin_ID"
    FROM "Cancellation" c
    JOIN "Reservation" r ON r."Reservation_ID" = c."Reservation_ID"
  LOOP

    INSERT INTO "Report" ("User_ID", "Admin_ID", "Status", "Text", "Answer", "Type")
    VALUES (
      reservation_rec."User_ID",
      reservation_rec."Admin_ID",
      'Checked',
      'Please end this',
      'For sure',
	  'reservation'
    )
    RETURNING "Report_ID" INTO report_id;

    INSERT INTO "Report_Reservation" ("Report_ID", "Reservation_ID")
    VALUES (report_id, reservation_rec."Reservation_ID");
  END LOOP;
END $$;

--insert into report(payment and ticket)
WITH report_data AS (
  SELECT
    gs AS idx,
    -- Random customer for User_ID
    (SELECT "User_ID" FROM "User" WHERE "Role" = 'Customer' ORDER BY random() LIMIT 1) AS "User_ID",
    -- Admin_ID is only set for checked reports
    CASE 
      WHEN gs <= 50 THEN NULL
      ELSE (SELECT "User_ID" FROM "User" WHERE "Role" = 'Admin' ORDER BY random() LIMIT 1)
    END AS "Admin_ID",
    CASE 
      WHEN gs <= 50 THEN 'Pending'
      ELSE 'Checked'
    END::report_status AS "Status",
    'This is report #' || gs AS "Text",
    -- Answer is NULL for pending, filled for checked
    CASE 
      WHEN gs <= 50 THEN NULL
      ELSE 'Answer for report #' || gs
    END AS "Answer",
    -- Alternate evenly between 'payment' and 'ticket'
    CASE 
      WHEN gs % 2 = 0 THEN 'payment'
      ELSE 'ticket'
    END::report_type AS "Type"
  FROM generate_series(1, 100) gs
)
INSERT INTO "Report" ("User_ID", "Admin_ID", "Status", "Text", "Answer", "Type")
SELECT "User_ID", "Admin_ID", "Status", "Text", "Answer", "Type"
FROM report_data;

-- Insert into Report_Payment table for reports of type 'payment'
INSERT INTO "Report_Payment" ("Report_ID", "Payment_ID")
SELECT r."Report_ID", 
       (SELECT "Payment_ID" FROM "Payment" ORDER BY random() LIMIT 1)
FROM "Report" r
WHERE r."Type" = 'payment' AND r."Report_ID" NOT IN (SELECT "Report_ID" FROM "Report_Payment");


-- Insert into Report_Ticket table for reports of type 'ticket'
INSERT INTO "Report_Ticket" ("Report_ID", "Ticket_ID")
SELECT r."Report_ID", 
       (SELECT "Ticket_ID" FROM "Ticket" ORDER BY random() LIMIT 1)
FROM "Report" r
WHERE r."Type" = 'ticket' AND r."Report_ID" NOT IN (SELECT "Report_ID" FROM "Report_Ticket");





------------------------------------------


WITH bus_tickets AS (
    SELECT tk."Ticket_ID"
    FROM "Ticket" tk
    JOIN "Bus_Ride" br ON tk."Ticket_ID" = br."Ticket_ID"
),
ticket_with_random_stops AS (
    SELECT ticket."Ticket_ID",
           FLOOR(RANDOM() * 4) + 1 AS num_stops
    FROM bus_tickets ticket
),
random_stations AS (
    SELECT
        t."Ticket_ID",
        s."Station_ID",
        ROW_NUMBER() OVER (PARTITION BY t."Ticket_ID" ORDER BY RANDOM()) AS rn
    FROM ticket_with_random_stops t
    JOIN "Station" s ON TRUE
),
filtered_stops AS (
    SELECT
        rs."Ticket_ID",
        rs."Station_ID",
        rs.rn AS stop_order
    FROM random_stations rs
    JOIN ticket_with_random_stops twrs
        ON rs."Ticket_ID" = twrs."Ticket_ID"
    WHERE rs.rn <= twrs.num_stops
),
valid_stop_types AS (
    SELECT "Valid_Stop_Type_ID"
    FROM "Valid_Stop_Type"
    WHERE "Transport_Mode" = 'Bus' AND "Stop_Type" = 'Rest'
)
INSERT INTO "Ticket_Stop" ("Ticket_ID", "Station_ID", "Stop_Order", "Stop_ID")
SELECT fs."Ticket_ID",
       fs."Station_ID",
       fs.stop_order,
       vst."Valid_Stop_Type_ID"
FROM filtered_stops fs
JOIN valid_stop_types vst ON TRUE
ORDER BY fs."Ticket_ID", fs.stop_order;


WITH train_tickets AS (
    SELECT tk."Ticket_ID"
    FROM "Ticket" tk
    JOIN "Train_Ride" tr ON tk."Ticket_ID" = tr."Ticket_ID"
),
ticket_with_random_stops AS (
    SELECT ticket."Ticket_ID",
           FLOOR(RANDOM() * 4) + 1 AS num_stops
    FROM train_tickets ticket
),
random_stations AS (
    SELECT
        t."Ticket_ID",
        s."Station_ID",
        ROW_NUMBER() OVER (PARTITION BY t."Ticket_ID" ORDER BY RANDOM()) AS rn
    FROM ticket_with_random_stops t
    JOIN "Station" s ON TRUE
),
filtered_stops AS (
    SELECT
        rs."Ticket_ID",
        rs."Station_ID",
        rs.rn AS stop_order
    FROM random_stations rs
    JOIN ticket_with_random_stops twrs
        ON rs."Ticket_ID" = twrs."Ticket_ID"
    WHERE rs.rn <= twrs.num_stops
),
valid_stop_types AS (
    SELECT "Valid_Stop_Type_ID"
    FROM "Valid_Stop_Type"
    WHERE "Transport_Mode" = 'Train' AND "Stop_Type" = 'Transit'
)
INSERT INTO "Ticket_Stop" ("Ticket_ID", "Station_ID", "Stop_Order", "Stop_ID")
SELECT fs."Ticket_ID",
       fs."Station_ID",
       fs.stop_order,
       vst."Valid_Stop_Type_ID"
FROM filtered_stops fs
JOIN valid_stop_types vst ON TRUE
ORDER BY fs."Ticket_ID", fs.stop_order;


-- insert 20 users so that they have no reservations
WITH inserted_users AS (
  INSERT INTO "User" ("Phone_Number", "Role", "Password_Hash")
  VALUES
    ('+989900000001', 'Customer', 'hashed1'),
    ('+989900000002', 'Customer', 'hashed2'),
    ('+989900000003', 'Customer', 'hashed3'),
    ('+989900000004', 'Customer', 'hashed4'),
    ('+989900000005', 'Customer', 'hashed5'),
    ('+989900000006', 'Customer', 'hashed6'),
    ('+989900000007', 'Customer', 'hashed7'),
    ('+989900000008', 'Customer', 'hashed8'),
    ('+989900000009', 'Customer', 'hashed9'),
    ('+989900000010', 'Customer', 'hashed10')
  RETURNING "User_ID"
),
numbered_users AS (
  SELECT "User_ID", ROW_NUMBER() OVER () AS rn FROM inserted_users
),
profile_data AS (
  SELECT * FROM (
    VALUES
      ('Ali', 'Azimi', 1),
      ('Narges', 'Moradi', 2),
      ('Reza', 'Shahbazi', 3),
      ('Ladan', 'Jalali', 4),
      ('Javad', 'Kazemi', 5),
      ('Sahar', 'Zare', 6),
      ('Kian', 'Farhadi', 7),
      ('Mina', 'Esmaili', 8),
      ('Arman', 'Hosseini', 9),
      ('Taraneh', 'Ghaffari', 10)
  ) AS p("Name", "Lastname", "City_ID")
),
numbered_profiles AS (
  SELECT *, ROW_NUMBER() OVER () AS rn FROM profile_data
)
INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City_ID")
SELECT u."User_ID", p."Name", p."Lastname", p."City_ID"
FROM numbered_users u
JOIN numbered_profiles p ON u.rn = p.rn;

WITH inserted_users AS (
  INSERT INTO "User" ("Email", "Role", "Password_Hash")
  VALUES
    ('alina.azari@mail.com', 'Customer', 'hashed11'),
    ('majid.taheri@mail.com', 'Customer', 'hashed12'),
    ('roya.khalili@mail.com', 'Customer', 'hashed13'),
    ('behnam.karimi@mail.com', 'Customer', 'hashed14'),
    ('elham.rashidi@mail.com', 'Customer', 'hashed15'),
    ('arman.jafari@mail.com', 'Customer', 'hashed16'),
    ('shiva.moradi@mail.com', 'Customer', 'hashed17'),
    ('masoud.golzar@mail.com', 'Customer', 'hashed18'),
    ('zahra.akbari@mail.com', 'Customer', 'hashed19'),
    ('omid.shahbaz@mail.com', 'Customer', 'hashed20')
  RETURNING "User_ID"
),
numbered_users AS (
  SELECT "User_ID", ROW_NUMBER() OVER () AS rn FROM inserted_users
),
profile_data AS (
  SELECT * FROM (
    VALUES
      ('Alina', 'Azari', 11),
      ('Majid', 'Taheri', 12),
      ('Roya', 'Khalili', 13),
      ('Behnam', 'Karimi', 14),
      ('Elham', 'Rashidi', 15),
      ('Arman', 'Jafari', 16),
      ('Shiva', 'Moradi', 17),
      ('Masoud', 'Golzar', 18),
      ('Zahra', 'Akbari', 19),
      ('Omid', 'Shahbaz', 20)
  ) AS p("Name", "Lastname", "City_ID")
),
numbered_profiles AS (
  SELECT *, ROW_NUMBER() OVER () AS rn FROM profile_data
)
INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City_ID")
SELECT u."User_ID", p."Name", p."Lastname", p."City_ID"
FROM numbered_users u
JOIN numbered_profiles p ON u.rn = p.rn;

-- insert reservation from the same origin for users
CREATE OR REPLACE PROCEDURE insert_reservations_and_payments()
LANGUAGE plpgsql
AS
$$
DECLARE
    rec RECORD;
    new_ticket_id BIGINT;
    new_seat VARCHAR(10);
    new_reservation_id BIGINT;
    ticket_price DECIMAL(10,2);
    original_datetime TIMESTAMP;
    new_datetime TIMESTAMP;
BEGIN
    FOR rec IN
        SELECT DISTINCT r."User_ID", r."Passenger_ID", t."Ticket_ID"
        FROM "Reservation" r
        JOIN "Ticket" t ON r."Ticket_ID" = t."Ticket_ID"
        WHERE r."Status" = 'Confirmed'
    LOOP
        SELECT t2."Ticket_ID" INTO new_ticket_id
        FROM "Ticket" t1
        JOIN "Route" r1 ON r1."Route_ID" = t1."Route_ID"
        JOIN "Ticket" t2 ON t2."Route_ID" = r1."Route_ID"
        WHERE t1."Ticket_ID" = rec."Ticket_ID"
          AND r1."Origin" = (SELECT "Origin" FROM "Route" WHERE "Route_ID" = t1."Route_ID")
        LIMIT 1;

        LOOP
            new_seat := CONCAT(FLOOR(RANDOM() * 30 + 1), CHR(65 + FLOOR(RANDOM() * 26)::INT));
            EXIT WHEN NOT EXISTS (
                SELECT 1
                FROM "Reservation"
                WHERE "Ticket_ID" = new_ticket_id
                  AND "Seat_Number" = new_seat
            );  -- Continue loop until a unique seat number is found
        END LOOP;

        SELECT make_timestamp(
                   EXTRACT(YEAR FROM r."Reservation_Date")::INT,
                   EXTRACT(MONTH FROM r."Reservation_Date")::INT,
                   EXTRACT(DAY FROM r."Reservation_Date")::INT,
                   EXTRACT(HOUR FROM r."Reservation_Time")::INT,
                   EXTRACT(MINUTE FROM r."Reservation_Time")::INT,
                   EXTRACT(SECOND FROM r."Reservation_Time")::INT
               ) + INTERVAL '5 hours'
        INTO new_datetime
        FROM "Reservation" r
        WHERE r."User_ID" = rec."User_ID"
          AND r."Ticket_ID" = rec."Ticket_ID"
        LIMIT 1;

        INSERT INTO "Reservation" (
            "User_ID", "Passenger_ID", "Ticket_ID", "Seat_Number",
            "Status", "Reservation_Date", "Reservation_Time", "Expiration"
        )
        VALUES (
            rec."User_ID", rec."Passenger_ID", new_ticket_id, new_seat,
            'Confirmed',
            new_datetime::DATE,
            new_datetime::TIME,
            INTERVAL '1 day'
        )
        RETURNING "Reservation_ID" INTO new_reservation_id;

        SELECT "Price" INTO ticket_price
        FROM "Ticket"
        WHERE "Ticket_ID" = new_ticket_id;

        INSERT INTO "Payment" (
            "User_ID", "Reservation_ID", "Amount", "Payment_Method", "Status", "Payment_Time", "Payment_Date"
        )
        VALUES (
            rec."User_ID", new_reservation_id, ticket_price,
            (ARRAY['Credit Card', 'PayPal', 'Bank Transfer', 'Cash', 'Wallet'])[FLOOR(RANDOM() * 5) + 1]::payment_method,
            'Completed', NOW(), CURRENT_DATE
        );
    END LOOP;
END;
$$;

CALL insert_reservations_and_payments();

-- since now no user exists who have bought only 1 ticket per city we delete some of the reservations
DELETE FROM "Reservation"
WHERE "Reservation_ID" IN (
    SELECT "Reservation_ID"
    FROM "Reservation"
    ORDER BY "Reservation_ID" DESC
    LIMIT 56
);

SELECT * FROM "User" ORDER BY "User_ID" DESC;

SELECT * FROM "Reservation" R WHERE R."Ticket_ID" = 1;

INSERT INTO "Reservation" ("User_ID", "Passenger_ID", "Ticket_ID", "Seat_Number", "Status", "Reservation_Date", "Reservation_Time", "Expiration") VALUES
  (98, 1, 1, '01A', 'Confirmed', CURRENT_DATE, CURRENT_TIME, INTERVAL'1 day'),
  (99, 1, 1, '02A', 'Confirmed', CURRENT_DATE, CURRENT_TIME, INTERVAL'1 day'),
  (100, 1, 1, '03A', 'Confirmed', CURRENT_DATE, CURRENT_TIME, INTERVAL'1 day');

SELECT * FROM "Reservation" R JOIN "Ticket" T ON T."Ticket_ID" = R."Ticket_ID" WHERE R."User_ID" = 99;

INSERT INTO "Payment" (
    "User_ID", "Reservation_ID", "Amount", "Payment_Method", "Status"
  )
  VALUES
  (98, 2469, 237.80, 'Cash', 'Completed'),
  (99, 2470, 237.80, 'Cash', 'Completed'),
  (100, 2471, 237.80, 'Cash', 'Completed');