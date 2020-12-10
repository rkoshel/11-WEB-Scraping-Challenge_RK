from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars.py

app = Flask(__name__)

# setup mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#conn = "mongodb://localhost:27017"
#client = pymongo.MongoClient(conn)

# connect to mongo db and collection
#db = client.store_inventory
#produce = db.produce


@app.route("/")
def index():
    mars_db = mongo.db.mars_db.find_one()
    return render_template("index.html", mars = mars_db)

@app.route("/scrape")
def scraper():
    mars = mongo.db.mars_db
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)