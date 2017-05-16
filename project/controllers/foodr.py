# -*- coding: utf-8 -*-
import os, json, Restaurant, random
from project import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

Restaurants = []
local_data = os.path.join(app.static_folder, 'data/restaurant.json')
with open(local_data) as f:
    lines = json.load(f)
    data = lines["Restaurants"]
    for r in data:
        Restaurants.append(
            Restaurant.Restaurant(str(r["name"]), str(" ".join(r["dietary"])).split(" "),
                                  str(" ".join(r["deals"])).split(','), str(r["alcohol"]), str(r["wheelchair"]),
                                  str(r["wifi"])))


@app.route('/')
def start():
    query = request.args.get('q')
    return render_template('foodr/index.html', query=query, restaurants=Restaurants)

@app.route('/search')
def search():
    query = request.args.get('q')

    # linear search: append restaruants that contains the query
    results = []
    count = 0
    if query != "":
        # iterate over restaurant elements
        for r in Restaurants:
            # obtain lower case dietary & deals elements
            dietary = [x.lower() for x in r.dietary]
            deals = [x.lower() for x in r.deals]
            if (query.lower() in r.name.lower()) | (query in dietary) | (query in deals):
                count = count + 1
                results.append(r)

    return render_template('foodr/search.html', query=query, results=results, count=count, lat=150+random.random()/100, long=150+random.random()/100+100)







@app.route('/restaurants/')
def restaurants():
    query = request.args.get('q')
    return render_template('foodr/restaurants.html', query=query)

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
    return render_template('foodr/saved_restaurants.html', query=query)

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
