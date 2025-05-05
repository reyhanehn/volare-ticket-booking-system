import os
import django
from faker import Faker
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "volare.settings")
django.setup()

fake = Faker()

def insert_fake_data():
    # Example to insert fake data into your 'User' table
    with connection.cursor() as cursor:
        for _ in range(10):  # Inserting 10 fake users as an example
            name = fake.name()
            email = fake.email()
            phone_number = fake.phone_number()
            password_hash = fake.sha256()

            # Insert statement (raw SQL)
            cursor.execute("""
                INSERT INTO eed_data_user (name, email, phone_number, password_hash)
                VALUES (%s, %s, %s, %s)
            """, [name, email, phone_number, password_hash])

if __name__ == "__main__":
    insert_fake_data()
    print("Fake data inserted successfully!")
