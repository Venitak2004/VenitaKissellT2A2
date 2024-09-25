from datetime import date

from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.product import Product
from models.review import Review

#define the bluepring for the database commands
dbcommands_bp = Blueprint("db", __name__)

#Set up the create all tables function
@dbcommands_bp.cli.command("create")
def create_tables():
    db.create_all()
    print("All Tables created!")

#Set up the seed all tables with inserted information from user
#@db_commands.cli.command("seed")
#def seed_tables():
# Create a list of User instances
#print("Tables seeded!")

#Set up the drop tables function
@dbcommands_bp.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped.")