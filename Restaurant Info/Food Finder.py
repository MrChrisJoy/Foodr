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
    for r in Restaurants:
        print r.to_string()


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
    if field == "name":
        if left.name < right.name:
            return -1
        elif left.name > right.name:
            return 1
        else:
            return 0
    elif field == "alcohol":
        if left.alcohol < right.alcohol:
            return -1
        elif left.alcohol > right.alcohol:
            return 1
        else:
            return 0
    elif field == "wheelchair":
        if left.wheelchair < right.wheelchair:
            return -1
        elif left.wheelchair > right.wheelchair:
            return 1
        else:
            return 0
    elif field == "wifi":
        if left.wifi < right.wifi:
            return -1
        elif left.wifi > right.wifi:
            return 1
        else:
            return 0

if __name__ == '__main__':
    main()
