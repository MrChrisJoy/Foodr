import random, urllib, json
from Restaurant import *

RAYCOLE_GOOGLE_API_KEY = "AIzaSyD4qoVPYOVCFOe-x_8mNGNU8uWka9ygPFw"
GOOGLE_API_KEY = "AIzaSyAR83M4SW2PeTdIOy4PV54Uwnj403hUJIM"
GOOGLE_API_KEY2 = "AIzaSyAYiPQqi9bJTIRsqfkkukGTc2YkV2DSQpo"
LOCATION = "-33.911751,%20151.223290"
Types = ["bar", "bakery", "cafe", "restaurant", "meal_takeaway", "meal_delivery"]
Keywords = ["American", "Arabian", "Australian", "Chinese", "French",
            "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
            "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Oriental", "Pakistani",
            "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
            "Vietnamese", "Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "BBQ",
            "Bubble Tea", "Burgers", "Charcoal Chicken", "Coffee", "Drink", "Dumplings", "Fast Food",
            "Fish and Chips", "Frozen Yogurt",  "Grill", "Ice Cream", "Juice",
            "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Pub Food", "Ramen", "Sandwich", "Seafood",
            "Steakhouse", "Sushi", "Tapas", "Tea House", "Teppanyaki", "Teriyaki", "Yum Cha"]
Deals = ["$5 off", "$10 off", "$15 off",
         "$5 off if you spend over $20", "$5 off if you spend over $30", "$10 off if you spend over $50",
         "Free drink with any meal", "Free drink with any purchase", "Free drink if you spend over $10",
         "Buy one get one free", "2 for 1", "Buy two get one free",
         "All you can eat for $20pp", "All you can eat for $25pp", "All you can eat for $30pp",
         "10% off", "15% off", "20% off"]


# List of Restaruant names (used to avoid duplicates)
Visited = []


def genRestaurant(ID, name, postcode, lng, lat, rating, vicinity, _type, cuisines):
    if (_type == 'bar') or (_type == 'restaurant'):
        alcohol = True
    else:
        alcohol = random.choice([True, False])
    wheelchair = random.choice([True, False])
    wifi = random.choice([True, False])
    deals = []
    for i in range(5):
        if random.choice([True, False]):
            deals.append(random.choice(Deals[i*3:i*3+2]))
    return Restaurant(ID, name, postcode, lng, lat, rating, vicinity, _type, cuisines, alcohol, wheelchair, wifi, deals)


def writeRestaurant(r):
    result = '\t{\n'
    result += '\t\t"id": ' + str(r.id) + ',\n'
    result += '\t\t"name": "' + r.name + '",\n'
    result += '\t\t"postcode": '+r.postcode+',\n'
    result += '\t\t"lng": '+r.lng+',\n'
    result += '\t\t"lat": '+r.lat+',\n'
    result += '\t\t"rating": '+r.rating+',\n'
    result += '\t\t"vicinity": "'+r.vicinity+'",\n'
    result += '\t\t"type": "'+r.type+'",\n'
    result += '\t\t"cuisines": '+str(r.cuisines).replace("'", '"')+',\n'
    result += '\t\t"alcohol": '+str(r.alcohol).lower()+',\n'
    result += '\t\t"wheelchair": '+str(r.wheelchair).lower()+',\n'
    result += '\t\t"wifi": '+str(r.wifi).lower()+',\n'
    result += '\t\t"deals": '+str(r.deals).replace("'", '"')+'\n'
    result += '\t},\n'
    return result


def getPostcode(name):

    url = "https://maps.googleapis.com/maps/api/geocode/json?key=" + GOOGLE_API_KEY2 + "&address=" + name
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    results = data['results']
    #print results
    #if u'address_components' in results and data[u'status'] == 'OK':
    for key in results:
        for f in key["address_components"]:
            if "postal_code" in f["types"]:
                return f["short_name"]
    # for f in results[u'address_components']:
    #     if u"postal_code" in f[u'types']:
    #         return f[u"short_name"].encode("utf8")
    return 0

def getRestaurants():
    restaurants = {}
    ID = 0
    # scan through all the types
    for Type in Types:
        # scan through all the keywords
        for Keyword in Keywords:
            print("searching: " + Type + " " + Keyword.lower())
            print('--------------------------')
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + LOCATION + "&radius=10500&type=" + Type + "&keyword=" + Keyword.lower() + "&key=" + GOOGLE_API_KEY2
            response = urllib.urlopen(url)
            data = json.loads(response.read())

            # iterate over each result pod
            for r in data['results']:

                # check if the restaurant has already been visited
                if r['name'] not in Visited:
                    # check if rating exists
                    rating = 0
                    if 'rating' in r:
                        rating = r['rating']
                    # add outlet name to visitied list
                    Visited.append(r['name'])
                    # print out data (debugging purposes)
                    #print(" FOUND: " + r['name'])
                    # write out restaruant to json file
                    postcode = getPostcode(str(r['geometry']['location']['lat']) + ' ' + str(r['geometry']['location']['lng']))
                    #print postcode
                    restaurants[r['name']] = genRestaurant(ID, r['name'].encode("utf8"),
                                                           str(postcode),
                                                           str(r['geometry']['location']['lng']),
                                                           str(r['geometry']['location']['lat']),
                                                           str(rating),
                                                           str(r['vicinity'].encode("utf8")),
                                                           str(Type.encode("utf8")),
                                                           [str(Keyword.encode("utf8"))])
                    ID += 1
                # when a duplicate restarant has been found
                # todo: add duplicate keyword to cuisine property of it's respsective outlet
                else:
                    curr = restaurants[r['name']]
                    cuisine = str(Keyword.encode("utf8"))
                    if len(curr.cuisines) < 5 and cuisine not in curr.cuisines:
                        restaurants[r['name']].cuisines.append(cuisine)
                    #print("DUPLICATE:" + r['name'])
    return restaurants


def export(restaurants):
    fout = open('restaurant.json', 'w')
    fout.write('{ "Restaurants":[')
    for r in restaurants.keys():
        fout.write(writeRestaurant(restaurants[r]))
    fout.write('\n]}\n')
    fout.close()


def main():
    restaurants = getRestaurants()
    export(restaurants)


if __name__ == "__main__":
    main()
