import random, urllib, json

GOOGLE_API_KEY = "AIzaSyBjVLxBPr63YeLF8wpi4ADCzUrBCUYQMzo"
LOCATION = "-33.911751,%20151.223290"
Types = ["bar", "bakery", "cafe", "restaurant", "meal_takeaway", "meal_delivery"]
Keywords = ["American", "Arabian", "Australian", "Chinese", "Eastern European", "French",
            "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
            "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Oriental", "Pakistani",
            "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
            "Turkish", "Vietnamese", "Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "BBQ",
            "Bubble Tea", "Burgers", "Charcoal Chicken", "Coffee", "Drink", "Dumplings", "Fast Food",
            "Fish and Chips", "Frozen Yogurt",  "Grill", "Healthy Food", "Ice Cream", "Juice",
            "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Pub Food", "Ramen", "Sandwich", "Seafood",
            "Soul Food", "Steakhouse", "Sushi Train", "Tapas", "Tea House", "Teppanyaki", "Teriyaki", "Yum Cha"]

# List of Restaruant names (used to avoid duplicates)
Visited = []


def genResult(name, lng, lat, rating, vicinity, _type, keyword):
    result = '\t{\n\t\t"name": '
    # API provided data
    result += '"' + name + '",\n'
    result += '\t\t"lng": '+lng+',\n'
    result += '\t\t"lat": '+lat+',\n'
    result += '\t\t"rating": '+rating+',\n'
    result += '\t\t"vicinity": "'+vicinity+'",\n'
    result += '\t\t"type": "'+_type+'",\n'
    result += '\t\t"cuisine": [ "'+keyword+'" ],\n'

    # made up stuff
    # bars/restaurant alwaus serve alcohol
    if (_type == 'bar') | (_type == 'restaurant'):
        result += '\t\t"alcohol": true,\n'
    else:
        result += '\t\t"alcohol": '+str(random.choice([True, False])).lower()+',\n'

    result += '\t\t"wheelchair": '+str(random.choice([True, False])).lower()+',\n'
    result += '\t\t"wifi": '+str(random.choice([True, False])).lower()+'\n'

    result += '\t},\n'
    return result


fout = open('restaurant.json', 'w')
fout.write('{ "Restaurants":[')

# scan through all the types
for Type in Types:
    # scan through all the keywords
    for Keyword in Keywords:
        print("searching: "+ Type+ " " +Keyword.lower())
        print('--------------------------')
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+LOCATION+"&radius=10500&type="+Type+"&keyword="+Keyword.lower()+"&key="+GOOGLE_API_KEY
        response = urllib.urlopen(url)
        data = json.loads(response.read())

        # iterate over each result pod
        for r in data['results']:

            # check if the restaurant has already been visited
            if r['name'] not in Visited:
                # check if rating exists
                rating =  0
                if ('rating' in r):
                    rating = r['rating']
                # add outlet name to visitied list
                Visited.append(r['name'])
                # print out data (debugging purposes)
                print(" FOUND: " + r['name'])
                # write out restaruant to json file
                fout.write(genResult(r['name'].encode("utf8"),
                                    str(r['geometry']['location']['lng']),
                                    str(r['geometry']['location']['lat']),
                                    str(rating),
                                    str(r['vicinity'].encode("utf8")),
                                    str(Type.encode("utf8")),
                                    str(Keyword.encode("utf8"))))
            # when a duplicate restarant has been found
            # todo: add duplicate keyword to cuisine property of it's respsective outlet
            else:
                print("DUPLICATE:" + r['name'])

fout.write('\n]}\n')
fout.close()




# fin = open('Names.txt', 'r')
# for name in fin:
#     Names.append(name.strip())

# fout = open('restaurant.json', 'w')
# fout.write('{ "Restaurants":[')
# first = True
# for i in range(0, 500):
#     if first:
#         first = False
#         fout.write("\n")
#     else:
#         fout.write(",\n")
#     name = random.choice(Names)
#     corm = random.randint(0,1)
#     restaurant = ""
#     if corm:
#         restaurant = random.choice(Meal)
#     else:
#         restaurant = random.choice(Cuisine)
#         restaurant = restaurant + ' ' + random.choice(Type)
#     diet = [False for i in range(10)]
#     num_diet = random.randint(0, 9)
#     for j in range(0, num_diet):
#         diet[random.randint(0, 9)] = True
#     fout.write(genString(name, restaurant, diet))
# fout.write('\n]}\n')
# fin.close()
# fout.close()






# fout = open('restaurant.json', 'w')
# fout.write('{ "Restaurants":[')




# fout.write('\n]}\n')
# fin.close()
# fout.close()






# Dietary = ["Halal", "Kosher", "Vegan", "Vegetarian",
#            "Lactose intolerant", "Gluten free", "Peanut allergy",
#            "Seafood allergy", "Egg allergy", "Soy allergy"]

# Cuisine = ["American", "Arabian", "Australian", "Chinese", "Eastern European", "French",
#            "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
#            "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Oriental", "Pakistani",
#            "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
#            "Turkish", "Vietnamese"]

# Type = ["Breakfast", "Brunch", "Lunch", "Dinner", "Dessert"]

# Meal = ["BBQ", "Bubble Tea", "Burgers", "Charcoal Chicken",
#         "Coffee", "Drink", "Dumplings", "Fast Food",
#         "Fish and Chips", "Frozen Yogurt",  "Grill", "Healthy Food", "Ice Cream", "Juice",
#         "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Pub Food", "Ramen",
#         "Sandwich", "Seafood", "Soul Food", "Steakhouse", "Sushi Train", "Tapas",
#         "Tea House", "Teppanyaki", "Teriyaki", "Yum Cha"]

# Deals = ["$5 off", "$10 off", "$5 off if you spend over $20", "$10 off if you spend over $50", "Free drink with any meal",
#          "Free drink with any purchase", "Buy one get one free", "All you can eat for $20pp", "All you can eat for $25pp",
#          "10% off", "15% off"]

# Names = []


# def genString(name, restaurant, diet):
#     string = '\t{\n\t\t"name":'
#     if name.endswith('s'):
#         string += '"' + name + "' " + restaurant + '",\n'
#     else:
#         string += '"' + name + "'s " + restaurant + '",\n'


#     string += '\t\t"dietary":[ '
#     first = True
#     for i in range(0, 10):
#         if diet[i]:
#             if not first:
#                 string += ", "
#             first = False
#             string += '"' + Dietary[i] + '"'
#     string += ' ],\n'


#     url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + name + " " + restaurant
#     print "trying: " + url
#     response = urllib.urlopen(url)
#     data = json.loads(response.read())

#     print data["status"]
#     if (data["status"] != "ZERO_RESULTS"):
#         lat = data["results"][0]["geometry"]["location"]["lat"]
#         lng = data["results"][0]["geometry"]["location"]["lng"]
#         string += '\t\t"lng":'+str(lng)+',\n'
#         string += '\t\t"lat":'+str(lat)+',\n'
#         print lat
#         print lng
#     else:
#         # else retry with only name
#         url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + name + " Restaraunt"
#         print "retrying: " + url
#         response = urllib.urlopen(url)
#         data = json.loads(response.read())
#         if (data["status"] == "OK"):
#             lat = data["results"][0]["geometry"]["location"]["lat"]
#             lng = data["results"][0]["geometry"]["location"]["lng"]
#             string += '\t\t"lng":'+str(lng)+',\n'
#             string += '\t\t"lat":'+str(lat)+',\n'
#             print lat
#             print lng


#     dealno = random.randint(0, len(Deals)-1)
#     string += '\t\t"deals":[ "' + Deals[dealno] + '" ],\n'

#     if random.randint(0,1):
#         string += '\t\t"alcohol":"true",\n'
#     else:
#         string += '\t\t"alcohol":"false",\n'
#     if random.randint(0, 1):
#         string += '\t\t"wheelchair":"true",\n'
#     else:
#         string += '\t\t"wheelchair":"false",\n'
#     if random.randint(0, 1):
#         string += '\t\t"wifi":"true"'
#     else:
#         string += '\t\t"wifi":"false"'

#     string += ' }'
#     return string










# fin = open('Names.txt', 'r')
# for name in fin:
#     Names.append(name.strip())

# fout = open('restaurant.json', 'w')
# fout.write('{ "Restaurants":[')
# first = True
# for i in range(0, 500):
#     if first:
#         first = False
#         fout.write("\n")
#     else:
#         fout.write(",\n")
#     name = random.choice(Names)
#     corm = random.randint(0,1)
#     restaurant = ""
#     if corm:
#         restaurant = random.choice(Meal)
#     else:
#         restaurant = random.choice(Cuisine)
#         restaurant = restaurant + ' ' + random.choice(Type)
#     diet = [False for i in range(10)]
#     num_diet = random.randint(0, 9)
#     for j in range(0, num_diet):
#         diet[random.randint(0, 9)] = True
#     fout.write(genString(name, restaurant, diet))
# fout.write('\n]}\n')
# fin.close()
# fout.close()








