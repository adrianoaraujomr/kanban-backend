from flask import Blueprint
from src.global_error_handling import InsufficientStorage

error_route = Blueprint("error_route", __name__)

@error_route.route("/insufficient-storage", strict_slashes=False)
def insufficient_storage():
    raise InsufficientStorage()