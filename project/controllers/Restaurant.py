class Restaurant:
    def __init__(self, name, lng, lat, rating, vicinity, _type, cuisine, alcohol, wheelchair, wifi):
        self.name = name
        self.cuisine = cuisine
        # long and lat date for seach and images
        self.lng = lng
        self.lat = lat
        self.vicinity = vicinity
        self.rating = rating
        self.cuisine = cuisine

        self.type = _type
        self.alcohol = alcohol
        self.wheelchair = wheelchair
        self.wifi = wifi