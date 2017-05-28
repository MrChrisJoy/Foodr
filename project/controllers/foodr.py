# -*- coding: utf-8 -*-
import os, json, random
from Restaurant import *
from project import app
from flask import render_template, request, redirect
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
Disliked = []

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

Restaurants.sort(key = lambda x: x.id)

@app.route('/')
def start():
	query = request.args.get('q')
	Recommended = []
	for r in Restaurants[:40]:
		if r not in Liked and r not in Disliked:
			Recommended.append(r)
	return render_template('foodr/index.html', query=query, restaurants=Recommended, cuisines=Cuisines)

@app.route('/search')
def search():
	query = request.args.get('q')
	#linear search: append restaurants that contains the query
	results = [[] for x in xrange(26*9)]
	results.append([])
	count = 0
	if query != "":
		querys = query.split(" ")
		for r in Restaurants:
			if r not in Liked and r not in Disliked:
				#iterate through each restaurant and check for priority according to query
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
	return render_template('foodr/search.html', query=query, results=results, count=count, url=request.url[len(request.url_root):])


@app.route('/view')
def view():
    r = request.args.get('r')
    return render_template('foodr/view_restaurant.html', result=Restaurants[int(r)], title=Restaurants[int(r)].name, url=request.url[len(request.url_root):])





@app.route('/like')
def like():
    r = request.args.get('r')
    callback = request.args.get('callback')
    if Restaurants[int(r)] not in Liked:
	    Liked.append(Restaurants[int(r)])
    return redirect('/'+callback)
@app.route('/unlike')
def unlike():
    r = request.args.get('r')
    callback = request.args.get('callback')
    if Restaurants[int(r)] in Liked:
	    Liked.remove(Restaurants[int(r)])
    return redirect('/'+callback)

@app.route('/dislike')
def dislike():
    r = request.args.get('r')
    callback = request.args.get('callback')
    if Restaurants[int(r)] not in Disliked:
	    Disliked.append(Restaurants[int(r)])
    if Restaurants[int(r)] in Liked:
	    Liked.remove(Restaurants[int(r)])
    return redirect('/'+callback)



@app.route('/restaurants/')
def restaurants():
    query = request.args.get('q')
    return render_template('foodr/index.html', query=query, restaurants=Restaurants, url=request.url[len(request.url_root):])

@app.route('/deals/')
def deals():
    query = request.args.get('q')
    return render_template('foodr/deals.html', query=query, url=request.url[len(request.url_root):])

@app.route('/saved/')
def saved():
    query = request.args.get('q')
    return render_template('foodr/saved.html', query=query, url=request.url[len(request.url_root):])

@app.route('/saved/restaurants/')
def saved_restaurants():
    query = request.args.get('q')
    return render_template('foodr/saved_restaurants.html', liked=Liked, query=query, url=request.url[len(request.url_root):])

@app.route('/saved/deals/')
def saved_deals():
    query = request.args.get('q')
    return render_template('foodr/saved_deals.html', query=query, url=request.url[len(request.url_root):])



# @app.route('/print', methods=['GET', 'POST'])
# def printer():
#     form = CreateForm(request.form)
#     if request.method == 'POST' and form.validate():
#         from project.models.Printer import Printer
#         printer = Printer()
#         printer.show_string(form.text.data)
#         return render_template('printer/index.html')
#     return render_template('printer/print.html', form=form)
