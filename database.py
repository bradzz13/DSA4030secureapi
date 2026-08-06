from app import app, db, bcrypt
from models import User, Customer

from faker import Faker
import random
import time



fake = Faker()


# DATABASE INITIALIZATION

with app.app_context():

    print("Creating database tables...")

    db.create_all()

    print("Database tables created successfully.")


    # CREATE USERS

    print("Creating system users...")


    users = [

        User(
            username="admin",
            password_hash=bcrypt.generate_password_hash(
                "Admin123!"
            ).decode("utf-8"),
            role="admin"
        ),

        User(
            username="analyst",
            password_hash=bcrypt.generate_password_hash(
                "Analyst123!"
            ).decode("utf-8"),
            role="analyst"
        ),

        User(
            username="customer",
            password_hash=bcrypt.generate_password_hash(
                "Customer123!"
            ).decode("utf-8"),
            role="customer"
        )

    ]


    db.session.add_all(users)

    db.session.commit()


    print("Users created successfully.")



    # GENERATE 100,000 CUSTOMER RECORDS

    print("Generating 100,000 customer records...")


    batch_size = 5000

    total_records = 100000


    for start in range(
        0,
        total_records,
        batch_size
    ):

        customers = []


        for i in range(
            start,
            min(
                start + batch_size,
                total_records
            )
        ):

            customer = Customer(

                customer_id=f"CUST-{i + 1:06d}",

                name=fake.name(),

                email=fake.email(),

                country=fake.country(),

                purchase_amount=round(
                    random.uniform(
                        10,
                        10000
                    ),
                    2
                )

            )


            customers.append(customer)


        db.session.add_all(customers)

        db.session.commit()


        print(
            f"Inserted records: "
            f"{min(start + batch_size, total_records)}"
        )


    print(
        "SUCCESS: 100,000 customer records created."
    )