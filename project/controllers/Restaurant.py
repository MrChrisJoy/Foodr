class Restaurant:
    def __init__(self, ID, name, postcode, lng, lat, rating, vicinity, _type, cuisines, alcohol, byo,
                 wheelchair, wifi, pets, card, music, tv, parking, photos, times, deals):
        self.id = ID
        self.name = name
        self.postcode = postcode
        self.lng = lng
        self.lat = lat
        self.vicinity = vicinity
        self.rating = rating
        self.cuisines = cuisines
        self.type = _type
        self.alcohol = alcohol
        self.byo = byo
        self.wheelchair = wheelchair
        self.wifi = wifi
        self.pets = pets
        self.card = card
        self.music = music
        self.tv = tv
        self.parking = parking
        self.photos = photos
        self.times = times
        self.deals = deals

    def toString(self, field):
        var = self.getField(field)
        if field in ["deals", "cuisines"]:
            return ", ".join(var)
        if field == "times":
            return ",\n".join(var)
        return var

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
        if field == "byo":
            return self.byo
        if field == "wheelchair":
            return self.wheelchair
        if field == "wifi":
            return self.wifi
        if field == "pets":
            return self.pets
        if field == "card":
            return self.card
        if field == "music":
            return self.music
        if field == "tv":
            return self.tv
        if field == "parking":
            return self.parking
        if field == "deals":
            return self.deals
        if field == "photos":
            return self.photos
        if field == "times":
            return self.times
