class User(object):
    id = int
    lastName = str
    firstName = str
    email = str
    password = str
    admin = int

    def __init__(self, id, lastName, firstName, email, password, admin):
        self.id = id
        self.lastName = lastName
        self.firstName = firstName
        self.email = email
        self.password = password
        self.admin = admin


def create_user(id, lastName, firstName, email, password, admin):
    person = User(id, lastName, firstName, email, password, admin)
    return person


class Festival(object):
    id = int
    name = str
    street = str
    locality = str
    city = str
    region = str
    country = str
    startDate = str
    endDate = str
    email = str

    def __init__(self, id, name, street, locality, city, region, country, startDate, endDate, email):
        self.id = id
        self.name = name
        self.street = street
        self.locality = locality
        self.city = city
        self.region = region
        self.country = country
        self.startDate = startDate
        self.endDate = endDate
        self.email = email


def create_festival(id, name, street, locality, region, city, country, startDate, endDate, email):
    festival = Festival(id, name, street, locality, region, city, country, startDate, endDate, email)
    return festival


class POI(object):
    id = int
    name = str
    category = str
    latitude = int
    longitude = int
    id_festival = int
    artist = []

    def __init__(self, id, name, category, latitude, longitude, id_festival, artist):
        self.id = id
        self.name = name
        self.category = category
        self.latitude = latitude
        self.longitude = longitude
        self.id_festival = id_festival
        self.artist = artist


def create_poi(id, name, category, latitude, longitude, id_festival, artist):
    poi = POI(id, name, category, latitude, longitude, id_festival, artist)
    return poi


class Artist(object):
    id = int
    name = str
    startDate = str
    endDate = str

    def __init__(self, id, name, startDate, endDate):
        self.id = id
        self.name = name
        self.startDate = startDate
        self.endDate = endDate


def create_artist(id, name, startDate, endDate):
    artist = Artist(id, name, startDate, endDate)
    return artist

