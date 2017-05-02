import random

Dietary = ["Halal", "Kosher", "Vegan", "Vegetarian",
           "Lactose intolerant", "Gluten free", "Peanut allergy",
           "Seafood allergy", "Egg allergy", "Soy allergy"]

Cuisine = ["American", "Arabian", "Australian", "Chinese", "Eastern European", "French",
           "Greek", "Indian", "Italian", "Japanese", "Korean", "Lebanese", "Malaysian",
           "Middle eastern", "Mediterranean", "Mexican", "Moroccan", "Oriental", "Pakistani",
           "Portuguese", "Scandinavian", "Singaporean", "Spanish", "Sri Lankan", "Thai",
           "Turkish", "Vietnamese"]

Type = ["Breakfast", "Brunch", "Lunch", "Dinner", "Dessert"]

Meal = ["BBQ", "Bubble Tea", "Burgers", "Charcoal Chicken",
        "Coffee", "Drink", "Dumplings", "Fast Food",
        "Fish and Chips", "Frozen Yogurt",  "Grill", "Healthy Food", "Ice Cream", "Juice",
        "Kebabs", "Noodles", "Pastry", "Pho", "Pizza", "Pub Food", "Ramen",
        "Sandwich", "Seafood", "Soul Food", "Steakhouse", "Sushi Train", "Tapas",
        "Tea House", "Teppanyaki", "Teriyaki", "Yum Cha"]

Names = []


def genString(name, restaurant, diet):
    if name.endswith('s'):
        string = '<' + name + "' " + restaurant + '> '
    else:
        string = '<' + name + "'s " + restaurant + '> '
    string += '<'
    first = True
    for i in range(0, 10):
        if diet[i]:
            if not first:
                string += ", "
            first = False
            string += Dietary[i]
    string += '> '
    if random.randint(0,1):
        string += '<True> '
    else:
        string += '<False> '
    if random.randint(0, 1):
        string += '<True> '
    else:
        string += '<False> '
    if random.randint(0, 1):
        string += '<True>'
    else:
        string += '<False>'

    string += '\n'
    return string

fin = open('Names.txt', 'r')
for name in fin:
    Names.append(name.strip())

fout = open('restaurant.txt', 'w')
fout.write("# <Name> <Dietary> <Alcohol> <Wheelchair_Access> <Free_WiFi>\n")
for i in range(0, 1000):
    name = random.choice(Names)
    corm = random.randint(0,1)
    restaurant = ""
    if corm:
        restaurant = random.choice(Meal)
    else:
        restaurant = random.choice(Cuisine)
        restaurant = restaurant + ' ' + random.choice(Type)
    diet = [False for i in range(10)]
    num_diet = random.randint(0, 9)
    for j in range(0, num_diet):
        diet[random.randint(0, 9)] = True
    fout.write(genString(name, restaurant, diet))

fin.close()
fout.close()
