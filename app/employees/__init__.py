from flask import Blueprint

employees = Blueprint('employees', __name__)

from app.employees import routes
