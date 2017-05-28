# -*- coding: utf-8 -*-
import os, json, random
from Restaurant import *
from project import app
from flask import render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

# Global Data Stores
Types = ["bar", "bakery", "cafe", "restaurant", "meal_takeaway", "meal_delivery"]
Cuisines = ["American", "Arabian", "Australian", "Chinese", "French",
            "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
            "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Pakistani",
            "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
            "Turkish", "Vietnamese", "Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "BBQ",
            "Burgers", "Charcoal Chicken", "Coffee", "Drink", "Dumplings", "Fast Food",
            "Fish and Chips", "Frozen Yogurt", "Grill", "Ice Cream", "Juice",
            "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Ramen", "Sandwich", "Seafood",
            "Steakhouse", "Sushi", "Tapas", "Teppanyaki", "Teriyaki", "Yum Cha"]
AllDeals = ["$5 off", "$10 off", "$15 off",
            "$5 off if you spend over $20", "$5 off if you spend over $30", "$10 off if you spend over $50",
             "Free drink with any meal", "Free drink with any purchase", "Free drink if you spend over $10",
             "Buy one get one free", "2 for 1", "Buy two get one free",
             "All you can eat for $20pp", "All you can eat for $25pp", "All you can eat for $30pp",
            "10% off", "15% off", "20% off"]

Restaurants = []
Liked = []
Disliked = []
Recommended = []
Deals = {}
SavedDeals = {}
DisDeals = {}
for d in AllDeals:
    Deals[d] = []
    SavedDeals[d] = []
    DisDeals[d] = []

# load restaruants from static json data using the restaraunts model
local_data = os.path.join(app.static_folder, 'data/restaurant.json')
with open(local_data) as f:
    lines = json.load(f)
    data = lines["Restaurants"]

    for r in data:
        rest = Restaurant(r['id'], r['name'], r['postcode'], r['lng'], r['lat'], r['rating'],
                                      r['vicinity'], r['type'], r['cuisines'], str(r['alcohol']).lower(),
                                      str(r['byo']).lower(), str(r['wheelchair']).lower(), str(r['wifi']).lower(),
                                      str(r['pets']).lower(), str(r['card']).lower(), str(r['music']).lower(),
                                      str(r['tv']).lower(), str(r['parking']).lower(), r['photos'],
                                      r['times'], r['deals'])
        Restaurants.append(rest)
        for d in r['deals']:
            Deals[d].append(rest)

Restaurants.sort(key=lambda x: x.id)

def initWeightings():
    w = {}
    for c in Cuisines:
        w[c] = 0
    for t in Types:
        w[t] = 0
    # w['alcohol'] = float(0)
    # w['byo'] = float(0)
    # w['wheelchair'] = float(0)
    # w['wifi'] = float(0)
    # w['pets'] = float(0)
    # w['card'] = float(0)
    # w['music'] = float(0)
    # w['tv'] = float(0)
    # w['parking'] = float(0)
    w['postcode'] = float(0)
    return w

def fillWeightings():
    w = initWeightings()
    total = 1
    for r in Liked:
        for cuisine in r.cuisines:
            w[cuisine] += 1
        w[r.type] += 1
        if w['postcode'] == 0:
            w['postcode'] = r.postcode
        else:
            w['postcode'] = int(w['postcode'] + r.postcode)/2
        # w['alcohol'] = (w['alcohol']+(1 if r.alcohol == 'true' else 0))/total
        # w['byo'] = (w['byo']+(1 if r.byo == 'true' else 0))/total
        # w['wheelchair'] = (w['wheelchair']+(1 if r.wheelchair == 'true' else 0))/total
        # w['wifi'] = (w['wifi']+(1 if r.wifi == 'true' else 0))/total
        # w['pets'] = (w['pets']+(1 if r.pets == 'true' else 0))/total
        # w['card'] = (w['card']+(1 if r.card == 'true' else 0))/total
        # w['music'] = (w['music']+(1 if r.music == 'true' else 0))/total
        # w['tv'] = (w['tv']+(1 if r.tv == 'true' else 0))/total
        # w['parking'] = (w['parking']+(1 if r.parking == 'true' else 0))/total
        total += 1
    for r in Disliked:
        for cuisine in r.cuisines:
            w[cuisine] -= 1
        w[r.type] -= 1
    return w

def applyWeight(weights):
    for r in Restaurants:
        total = 0
        for c in r.cuisines:
            total += weights[c]
        total += weights[r.type]
        r.weight = total

@app.route('/')
def start():
    query = request.args.get('q')
    Weightings = fillWeightings()
    applyWeight(Weightings)
    weighted = [x for x in Restaurants]
    if len(Liked) + len(Disliked) == 0:
        random.shuffle(weighted)
    weighted.sort(key=lambda x: -x.weight)
    for r in Recommended:
        if r.weight < -5:
            Recommended.remove(r)
    if len(Recommended) < 40:
        for r in weighted:
            if len(Recommended) >= 40:
                break
            if r not in Liked and r not in Disliked and r not in Recommended:
                Recommended.append(r)
    return render_template('foodr/index.html', query=query, restaurants=Recommended, cuisines=Cuisines)


@app.route('/search')
def search():
    query = request.args.get('q')
    # linear search: append restaurants that contains the query
    results = [[] for x in xrange(26 * 9)]
    results.append([])
    count = 0
    if query != "":
        querys = query.split(" ")
        for r in Restaurants:
            if r not in Liked and r not in Disliked:
                # iterate through each restaurant and check for priority according to query
                relevance = -1
                for q in querys:
                    if q.lower() in r.name.lower():
                        relevance += 1
                    for cuisine in r.cuisines:
                        if q.lower() == cuisine.lower():
                            relevance += 1
                    if q.lower() in r.vicinity.lower():
                        relevance += 1
                if relevance > -1:
                    results[relevance].append(r)
                    count = count + 1
    # i = 0
    # while i < 26*9:
    # 	for j in results[i]:
    # 		print "row ", i, " : ", j.name
    # 	i += 1

    results.reverse()
    return render_template('foodr/search.html', query=query, results=results, count=count,
                           url=request.url[len(request.url_root):])


@app.route('/view')
def view():
    r = request.args.get('r')
    return render_template('foodr/view_restaurant.html', result=Restaurants[int(r)], title=Restaurants[int(r)].name,
                           url=request.url[len(request.url_root):])


@app.route('/save_deal')
def save_deal():
    r = request.args.get('r')
    callback = request.args.get('callback')
    deal, restaurant = str(r).split('-')
    if Restaurants[int(restaurant)] not in SavedDeals[AllDeals[int(deal)]]:
        SavedDeals[AllDeals[int(deal)]].append(Restaurants[int(restaurant)])
    return redirect('/' + callback)

@app.route('/unsave_deal')
def unsave_deal():
    r = request.args.get('r')
    callback = request.args.get('callback')
    deal, restaurant = str(r).split('-')
    if Restaurants[int(restaurant)] in SavedDeals[AllDeals[int(deal)]]:
        SavedDeals[AllDeals[int(deal)]].remove(Restaurants[int(restaurant)])
    if Restaurants[int(restaurant)] not in DisDeals[AllDeals[int(deal)]]:
        DisDeals[AllDeals[int(deal)]].append(Restaurants[int(restaurant)])
    return redirect('/' + callback)


@app.route('/like')
def like():
    r = request.args.get('r')
    callback = request.args.get('callback')
    if Restaurants[int(r)] not in Liked:
        Liked.append(Restaurants[int(r)])
    if Restaurants[int(r)] in Recommended:
        Recommended.remove(Restaurants[int(r)])
    return redirect('/' + callback)


@app.route('/unlike')
def unlike():
    r = request.args.get('r')
    callback = request.args.get('callback')
    if Restaurants[int(r)] in Liked:
        Liked.remove(Restaurants[int(r)])
    return redirect('/' + callback)


@app.route('/dislike')
def dislike():
    r = request.args.get('r')
    callback = request.args.get('callback')
    if Restaurants[int(r)] not in Disliked:
        Disliked.append(Restaurants[int(r)])
    if Restaurants[int(r)] in Liked:
        Liked.remove(Restaurants[int(r)])
    if Restaurants[int(r)] in Recommended:
        Recommended.remove(Restaurants[int(r)])
    return redirect('/' + callback)


@app.route('/restaurants/')
def restaurants():
    query = request.args.get('q')
    del Recommended[:]
    return render_template('foodr/index.html', query=query, restaurants=Restaurants,
                           url=request.url[len(request.url_root):])


@app.route('/deals/')
def deals():
    query = request.args.get('q')
    del Recommended[:]
    Display = {}
    for d in AllDeals:
        Display[d] = []
    i = 0
    while i < 40:
        d = random.choice(AllDeals)
        r = random.choice(Deals[d])
        if r in DisDeals[d] or r in SavedDeals[d]:
            continue
        Display[d].append(r)
        i += 1
    return render_template('foodr/deals.html', deals=Display, alldeals=AllDeals, query=query, url=request.url[len(request.url_root):])


@app.route('/saved/')
def saved():
    query = request.args.get('q')
    del Recommended[:]
    return render_template('foodr/saved.html', query=query, url=request.url[len(request.url_root):])


@app.route('/saved/restaurants/')
def saved_restaurants():
    query = request.args.get('q')
    del Recommended[:]
    return render_template('foodr/saved_restaurants.html', liked=Liked, query=query,
                           url=request.url[len(request.url_root):])


@app.route('/saved/deals/')
def saved_deals():
    query = request.args.get('q')
    del Recommended[:]
    return render_template('foodr/saved_deals.html', deals=SavedDeals, alldeals=AllDeals, query=query, url=request.url[len(request.url_root):])

# @app.route('/print', methods=['GET', 'POST'])
# def printer():
#     form = CreateForm(request.form)
#     if request.method == 'POST' and form.validate():
#         from project.models.Printer import Printer
#         printer = Printer()
#         printer.show_string(form.text.data)
#         return render_template('printer/index.html')
#     return render_template('printer/print.html', form=form)
