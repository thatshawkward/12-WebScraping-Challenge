from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    all_data = scrape.news_scrape()
    all_data = scrape.img_scrape()
    all_data = scrape.twitter_scrape()
    all_data = scrape.facts_scrape()
    all_data = scrape.hemi_scrape()
    mars.update({}, all_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)