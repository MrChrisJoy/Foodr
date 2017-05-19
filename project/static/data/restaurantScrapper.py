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