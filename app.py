import certifi
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://yashjain74170:3IOBzOZjV5ZUfMhz@todoproject.lcce3hx.mongodb.net/?retryWrites=true&w=majority&appName=todoproject"

# ✅ certifi ke SSL certs use karo
client = MongoClient(uri, tlsCAFile=certifi.where(), server_api=ServerApi('1'))

db = client["todo"]
todos = db["tasks"]

@app.route("/")
def home():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_desc = request.form.get("itemDescription")

    todos.insert_one({
        "name": item_name,
        "description": item_desc
    })

    return "Item added successfully ✅ <br><a href='/'>Go Back</a>"

@app.route("/gettodos", methods=["GET"])
def get_todos():
    items = list(todos.find({}, {"_id": 0}))
    return jsonify(items), 200

if __name__ == "__main__":
    app.run(debug=True)
