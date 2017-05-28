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
Keywords = ["American", "Arabian", "Australian", "Chinese", "French",
            "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
            "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Pakistani",
            "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
            "Turkish", "Vietnamese", "Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "BBQ",
            "Burgers", "Charcoal Chicken", "Coffee", "Drink", "Dumplings", "Fast Food",
            "Fish and Chips", "Frozen Yogurt", "Grill", "Ice Cream", "Juice",
            "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Ramen", "Sandwich", "Seafood",
            "Steakhouse", "Sushi", "Tapas", "Teppanyaki", "Teriyaki", "Yum Cha"]
Liked = []

# load restaruants from static json data using the restaraunts model
local_data = os.path.join(app.static_folder, 'data/restaurant.json')
with open(local_data) as f:
    lines = json.load(f)
    data = lines["Restaurants"]

    for r in data:
        Restaurants.append(Restaurant(r['id'], r['name'], r['postcode'], r['lng'], r['lat'], r['rating'],
                                      r['vicinity'], r['type'], r['cuisines'], str(r['alcohol']).lower(),
                                      str(r['byo']).lower(), str(r['wheelchair']).lower(), str(r['wifi']).lower(),
                                      str(r['pets']).lower(), str(r['card']).lower(), str(r['music']).lower(),
                                      str(r['tv']).lower(), str(r['parking']).lower(), r['photos'],
                                      r['times'], r['deals']))

@app.route('/')
def start():
    query = request.args.get('q')
    return render_template('foodr/index.html', query=query, restaurants=Restaurants, cuisines=Cuisines)

@app.route('/search')
def search():
    query = request.args.get('q')
    #linear search: append restaurants that contains the query
    results = [[] for x in xrange(26*9)]
    count = 0
    if query != "":
        querys = query.split(" ")
        for r in Restaurants:
            #iterate through each restaurant and check for priority according to query
            relevance = -1
            for q in querys:
                if q.lower() in r.name.lower():
                    relevance = relevance + 1
                for cuisine in r.cuisines:

                    if q.lower() == cuisine.lower():
                        relevance = relevance + 1
                if q.lower() in r.vicinity.lower():
                    relevance = relevance + 1
            if relevance > -1:
                results[relevance].append(r)
                count = count + 1
    results.reverse()
    return render_template('foodr/search.html', query=query, results=results, count=count)

# def filterBoolean(field):
#     resultstrue = []
#     resultsfalse = []
#     for r in Restaurants:
#         if r.getField(field):
#             resultstrue += [r]
#         else:
#             resultsfalse += [r]
#     return resultstrue + resultsfalse


@app.route('/advsearch')
def advSearch():
    queryCuisine = request.args.get('c')
    # queryVicinity = request.args.get('v')
    queryRating = request.args.get('r')
    queryType = request.args.get('t')
    queryAlcohol = request.args.get('a')
    queryWheelchair = request.args.get('wh')
    queryWifi = request.args.get("wi")

    results = [[] for x in xrange(16)]
    count = 0
    for r in Restaurants:
        relevance = -1
        for restCuisine in r.cuisine:
            for cuisine in queryCuisine:
                if cuisine == restCuisine:
                    relevance = relevance + 1
        # if (queryVicinity > r.vicinity):
        #     relevance = relevance + 1
        if (queryRating < r.rating):
            relevance = relevance + 1
        if (queryType == r.type):
            relevance = relevance + 1
        if (queryAlcohol == r.alcohol):
            relevance = relevance + 1
        if (queryWheelchair == r.wheelchair):
            relevance = relevance + 1
        if (queryWifi == r.wifi):
            relevance = relevance + 1
        if(count > -1):
            results[relevance].append(r)
            count = count + 1
    results.reverse()
    return render_template('foodr/advsearch.html')

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