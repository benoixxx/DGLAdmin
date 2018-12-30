from django.shortcuts import render, redirect

import requests
import json

from geopy.geocoders import Nominatim

from .models import create_user, create_festival, create_poi, create_artist
from .forms import LoginForm, UserForm, FestivalForm, PoiForm, ArtistForm

google_api_key = "AIzaSyAQTLCdWWBdwA-tlLNd16VwUVabRvr2CrA"

address_users = "http://192.168.128.13:8081/DGLREST_AMPU_COLL_2/users/"
address_admins = "http://192.168.128.13:8081/DGLREST_AMPU_COLL_2/admin"
address_festivals = "http://192.168.128.13:8081/DGLREST_AMPU_COLL_2/festivals/"
address_pois = "http://192.168.128.13:8081/DGLREST_AMPU_COLL_2/pois/"

# address_users = "http://localhost:8080/users/"
# address_admins = "http://localhost:8080/admin"
# address_festivals = "http://localhost:8080/festivals/"
# address_pois = "http://localhost:8080/pois/"

jar = requests.cookies.RequestsCookieJar()


# LOGIN


def home(request):
    # Affichage différent si connecté ou non
    if len(jar) == 0:
        connected = False
    else:
        connected = True

    form = LoginForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        try:
            response = requests.get(address_admins + "?email=" + email + "&" + "password=" + password)
            user = response.json()

            if len(user) is 0:
                error = True
            else:
                jar.set('email', email)
                return redirect('user')

        except requests.exceptions.RequestException:
            error_request = True

    return render(request, 'home.html', locals())


def sign_out(request):
    global jar
    jar.clear()
    return redirect('home')


# USERS


def user(request):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        response = requests.get(address_users)
        users_list = response.json()
    except requests.exceptions.RequestException:
        users_list = []
        error_request = True

    users = []
    for u in users_list:
        user = create_user(u['id'], u['lastName'], u['firstName'], u['email'], u['password'], u['admin'])
        users.append(user)

    return render(request, 'user/user.html', locals())


def add_user(request):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    form = UserForm(request.POST)
    if form.is_valid():
        lastName = form.cleaned_data['lastName']
        firstName = form.cleaned_data['firstName']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        new_user = create_user(0, lastName, firstName, email, password, 0)
        user_json = json.dumps(new_user.__dict__)

        try:
            requests.post(address_users, json=json.loads(user_json))
        except requests.exceptions.RequestException:
            pass

        return redirect('user')

    return render(request, 'user/add_user.html', locals())


def delete_user(request, id):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    requests.delete(address_users + str(id))
    return redirect('user')


def edit_user(request, id):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        response = requests.get(address_users + str(id))
        u = response.json()
        user = create_user(u['id'], u['lastName'], u['firstName'], u['email'], u['password'], u['admin'])
    except requests.exceptions.RequestException:
        redirect('user')

    form = UserForm(request.POST)
    if form.is_valid():
        lastName = form.cleaned_data['lastName']
        firstName = form.cleaned_data['firstName']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        new_user = create_user(0, lastName, firstName, email, password, 0)
        user_json = json.dumps(new_user.__dict__)

        try:
            requests.put(address_users + str(id), json=json.loads(user_json))
        except requests.exceptions.RequestException:
            pass

        return redirect('user')

    return render(request, 'user/edit_user.html', locals())


# FESTIVALS


def festival(request):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        response = requests.get(address_festivals)
        festivals_list = response.json()
    except requests.exceptions.RequestException:
        festivals_list = []
        error_request = True

    festivals = []
    for f in festivals_list:
        fest = create_festival(f['id'], f['name'], f['street'], f['locality'], f['city'], f['region'], f['country'],
                               f['startDate'], f['endDate'], f['email'])
        festivals.append(fest)

    return render(request, 'festival/festival.html', locals())


def add_festival(request):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    form = FestivalForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        street = form.cleaned_data['street']
        locality = form.cleaned_data['locality']
        region = form.cleaned_data['region']
        city = form.cleaned_data['city']
        country = form.cleaned_data['country']
        startDate = form.cleaned_data['startDate']
        endDate = form.cleaned_data['endDate']
        email = form.cleaned_data['email']

        new_festival = create_festival(0, name, street, locality, city, region, country, startDate, endDate, email)
        festival_json = json.dumps(new_festival.__dict__)

        try:
            requests.post(address_festivals, json=json.loads(festival_json))
        except requests.exceptions.RequestException:
            pass

        return redirect('festival')

    return render(request, 'festival/add_festival.html', locals())


def delete_festival(request, id):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        requests.delete(address_festivals + str(id))
    except requests.exceptions.RequestException:
        pass

    return redirect('festival')


def edit_festival(request, id):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        response = requests.get(address_festivals + str(id))
        f = response.json()
        festival = create_festival(f['id'], f['name'], f['street'], f['locality'], f['city'], f['region'], f['country'],
                                   f['startDate'], f['endDate'], f['email'])
    except requests.exceptions.RequestException:
        redirect('festival')

    form = FestivalForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        street = form.cleaned_data['street']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        region = form.cleaned_data['region']
        country = form.cleaned_data['country']
        startDate = form.cleaned_data['startDate']
        endDate = form.cleaned_data['endDate']
        email = form.cleaned_data['email']

        new_festival = create_festival(0, name, street, locality, city, region, country, startDate, endDate, email)
        festival_json = json.dumps(new_festival.__dict__)

        try:
            requests.put(address_festivals + str(id), json=json.loads(festival_json))
        except requests.exceptions.RequestException:
            pass

        return redirect('festival')

    return render(request, 'festival/edit_festival.html', locals())


# POI


def poi(request, id):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        response = requests.get(address_festivals + str(id))
        f = response.json()
        id_festival = f['id']
        name_festival = f['name']

        response = requests.get(address_festivals + str(id) + "/pois")
        poi_list = response.json()
    except requests.exceptions.RequestException:
        redirect('festival')

    stages = []
    pois = []
    number_artists = 0
    for p in poi_list:

        artists = []
        for a in p['artist']:
            number_artists += 1
            artist = create_artist(a['id'], a['name'], a['startDate'], a['endDate'])
            artists.append(artist)

        poi = create_poi(p['id'], p['name'], p['category'], p['latitude'], p['longitude'], f['id'], artists)
        pois.append(poi)

        if poi.category == "Stage":
            stages.append(poi)

    # Code api google map
    code = google_api_key
    # Géo-localisation de la ville
    geo_locator = Nominatim(user_agent="MAP")
    location = geo_locator.geocode(f['city'], timeout=None)
    latitude_festival = location.latitude
    longitude_festival = location.longitude

    # Ajouter un POI
    form = PoiForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        lat = form.cleaned_data['lat']
        long = form.cleaned_data['long']
        category = form.cleaned_data['category']

        new_poi = create_poi(0, name, category, lat, long, id, None)
        poi_json = json.dumps(new_poi.__dict__)

        try:
            requests.put(address_festivals + str(id) + "/pois", json=json.loads(poi_json))
        except requests.exceptions.RequestException:
            pass

        return redirect('poi', id)

    return render(request, 'festival/poi.html', locals())


def delete_poi(request, id_fest, id_poi):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        requests.delete(address_festivals + str(id_fest) + "/pois/" + str(id_poi))
    except requests.exceptions.RequestException:
        redirect('festival')

    return redirect('poi', id_fest)


# ARTISTS


def add_artist(request, id_fest, id_poi):

    try:
        response = requests.get(address_festivals + str(id_fest))
        f = response.json()
        id_festival = id_fest
        name_festival = f['name']

        response = requests.get(address_pois + str(id_poi))
        f = response.json()
        id_poi = id_poi
        name_poi = f['name']
    except requests.exceptions.RequestException:
        redirect('festival')

    # Ajouter un Artiste
    form = ArtistForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        startDate = form.cleaned_data['startDate']
        endDate = form.cleaned_data['endDate']

        new_artist = create_artist(0, name, startDate, endDate)
        artist_json = json.dumps(new_artist.__dict__)

        try:
            requests.put(address_pois + str(id_poi) + "/artists", json=json.loads(artist_json))
        except requests.exceptions.RequestException:
            pass

        return redirect('poi', id_fest)

    return render(request, 'festival/add_artist.html', locals())


def delete_artist(request, id_fest, id_poi, id_artist):
    # Vérifie si connecté ou non
    if len(jar) == 0:
        return redirect('home')

    try:
        requests.delete(address_pois + str(id_poi) + "/artists/" + str(id_artist))
    except requests.exceptions.RequestException:
        redirect('festival')

    return redirect('poi', id_fest)


# ERRORS


def handler404(request):
    return render(request, 'error/404.html', {}, status=404)


def handler500(request):
    return render(request, 'error/500.html', {}, status=500)
