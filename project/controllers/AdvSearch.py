# @app.route('/search')
# def search():
#     query = request.args.get('q')
#
#     # linear search: append restaruants that contains the query
#     results = []
#     count = 0
#     if query != "":
#         # iterate over restaurant elements
#         for r in Restaurants:
#             # obtain lower case dietary & deals elements
#             dietary = [x.lower() for x in r.dietary]
#             deals = [x.lower() for x in r.deals]
#             if (query.lower() in r.name.lower()) | (query in dietary) | (query in deals):
#                 count = count + 1
#                 results.append(r)
#
#     return render_template('foodr/search.html', query=query, results=results, count=count, lat=150+random.random()/100, long=150+random.random()/100+100)

# import os, json, random
# import Restaurant
# import foodr
# from project import app
# from flask import render_template, request
#
# @app.route('/advsearch')
# def advSearch():
#     queryCuisine = request.args.get('c')
#     queryVicinity = request.args.get('v')
#     queryRating = request.args.get('r')
#     queryType = request.args.get('t')
#     queryAlcohol = request.args.get('a')
#     queryWheelchair = request.args.get('wh')
#     queryWifi = request.args.get("wi")
#
#     results = []
#     results.append([])
#     for r in Restaurants:
#         count = -1
#         if (queryCuisine in r.cuisine):
#             count = count + 1
#         if (queryVicinity > r.vicinity):
#             count = count + 1
#         if (queryRating < r.rating):
#             count = count + 1
#         if (queryType == r.type):
#             count = count + 1
#         if (queryAlcohol == r.alcohol):
#             count = count + 1
#         if (queryWheelchair == r.wheelchair):
#             count = count + 1
#         if (queryWifi == r.wifi):
#             count = count + 1
#         if(count > -1):
#             results[count].append(r)
#     return render_template('foodr/advsearch.html')