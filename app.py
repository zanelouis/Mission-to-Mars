from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds data from mongo
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

if __name__ == "__main__":
    # If running as script, print scraped data
    app.run(debug= True)