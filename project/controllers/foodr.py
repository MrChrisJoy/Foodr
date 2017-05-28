# -*- coding: utf-8 -*-
import os, json, random
from Restaurant import *
from project import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# Global Data Stores
Restaurants = []
Cuisines = ["American", "Arabian", "Australian", "Chinese", "Eastern European", "French",
            "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
            "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Oriental", "Pakistani",
            "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
            "Turkish", "Vietnamese", "Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "BBQ",
            "Bubble Tea", "Burgers", "Charcoal Chicken", "Coffee", "Drink", "Dumplings", "Fast Food",
            "Fish and Chips", "Frozen Yogurt",  "Grill", "Healthy Food", "Ice Cream", "Juice",
            "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Pub Food", "Ramen", "Sandwich", "Seafood",
            "Soul Food", "Steakhouse", "Sushi Train", "Tapas", "Tea House", "Teppanyaki", "Teriyaki", "Yum Cha"]
Liked = []

# load restaruants from static json data using the restaraunts model
local_data = os.path.join(app.static_folder, 'data/restaurant.json')
with open(local_data) as f:
    lines = json.load(f)
    data = lines["Restaurants"]

    for r in data:
        Restaurants.append(Restaurant(r['id'], r['name'], r['postcode'], r['lng'], r['lat'], r['rating'],
                                      r['vicinity'], r['type'], ", ".join([str(x) for x in r['cuisines']]), str(r['alcohol']).lower(),
                                      str(r['wheelchair']).lower(), str(r['wifi']).lower(), ", ".join([str(x) for x in r['deals']])))


@app.route('/')
def start():
    query = request.args.get('q')
    return render_template('foodr/index.html', query=query, restaurants=Restaurants, cuisines=Cuisines)

@app.route('/search')
def search():
    query = request.args.get('q')
    # linear search: append restaruants that contains the query
    results = []
    count = 0
    if query != "":
        querys = query.split(" ")
        # iterate over restaurant elements
        for q in querys:
            for r in Restaurants:
                # RESULT RANKING CONDITIONS PRIORITY (TODO: come up with a better way)
                if (q.lower() in r.name.lower()) & (q in r.cuisine) & (q.lower() in r.vicinity.lower()):
                    count = count + 1
                    results.insert(0, r)
                elif ((q.lower() in r.name.lower()) & (q.lower() in r.vicinity.lower())) | (q in r.cuisine):
                    # prevent duplicated results
                    if r not in results:
                        count = count + 1
                        results.append(r)
                elif ((q.lower() in r.name.lower()) & (q in r.cuisine)) | (q.lower() in r.vicinity.lower()):
                    if r not in results:
                        count = count + 1
                        results.append(r)
                elif (q.lower() in r.name.lower()) | ((q in r.cuisine) & (q.lower() in r.vicinity.lower())):
                    if r not in results:
                        count = count + 1
                        results.append(r)
                elif (q.lower() in r.name.lower()) | (q in r.cuisine) | (q.lower() in r.vicinity.lower()):
                    if r not in results:
                        count = count + 1
                        results.append(r)

    return render_template('foodr/search.html', query=query, results=results, count=count)

Liked = []

@app.route('/like')
def like():
    r = request.args.get('r')
    Liked.append(r)
    return render_template('foodr/saved_restaurants.html', liked=Liked)

@app.route('/dislike')
def dislike():
    r = request.args.get('r')
    Liked.remove(r)
    return render_template('foodr/saved_restaurants.html')



@app.route('/restaurants/')
def restaurants():
    query = request.args.get('q')
    return render_template('foodr/index.html', query=query, restaurants=Restaurants)

@app.route('/deals/')
def deals():
    query = request.args.get('q')
    return render_template('foodr/deals.html', query=query)

@app.route('/saved/')
def saved():
    query = request.args.get('q')
    return render_template('foodr/saved.html', query=query)

@app.route('/saved/restaurants/')
def saved_restaurants():
    query = request.args.get('q')
    return render_template('foodr/saved_restaurants.html', liked=Liked, query=query)

@app.route('/saved/deals/')
def saved_deals():
    query = request.args.get('q')
    return render_template('foodr/saved_deals.html', query=query)


# @app.route('/print', methods=['GET', 'POST'])
# def printer():
#     form = CreateForm(request.form)
#     if request.method == 'POST' and form.validate():
#         from project.models.Printer import Printer
#         printer = Printer()
#         printer.show_string(form.text.data)
#         return render_template('printer/index.html')
#     return render_template('printer/print.html', form=form)
