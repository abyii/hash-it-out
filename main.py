from quart import Quart, request
from dotenv import load_dotenv
from db import get_database
import bson.json_util as json_util
from os import environ


app = Quart(__name__)

load_dotenv()

db = get_database()
aliens = db["aliens"]

@app.route('/')
async def hello():
    return 'hash bash slash dash'

@app.route('/new', methods=["POST"])
async def new_alien():
    try:
        if environ['ADMIN_PASS'] != request.args.get("pass_token"):
            return "ONLY ADMINS CAN CREATE NEW ALIENS"
        name = request.args.get("name")
        age = request.args.get("age")
        native_planet = request.args.get("native_planet")
        weight = request.args.get("weight")
        height = request.args.get("height")
        language = request.args.get("language") 

        if not name:
            return "Name is required"

        existing = aliens.find_one({"name":name})
        
        if existing:
            return "Name cannot be same for multiple aliens"

        aliens.insert_one({
            "name":name,
            "age":age,
            "native_planet":native_planet,
            "weight":weight,
            "height":height,
            "language":language
        })

        return 'new alien created'
    except:
        return "Something went wrong"

@app.route('/update/<string:name>', methods=["PUT"])
async def update(name):
    try:
        if environ['ADMIN_PASS'] != request.args.get("pass_token"):
            return "ONLY ADMINS CAN UPDATE NEW ALIENS"
        existing = aliens.find_one({"name":name})
        if not existing:
            return "That alien doesnt exist"

        age = request.args.get("age")
        native_planet = request.args.get("native_planet")
        weight = request.args.get("weight")
        height = request.args.get("height")
        language = request.args.get("language") 

        aliens.update_one({"name":name}, {
            "$set":{
                "age":age or existing["age"],
                "native_planet":native_planet or existing["native_planet"],
                "weight":weight or existing["weight"],
                "height":height or existing["height"],
                "language":language or existing["language"]
            }})

        return 'alien '+name+" got updated!"
    except:
        return "Something went wrong"

@app.route('/get-all', methods=["GET"])
async def getAll():
    try:
        if environ['ADMIN_PASS'] != request.args.get("pass_token"):
            return "ONLY ADMINS CAN GET ALL THE ALIENS INFO"
        all = aliens.find()
        if not all:
            return "No aliens"
        return json_util.dumps(all)
    except:
        return "Something went wrong"


@app.route('/delete/<string:name>', methods=["DELETE"])
async def delete(name):
    try:
        if environ['ADMIN_PASS'] != request.args.get("pass_token"):
            return "ONLY ADMINS CAN DELETE NEW ALIENS"
        existing = aliens.find_one({"name":name})
        if not existing:
            return "That alien doesnt exist"
        aliens.delete_one({"name":name})

        return "Alien " + name + " got deleted!"
    except:
        return "Something went wrong"

app.run()  