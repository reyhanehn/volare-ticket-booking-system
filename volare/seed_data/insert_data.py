import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Initialize Faker and Database connection
fake = Faker()

# Establish the connection to the database
connection = psycopg2.connect(
    dbname="Volare_DB",
    user="postgres",
    password="h.tah1584",
    host="localhost",
    port="5432"
)

cursor = connection.cursor()

def generate_random_date(start_date, end_date):
    """ Generate a random date between start_date and end_date """
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )

def insert_fake_data():
    # Example to insert fake data into your 'User' table
    # with connection.cursor() as cursor:
    #     cursor.execute("""
    #                        INSERT INTO "Location" ("Country", "City")
    #                        VALUES (%s, %s) ON CONFLICT DO NOTHING
    #                        RETURNING "Location_ID";
    #                    """, ["Iran", "Saveh"])
    #     loc_id = cursor.fetchone()[0]
    #     print(loc_id)
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    random_registration_date = generate_random_date(start_date, end_date).date()
    print(random_registration_date)

def insert_to_location():
    # List of 50 Iranian cities
    iran_cities = [
        "Tehran", "Mashhad", "Isfahan", "Shiraz", "Tabriz",
        "Ahvaz", "Kermanshah", "Karaj", "Yazd", "Qom",
        "Kerman", "Rasht", "Zanjan", "Arak", "Hamedan",
        "Sanandaj", "Urmia", "Sari", "Khorramabad", "Qazvin",
        "Gorgan", "Kashan", "Semnan", "Shahrekord", "Band e Amir",
        "Kangavar", "Ghaemshahr", "Bojnourd", "Kerman", "Sirjan",
        "Gilan", "Birjand", "Babol", "Alborz", "Shiraz",
        "Hamedan", "Meybod", "Roudbar", "Jiroft", "Sanandaj",
        "Ahvaz", "Esfahan", "Kermanshah", "Bojnourd", "Fasa",
        "Shushtar", "Kamalshahr", "Khalkhal", "Ramhormoz"
    ]

    # List of 50 famous cities from around the world
    world_cities = [
        ("USA", "New York"), ("USA", "Los Angeles"), ("USA", "Chicago"),
        ("UK", "London"), ("UK", "Manchester"), ("France", "Paris"),
        ("Germany", "Berlin"), ("Germany", "Hamburg"), ("Italy", "Rome"),
        ("Spain", "Barcelona"), ("Spain", "Madrid"), ("Australia", "Sydney"),
        ("Australia", "Melbourne"), ("Brazil", "Rio de Janeiro"),
        ("Brazil", "Sao Paulo"), ("Mexico", "Mexico City"), ("India", "Mumbai"),
        ("India", "Bangalore"), ("Japan", "Tokyo"), ("Japan", "Osaka"),
        ("China", "Beijing"), ("China", "Shanghai"), ("South Korea", "Seoul"),
        ("Canada", "Toronto"), ("Canada", "Vancouver"), ("Russia", "Moscow"),
        ("South Africa", "Cape Town"), ("Egypt", "Cairo"), ("Turkey", "Istanbul"),
        ("Greece", "Athens"), ("Sweden", "Stockholm"), ("Finland", "Helsinki"),
        ("Norway", "Oslo"), ("Denmark", "Copenhagen"), ("Switzerland", "Zurich"),
        ("Austria", "Vienna"), ("Belgium", "Brussels"), ("Netherlands", "Amsterdam"),
        ("Portugal", "Lisbon"), ("Sweden", "Gothenburg"), ("Denmark", "Aarhus"),
        ("Norway", "Bergen"), ("Italy", "Milan"), ("France", "Lyon"),
        ("Belgium", "Antwerp"), ("Poland", "Warsaw"), ("Poland", "Krakow"),
        ("Romania", "Bucharest"), ("Hungary", "Budapest"), ("Ukraine", "Kyiv"),
        ("Argentina", "Buenos Aires"), ("Chile", "Santiago"), ("Peru", "Lima"),
        ("Colombia", "Bogota"), ("Venezuela", "Caracas")
    ]

    # Insert Iranian cities into the Location table
    with connection.cursor() as cursor:
        for city in iran_cities:
            cursor.execute("""
                           INSERT INTO "Location" ("Country", "City")
                           VALUES (%s, %s) ON CONFLICT DO NOTHING;
                           """, ["Iran", city])

        # Insert world cities into the Location table
        for country, city in world_cities:
            cursor.execute("""
                           INSERT INTO "Location" ("Country", "City")
                           VALUES (%s, %s) ON CONFLICT DO NOTHING;
                           """, [country, city])


def insert_user():

    with connection.cursor() as cursor:
        for _ in range(1000):
            option = random.choice([1, 2, 3])
            if option == 1:
                email = fake.email()
                phone_number = None
            elif option == 2:
                phone_number = fake.phone_number()
                email = None
            else:
                email = fake.email()
                phone_number =  fake.phone_number()
            password_hash =  fake.password()
            user_query = """
                    INSERT INTO "User" ("Phone_Number", "Email", "Role", "Status", "Password_Hash")
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING "User_ID";
                """
            cursor.execute(user_query, (phone_number, email, "Customer", "Active", password_hash))
            user_id = cursor.fetchone()[0]

            cursor.execute("""
                SELECT "Location_ID"
                FROM "Location"
                ORDER BY RANDOM()
                LIMIT 1;
            """)
            location_id = cursor.fetchone()[0]
            start_date = datetime.now() - timedelta(days=365)
            end_date = datetime.now()
            random_registration_date = "Date '" + str(generate_random_date(start_date, end_date).date())+ "'"
            profile_query = """
                INSERT INTO "Profile" ("User_ID", "Name", "Lastname", "City_ID", "Registration_Date")
                VALUES (%s, %s, %s, %s, %s);
            """
            name =fake.first_name()
            lastname = fake.last_name()
            cursor.execute(profile_query, (user_id, name, lastname, location_id, random_registration_date))

            wallet_query = """
                    INSERT INTO "Wallet" ("User_ID", "Balance")
                    VALUES (%s, %s);
                """
            balance = random.uniform(0, 1000)  # Random balance between 0 and 1000
            cursor.execute(wallet_query, (user_id, round(balance, 2)))


if __name__ == "__main__":
    insert_user()
    # connection.commit()
    print("Fake data inserted successfully!")
