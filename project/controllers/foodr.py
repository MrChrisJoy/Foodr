# -*- coding: utf-8 -*-
import os, json, Restaurant
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

DEBUG_TB_INTERCEPT_REDIRECTS = False
class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])


@app.route('/')
def start():
    restaurants = json.load(open(local_data))
    return render_template('foodr/index.html', restaurants=restaurants)

@app.route('/search')
def search():
    query = request.args.get('q')
    return render_template('foodr/search.html', query=query)

@app.route('/restaurants/')
def restaurants():
    return render_template('foodr/restaurants.html')

@app.route('/deals/')
def deals():
    return render_template('foodr/deals.html')

@app.route('/saved/')
def saved():
    return render_template('foodr/saved.html')

@app.route('/saved/restaurants/')
def saved_restaurants():
    return render_template('foodr/saved_restaurants.html')
@app.route('/saved/deals/')
def saved_deals():
    return render_template('foodr/saved_deals.html')


# @app.route('/print', methods=['GET', 'POST'])
# def printer():
#     form = CreateForm(request.form)
#     if request.method == 'POST' and form.validate():
#         from project.models.Printer import Printer
#         printer = Printer()
#         printer.show_string(form.text.data)
#         return render_template('printer/index.html')
#     return render_template('printer/print.html', form=form)
