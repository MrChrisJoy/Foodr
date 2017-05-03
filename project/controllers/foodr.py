# -*- coding: utf-8 -*-
from project import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

DEBUG_TB_INTERCEPT_REDIRECTS = False
class CreateForm(FlaskForm):
    text = StringField('name', validators=[DataRequired()])


@app.route('/')
def start():
    return render_template('foodr/index.html')

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
