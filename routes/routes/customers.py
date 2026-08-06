from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from models import Customer

import logging


customers = Blueprint(
    "customers",
    __name__
)


# ROLE CHECK HELPER

def role_required(allowed_roles):

    def decorator(function):

        from functools import wraps

        @wraps(function)
        @jwt_required()
        def wrapper(*args, **kwargs):

            claims = get_jwt()

            username = claims.get("username")

            role = claims.get("role")


            if role not in allowed_roles:

                logging.warning(

                    f"Unauthorized access attempt: "

                    f"user={username}, "

                    f"role={role}, "

                    f"required_roles={allowed_roles}"

                )


                return jsonify({

                    "message": "Access denied",

                    "error": "Insufficient permissions",

                    "your_role": role,

                    "required_roles": allowed_roles

                }), 403


            return function(*args, **kwargs)


        return wrapper

    return decorator


# ==================================================
# GENERAL CUSTOMER DATA
# ADMIN AND ANALYST

@customers.route(
    "/customers",
    methods=["GET"]
)
@role_required(["admin", "analyst"])
def get_customers():

    claims = get_jwt()

    username = claims.get("username")

    role = claims.get("role")


    logging.info(

        f"Customer data accessed by "

        f"user={username}, "

        f"role={role}"

    )


    customer_records = Customer.query.limit(
        100
    ).all()


    results = []


    for customer in customer_records:

        results.append({

            "customer_id": customer.customer_id,

            "name": customer.name,

            "email": customer.email,

            "country": customer.country,

            "purchase_amount": customer.purchase_amount

        })


    return jsonify({

        "count": len(results),

        "data": results

    }), 200


# ==================================================
# ADMIN-ONLY ENDPOINT
# ==================================================

@customers.route(
    "/admin/customers",
    methods=["GET"]
)
@role_required(["admin"])
def admin_customers():

    claims = get_jwt()

    username = claims.get("username")


    logging.info(

        f"Admin endpoint accessed by "

        f"user={username}"

    )


    return jsonify({

        "message": "Admin access granted",

        "user": username,

        "role": "admin"

    }), 200