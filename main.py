from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=["GET"])
def random():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = choice(all_cafes)

    return jsonify(cafe={
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price,
        "has_sockets": random_cafe.has_sockets,
        "has_toilets": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "id": random_cafe.id,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "map_url": random_cafe.map_url,
        "name": random_cafe.name,
        "seats": random_cafe.seats,
    })


@app.route("/all", methods=["GET"])
def all():
    all_cafes = db.session.query(Cafe).all()
    cafe_list = [{
        "can_take_calls": cafe.can_take_calls,
        "coffee_price": cafe.coffee_price,
        "has_sockets": cafe.has_sockets,
        "has_toilets": cafe.has_toilet,
        "has_wifi": cafe.has_wifi,
        "id": cafe.id,
        "img_url": cafe.img_url,
        "location": cafe.location,
        "map_url": cafe.map_url,
        "name": cafe.name,
        "seats": cafe.seats,
    } for cafe in all_cafes]
    return jsonify(cafe=cafe_list), 200


@app.route("/search", methods=["GET"])
def cafe_search():
    location = request.args.get("loc")
    print(location)
    cafe = Cafe.query.filter_by(location=location).first()
    if cafe == None:
        return jsonify(error={
            "Not found": "Sorry, we don't have cafe at that location!",
        }), 404
    else:
        return jsonify(cafe={
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price,
            "has_sockets": cafe.has_sockets,
            "has_toilets": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "id": cafe.id,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "map_url": cafe.map_url,
            "name": cafe.name,
            "seats": cafe.seats,
        }), 200


## HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def add():
    new_cafe = Cafe(name=request.form.get("name"),
                    map_url=request.form.get("map_url"),
                    img_url=request.form.get("img_url"),
                    location=request.form.get("location"),
                    seats=bool(request.form.get("seats")),
                    has_toilet=bool(request.form.get("has_toilet")),
                    has_wifi=bool(request.form.get("has_wifi")),
                    has_sockets=bool(request.form.get("has_sockets")),
                    can_take_calls=bool(request.form.get("can_take_calls")),
                    coffee_price=request.form.get("coffee_price"),
                    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={
        "success": " You have succesfully added a cafe"
    })

@app.route("/coffee_price_change", methods=["PATCH"])
def price_change():
    cafe_id = request.args.get("id")
    cafe_to_patch = Cafe.query.get(cafe_id)
    if cafe_to_patch is None:
        return jsonify(error={
            "Not found": "Sorry, we don't have cafe at that location!",
        }), 404
    else:
        cafe_to_patch.coffee_price = request.form.get("coffee_price")
        db.session.commit()
        return jsonify(success={
            "success": " You have succesfully added a new price",
        }), 200


## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record
@app.route("/delete_cafe/<int:id>", methods=["DELETE"])
def delete_cafe(id):
    cafe_to_delete = db.session.query(Cafe).get(id)
    api_key = request.form.get("api_key")
    if cafe_to_delete and api_key == "TopSecretAPIKey":
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(success={
            "success": " You have succesfully deleted a cafe",
        }), 200
    else:
        return jsonify(error={
            "Not found": "Sorry, we don't have cafe at that location!",
        }), 404







if __name__ == '__main__':
    app.run(debug=True)
