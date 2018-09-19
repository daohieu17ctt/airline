from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("postgres://sgjzmebtdhpach:9311cfaed8cb528d0c15188fb32cadb4cd5b5bbf3addfa65a3353447f127d7f6@ec2-54-225-97-112.compute-1.amazonaws.com:5432/d4d1is00qm8asc")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights = flights)

@app.route("/book", methods=["POST"])
def book():
    
    # Get form information.
    name = request.form.get("name")
    try:
        flight_id = int(request.form.get("flight_id"))
    except ValueError:
        return render_template("error.html", message="Invalid flight number")
    
    # Make sure the flight exists.
    if db.execute("SELECT * FROM flights WHERE id = :id", {"id": flight_id}).rowcount == 0:
        return render_template("error.html", message="No such flight with that id")
    db.execute("INSERT INTO passengers(name, flight_id) VALUES (:name, :flight_id)", {"name": name, "flight_id": flight_id})
    db.commit()
    return render_template("success.html")

@app.route("/flights")
def flights():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=flights)

@app.route("/flights/<int:flight_id>")
def flight(flight_id):
    passengers = db.execute("SELECT * FROM passengers WHERE flight_id = :flight_id", {"flight_id": flight_id}).fetchall()
    flight = db.execute("SELECT * FROM flights WHERE id = :flight_id", {"flight_id": flight_id}).fetchone()
    return render_template("flight.html", passengers=passengers, flight=flight)
