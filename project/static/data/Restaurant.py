class Restaurant:
    def __init__(self, ID, name, postcode, lng, lat, rating, vicinity, _type, cuisines, alcohol, wheelchair, wifi, deals):
        self.ID = ID
        self.name = name
        # long and lat date for seach and images
        self.postcode = postcode
        self.lng = lng
        self.lat = lat
        self.vicinity = vicinity
        self.rating = rating
        self.cuisines = cuisines
        self.type = _type
        self.alcohol = alcohol
        self.wheelchair = wheelchair
        self.wifi = wifi
        self.deals = deals
