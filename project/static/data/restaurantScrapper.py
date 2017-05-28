import random, urllib, json
from Restaurant import *

API_KEYS = ["AIzaSyBgblVJRCXipHa--LqaBsfUYN4KExsA7Rk", "AIzaSyBsbWM_MSeTwsID1vFDXQNi6ksrraaxgmc",
            "AIzaSyBWGb1hoPwvP7w2ZwDhQJty5_wUU2S1Zj0"]
            #"AIzaSyAgEizznGrl4fsrC8Cs_8niV32-TeI17-k", "AIzaSyBtbxbF5dJnKD_hSHPQ_zgbtjzhCtCXiBc"]
LOCATION = "-33.911751,%20151.223290"
Types = ["bar", "bakery", "cafe", "restaurant", "meal_takeaway", "meal_delivery"]
Keywords = ["American", "Arabian", "Australian", "Chinese", "French",
            "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
            "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Pakistani",
            "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
            "Turkish", "Vietnamese", "Breakfast", "Brunch", "Lunch", "Dinner", "Dessert", "BBQ",
            "Burgers", "Charcoal Chicken", "Coffee", "Drink", "Dumplings", "Fast Food",
            "Fish and Chips", "Frozen Yogurt", "Grill", "Ice Cream", "Juice",
            "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Ramen", "Sandwich", "Seafood",
            "Steakhouse", "Sushi", "Tapas", "Teppanyaki", "Teriyaki", "Yum Cha"]
Deals = ["$5 off", "$10 off", "$15 off",
         "$5 off if you spend over $20", "$5 off if you spend over $30", "$10 off if you spend over $50",
         "Free drink with any meal", "Free drink with any purchase", "Free drink if you spend over $10",
         "Buy one get one free", "2 for 1", "Buy two get one free",
         "All you can eat for $20pp", "All you can eat for $25pp", "All you can eat for $30pp",
         "10% off", "15% off", "20% off"]


# List of Restaurant names (used to avoid duplicates)
Visited = []


def genRestaurant(ID, name, postcode, lng, lat, rating, vicinity, _type, cuisines, photos, times):
    if (_type == 'bar') or (_type == 'restaurant'):
        alcohol = True
        byo = True
    else:
        alcohol = random.choice([True, False])
        byo = random.choice([True, False])
    wheelchair = random.choice([True, False])
    wifi = random.choice([True, False])
    pets = random.choice([True, False])
    card = random.choice([True, False])
    music = random.choice([True, False])
    tv = random.choice([True, False])
    parking = random.choice([True, False])

    deals = []
    for i in range(6):
        if random.choice([True, False]):
            deals.append(random.choice(Deals[i*3:i*3+3]))
    return Restaurant(ID, name, postcode, lng, lat, rating, vicinity, _type, cuisines, alcohol, byo,
                      wheelchair, wifi, pets, card, music, tv, parking, photos, times, deals)


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
    result += '\t\t"byo": '+str(r.byo).lower()+',\n'
    result += '\t\t"wheelchair": '+str(r.wheelchair).lower()+',\n'
    result += '\t\t"wifi": '+str(r.wifi).lower()+',\n'
    result += '\t\t"pets": '+str(r.pets).lower()+',\n'
    result += '\t\t"card": '+str(r.card).lower()+',\n'
    result += '\t\t"music": '+str(r.music).lower()+',\n'
    result += '\t\t"tv": '+str(r.tv).lower()+',\n'
    result += '\t\t"parking": '+str(r.parking).lower()+',\n'
    result += '\t\t"photos": '+str(r.photos).replace("'", '"')+',\n'
    result += '\t\t"times": '+str(r.times).replace("'", '"')+',\n'
    result += '\t\t"deals": '+str(r.deals).replace("'", '"')+'\n'
    result += '\t},\n'
    return result


def getPostcode(data):
    if 'result' in data and 'address_components' in data['result']:
        for field in data['result']['address_components']:
            if "postal_code" in field["types"]:
                return field["short_name"]
    return 0


def getPhotos(data):
    arr = []
    if 'result' in data and 'photos' in data['result']:
        for photo in data['result']['photos']:
            arr.append(str(photo['photo_reference'].encode("utf8")))
    return arr


def getOpeningTimes(data):
    times = []
    if 'result' in data and 'opening_hours' in data['result'] and 'weekday_text' in data['result']['opening_hours']:
        for time in data['result']['opening_hours']['weekday_text']:
            times.append(str(time.encode("utf8").replace('\xe2\x80\x93', '-')))
    return times


def getRestaurants():
    restaurants = {}
    ID = 0
    # scan through all the types
    for Type in Types:
        # scan through all the keywords
        for Keyword in Keywords:
            print("searching: " + Type + " " + Keyword.lower())
            print('--------------------------')
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + LOCATION + "&radius=10500&type=" + Type + "&keyword=" + Keyword.lower() + "&key=" + API_KEYS[ID % 3]
            response = urllib.urlopen(url)
            data = json.loads(response.read())
            limit = 0
            # iterate over each result pod
            for r in data['results']:
                if limit > 15:
                    break
                # check if the restaurant has already been visited
                if r['name'] not in Visited:
                    # check if rating exists
                    rating = 0
                    if 'rating' in r:
                        rating = r['rating']
                    # add outlet name to visitied list
                    Visited.append(r['name'])
                    # print out data (debugging purposes)
                    print(" FOUND: " + r['name'])
                    detailsURL = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + r["place_id"] + "&review_summary&key=" + API_KEYS[ID % 3]
                    detailsResponse = urllib.urlopen(detailsURL)
                    detailsData = json.loads(detailsResponse.read())
                    photos = getPhotos(detailsData)
                    times = getOpeningTimes(detailsData)
                    postcode = getPostcode(detailsData)
                    restaurants[r['name']] = genRestaurant(ID, r['name'].encode("utf8"),
                                                           str(postcode),
                                                           str(r['geometry']['location']['lng']),
                                                           str(r['geometry']['location']['lat']),
                                                           str(rating),
                                                           str(r['vicinity'].encode("utf8")),
                                                           str(Type.encode("utf8")),
                                                           [str(Keyword.encode("utf8"))],
                                                           photos, times)
                    ID += 1
                # when a duplicate restarant has been found
                else:
                    curr = restaurants[r['name']]
                    cuisine = str(Keyword.encode("utf8"))
                    if len(curr.cuisines) < 5 and cuisine not in curr.cuisines:
                        restaurants[r['name']].cuisines.append(cuisine)
                limit += 1
    return restaurants


def export(restaurants):
    fout = open('restaurant_new3.json', 'w')
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