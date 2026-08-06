from extensions import db

# USER TABLE

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )


# ==================================================
# CUSTOMER DATA TABLE
# ==================================================

class Customer(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(150),
        nullable=False
    )

    country = db.Column(
        db.String(50),
        nullable=False
    )

    purchase_amount = db.Column(
        db.Float,
        nullable=False
    )