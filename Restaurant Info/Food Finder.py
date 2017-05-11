import json

class Restaurant:
    def __init__(self, name, dietary, deals, alcohol, wheelchair, wifi):
        self.name = name
        self.dietary = dietary
        self.deals = deals
        if alcohol == "true":
            self.alcohol = True
        else:
            self.alcohol = False
        if wheelchair == "true":
            self.wheelchair = True
        else:
            self.wheelchair = False
        if wifi == "true":
            self.wifi = True
        else:
            self.wifi = False

    def get_field(self, field):
        if field == "name":
            return self.name
        if field == "dietary":
            return self.dietary
        if field == "deals":
            return self.deals
        if field == "alcohol":
            return self.alcohol
        if field == "wheelchair":
            return self.wheelchair
        if field == "wifi":
            return self.wifi

    def to_string(self):
        return "name: %s, dietary: %s, deals: %s, alcohol: %s, wheel: %s, wifi: %s" % (self.name, self.dietary, self.deals, self.alcohol, self.wheelchair, self.wifi)

Restaurants = []


def main():

    with open("restaurant.json") as f:
        lines = json.load(f)
        testArr = lines["Restaurants"]
        for r in testArr:
            Restaurants.append(Restaurant(str(r["name"]), str(" ".join(r["dietary"])).split(" "), str(" ".join(r["deals"])).split(','), str(r["alcohol"]), str(r["wheelchair"]), str(r["wifi"])))
    bubble_sort("Ascending", "name")
    f = filter_diet(["Halal", "Vegan", "Kosher"])
    for r in f:
        print r.to_string()


def filter_diet(arg):
    # arg is an array containing the dietary requirements to match
    filtered = []
    for r in Restaurants:
        match = True
        for req in arg:
            if req not in r.dietary:
                match = False
                break
        if match:
            filtered.append(r)
    return filtered


def bubble_sort(direction, field):
    for i in range(len(Restaurants)):
        swapped = False
        for j in range(1, len(Restaurants)):
            comp = compare(Restaurants[i], Restaurants[j], field)
            if (direction == "Descending" and comp > 0) or (direction == "Ascending" and comp < 0):
                Restaurants[i], Restaurants[j] = Restaurants[j], Restaurants[i]
                swapped = True
        if not swapped:
            return


def compare(left, right, field):
    if left.get_field(field) < right.get_field(field):
        return -1
    elif left.get_field(field) > right.get_field(field):
        return 1
    else:
        return 0


if __name__ == '__main__':
    main()
