import re

class Restaurant:
    def __init__(self, name, dietary, alcohol, wheelchair, wifi):
        self.name = name
        self.dietary = dietary
        if alcohol == "True":
            self.alcohol = True
        else:
            self.alcohol = False
        if wheelchair == "True":
            self.wheelchair = True
        else:
            self.wheelchair = False
        if wifi == "True":
            self.wifi = True
        else:
            self.wifi = False

    def get_field(self, field):
        if field == "name":
            return self.name
        if field == "dietary":
            return self.dietary
        if field == "alcohol":
            return self.alcohol
        if field == "wheelchair":
            return self.wheelchair
        if field == "wifi":
            return self.wifi

    def to_string(self):
        return "name: %s, dietary: %s, alcohol: %s, wheel: %s, wifi: %s" % (self.name, self.dietary, self.alcohol, self.wheelchair, self.wifi)

Restaurants = []

def main():

    with open("restaurant.txt", "r") as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            find = re.findall(r"<[\w,' ]*>", line)
            name = find[0].strip("<").strip(">")
            dietary = find[1].strip("<").strip(">")
            alcohol = find[2].strip("<").strip(">")
            wheelchair = find[3].strip("<").strip(">")
            wifi = find[4].strip("<").strip(">")
            new = Restaurant(name, dietary.split(', '), alcohol, wheelchair, wifi)
            Restaurants.append(new)
    bubble_sort("Ascending", "name")
    filtered = filter_diet(["Vegetarian", "Vegan", "Halal"])
    for f in filtered:
        print f.to_string()


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
