#from models.user import User
from models.product import Product
#from models.review import Review


from flask import Blueprint
from init import db, ma

#define the blueprint for the database commands
db_commands = Blueprint("db", __name__)

#Set up the create all tables function
@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("All Tables created!")

#Set up the seed all tables with inserted information from user
#@db_commands.cli.command("seed")
#def seed_tables():
#Create a list of User instances
#    Product({
#       "name": "Giant Bike", 
#       "description": "24inch Wheel Mountain bike.",
#        "category": "Sports"
#    }
#    )

#    print("Tables Seeded")

#Set up the drop tables function

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables droppped.")