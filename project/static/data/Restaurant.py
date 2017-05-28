class Restaurant:
    def __init__(self, ID, name, postcode, lng, lat, rating, vicinity, _type, cuisines, alcohol, wheelchair, wifi, deals):
        self.id = ID
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

    def getField(self, field):
        if field == "id":
            return self.id
        if field == "name":
            return self.name
        if field == "postcode":
            return self.postcode
        if field == "lng":
            return self.lng
        if field == "lat":
            return self.lat
        if field == "vicinity":
            return self.vicinity
        if field == "rating":
            return self.rating
        if field == "cuisines":
            return self.cuisines
        if field == "type":
            return self.type
        if field == "alcohol":
            return self.alcohol
        if field == "wheelchair":
            return self.wheelchair
        if field == "wifi":
            return self.wifi
        if field == "deals":
            return self.deals