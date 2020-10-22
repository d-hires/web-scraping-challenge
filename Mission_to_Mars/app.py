from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find()
    return render_template("index.html", mars=mars)


@app.route("/scrape")
def scraper():
    mars_db = mongo.db.mars
    # mars_db.drop()
    mars_data = scrape_mars.scrape()
    print(mars_data, sys.stderr)
    mars_db.insert_many(mars_data)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
