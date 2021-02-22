# from rest_framework import viewsets
# from app.serializers import UserSerializer, GroupSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
import packets.apis.apimongo as db
from packets.configuration.mongo import MONGO_DB, MONGO_COLLECTION
from packets.forms import LoginForm, SignupForm
from datetime import datetime, timedelta
import packets.code.helper as helper
import packets.code.protocol_info.protocol_info as pi
import packets.code.stats.plot as sp
import logging

logger = logging.getLogger(__name__)

def user_login(request):

    nextredir = ""

    if request.GET:
        nextredir = request.GET['next']

    if request.POST:
        # Process the request if posted data are available
        username = request.POST['username']
        password = request.POST['password']
        # Check username and password combination if correct
        user = authenticate(username=username, password=password)
        if user is not None:
            # Save session as cookie to login the user
            login(request, user)
            # Success, now let's login the user.
            if (nextredir == ""):
                return redirect('index')
            else:
                return redirect(nextredir)
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'packets/login.html', {'error_message': 'Incorrect username and/ or password.'})
    else:
        # No post data availabe, let's just show the page to the user.
        context={
            'nextredir' : nextredir,
        }
        return render(request, 'packets/login.html', context)

def logout_view(request):

    logout(request)
    return render(request, 'packets/index.html')

# Mostrar lista de protocolos
# Contar paquetes de cada lista de protoclos
# Enlace ao ao análisis
# Recurso /environment/env_name/mac
@login_required
def mac(request, env, mac):
    context = None

    oldest_timestamp = db.get_oldest_mac_packet(MONGO_DB, MONGO_COLLECTION, env, mac)
    if (oldest_timestamp):
        oldest_timestamp = oldest_timestamp.strftime('%Y-%m-%dT%H:%M')
    newest_timestamp = db.get_newest_mac_packet(MONGO_DB, MONGO_COLLECTION, env, mac)
    if (newest_timestamp):
        newest_timestamp += timedelta(minutes=1)
        newest_timestamp = newest_timestamp.strftime('%Y-%m-%dT%H:%M')

    inidate = oldest_timestamp
    enddate = newest_timestamp

    dates = helper.get_date_interval(request.GET)
    if (dates):
        inidate = dates["inidate"]
        enddate = dates["enddate"]

    protos = db.get_protocol_list(MONGO_DB, MONGO_COLLECTION, env, inidate, enddate)
    proto_list = []
    protocol_info = {}

    for proto in protos:
        proto_data = {}
        proto_data["name"] = proto
        proto_data["num"] = db.count_protocol_mac_packets(MONGO_DB, MONGO_COLLECTION, env, mac, proto, inidate, enddate)
        protocol_info[proto] = pi.get_protocol_info(mac, proto, env, inidate, enddate)
        template = "packets/proto_mac_info/"+proto+".html"
        if (helper.template_exists(template)):
            protocol_info[proto]["template"] = template
        if (proto_data["num"] != 0):
            proto_list.append(proto_data)


    context={
        'user' : request.user,
        'env' : env,
        'mac' : mac,
        'proto_list' : proto_list,
        'protocol_info' : protocol_info,
        'oldest_timestamp' : oldest_timestamp,
        'newest_timestamp' : newest_timestamp,
        'inidate' : inidate,
        'enddate' : enddate,
    }

    return render(request, 'packets/mac.html', context)

# Mostrar lista de macs
# Contar paquetes de cada lista de protoclos
# Enlace ao ao análisis
# Recurso /environment/env_name/protocol/nomeprotocolo
@login_required
def protocol(request, env, protocol):
    context = None

    oldest_timestamp = db.get_oldest_protocol_packet(MONGO_DB, MONGO_COLLECTION, env, protocol)
    if (oldest_timestamp):
        oldest_timestamp = oldest_timestamp.strftime('%Y-%m-%dT%H:%M')
    newest_timestamp = db.get_newest_protocol_packet(MONGO_DB, MONGO_COLLECTION, env, protocol)
    if (newest_timestamp):
        newest_timestamp += timedelta(minutes=1)
        newest_timestamp = newest_timestamp.strftime('%Y-%m-%dT%H:%M')

    inidate = oldest_timestamp
    enddate = newest_timestamp

    dates = helper.get_date_interval(request.GET)
    if (dates):
        inidate = dates["inidate"]
        enddate = dates["enddate"]

    macs = db.get_mac_list(MONGO_DB, MONGO_COLLECTION, env, inidate, enddate)
    mac_list = []

    for mac in macs:
        mac_data = {}
        mac_data["name"] = mac
        mac_data["num"] = db.count_protocol_mac_packets(MONGO_DB, MONGO_COLLECTION, env, mac, protocol, inidate, enddate)
        mac_data["manufacturer"] = db.get_mac_manufacturer(MONGO_DB, MONGO_COLLECTION, env, mac, inidate, enddate)
        protocol_info = pi.get_protocol_info(mac, protocol, env, inidate, enddate)
        if (mac_data["num"] != 0):
            mac_list.append(mac_data)

    context={
        'user' : request.user,
        'env' : env,
        'protocol' : protocol,
        'mac_list': mac_list,
        'oldest_timestamp': oldest_timestamp,
        'newest_timestamp': newest_timestamp,
        'inidate': inidate,
        'enddate': enddate,
    }
    template = "packets/proto_info/"+protocol+".html"
    if (not helper.template_exists(template)):
        template = "packets/proto_info/NOPROTO.html"

    return render(request, template, context)

# Mostrar lista de paquetes
# Recurso /environment/env_name/mac/nomemac/protocol/nomeprotocolo
@login_required
def packets(request, env, mac, protocol):

    context = None

    oldest_timestamp = db.get_oldest_protocol_mac_packet(MONGO_DB, MONGO_COLLECTION, env, protocol, mac)
    if (oldest_timestamp):
        oldest_timestamp = oldest_timestamp.strftime('%Y-%m-%dT%H:%M')
    newest_timestamp = db.get_newest_protocol_mac_packet(MONGO_DB, MONGO_COLLECTION, env, protocol, mac)
    if (newest_timestamp):
        newest_timestamp += timedelta(minutes=1)
        newest_timestamp = newest_timestamp.strftime('%Y-%m-%dT%H:%M')

    inidate = oldest_timestamp
    enddate = newest_timestamp

    dates = helper.get_date_interval(request.GET)
    if (dates):
        inidate = dates["inidate"]
        enddate = dates["enddate"]

    page_number = helper.get_page(request.GET)
    if (not page_number):
        page_number = 1


    mac_protocol_packets = db.get_mac_protocol_packets(MONGO_DB, MONGO_COLLECTION, env, mac, protocol, inidate, enddate)
    mac_protocol_packets = db.mongo_cursor_to_list(mac_protocol_packets)

    # IMPORTANT Needs to be only one packet per page
    paginatedpackets = Paginator(mac_protocol_packets, 1)
    page_obj = paginatedpackets.page(page_number)
    packet = page_obj[0]
    timestamp = packet["timestamp"]
    datetimeObj = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    timestamp = datetimeObj.strftime('%H:%M:%S on %A, %B the %dth, %Y')

    keys = list(packet.keys())
    keys.remove("_id")
    keys.remove("protocol")
    keys.remove("environment")
    keys.remove("timestamp")
    keys.remove("mac")

    transformed_packet = {}
    transformed_packet["claves"] = {}
    transformed_packet["valores"] = {}
    for layer in keys:
        claves = []
        valores = []
        for field in packet[layer]:
            claves.append(field)
            valores.append(packet[layer][field])
        transformed_packet["claves"][layer] = claves
        transformed_packet["valores"][layer] = valores

    protocol_info = {}
    protocol_info[protocol] = pi.get_protocol_info(mac, protocol, env, inidate, enddate)
    template = "packets/proto_mac_info/"+protocol+".html"
    if (helper.template_exists(template)):
        protocol_info[protocol]["template"] = template

    context={
        'user' : request.user,
        'env' : env,
        'mac' : mac,
        'protocol' : protocol,
        'timestamp' : timestamp,
        'page_obj' : page_obj,
        'layers' : keys,
        'packet' : transformed_packet,
        'protocol_info' : protocol_info,
        'oldest_timestamp' : oldest_timestamp,
        'newest_timestamp' : newest_timestamp,
        'inidate' : inidate,
        'enddate' : enddate,
    }

    template = "packets/packets.html"

    return render(request,template, context)

# Recurso /environment/env_name/stats
@login_required
def stats(request, env):
    context = None
    nextdate = None
    prevdate = None
    dailystats = True

    oldest_timestamp = db.get_oldest_env_packet(MONGO_DB, MONGO_COLLECTION, env)
    if (oldest_timestamp):
        oldest_timestamp = oldest_timestamp.strftime('%Y-%m-%d')
    newest_timestamp = db.get_newest_env_packet(MONGO_DB, MONGO_COLLECTION, env)
    if (newest_timestamp):
        newest_timestamp = newest_timestamp.strftime('%Y-%m-%d')

    statsday = oldest_timestamp

    inidate = oldest_timestamp
    enddate = newest_timestamp
    dates = helper.get_day(request.GET)
    if (dates):
        inidate = dates["ini"]
        enddate = dates["end"]
        statsday = inidate

    env_num = db.count_env_packets(MONGO_DB, MONGO_COLLECTION, env, inidate, enddate)

    nextpacket = db.get_next_env_packet(MONGO_DB, MONGO_COLLECTION, env, enddate)
    if (nextpacket != None):
        nextdatestr = datetime.strptime(nextpacket["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        nextdate = nextdatestr.strftime('%Y-%m-%d')

    prevpacket = db.get_prev_env_packet(MONGO_DB, MONGO_COLLECTION, env, inidate)
    if (prevpacket != None):
        prevdatestr = datetime.strptime(prevpacket["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        prevdate = prevdatestr.strftime('%Y-%m-%d')

    base64fig = sp.plotdataenv(env, statsday)

    context={
        'user' : request.user,
        'env' : env,
        'env_num' : env_num,
        'figure' : base64fig,
        'dailystats' : dailystats,
        'day' : statsday,
        'nextdate' : nextdate,
        'prevdate' : prevdate,
        'oldest_timestamp' : oldest_timestamp,
        'newest_timestamp' : newest_timestamp,
    }

    return render(request, 'packets/stats.html', context)

# Recurso /environment/env_name/stats
@login_required
def stats_mac(request, env, mac):
    context = None
    nextdate = None
    prevdate = None
    dailystats = True

    oldest_timestamp = db.get_oldest_mac_packet(MONGO_DB, MONGO_COLLECTION, env, mac)
    if (oldest_timestamp):
        oldest_timestamp = oldest_timestamp.strftime('%Y-%m-%d')
    newest_timestamp = db.get_newest_mac_packet(MONGO_DB, MONGO_COLLECTION, env, mac)
    if (newest_timestamp):
        newest_timestamp = newest_timestamp.strftime('%Y-%m-%d')

    statsday = oldest_timestamp

    inidate = oldest_timestamp
    enddate = newest_timestamp
    dates = helper.get_day(request.GET)
    if (dates):
        inidate = dates["ini"]
        enddate = dates["end"]
        statsday = inidate

    env_num = db.count_mac_packets(MONGO_DB, MONGO_COLLECTION, env, mac, inidate, enddate)

    nextpacket = db.get_next_mac_packet(MONGO_DB, MONGO_COLLECTION, env, mac, enddate)
    if (nextpacket != None):
        nextdatestr = datetime.strptime(nextpacket["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        nextdate = nextdatestr.strftime('%Y-%m-%d')

    prevpacket = db.get_prev_mac_packet(MONGO_DB, MONGO_COLLECTION, env, mac, inidate)
    if (prevpacket != None):
        prevdatestr = datetime.strptime(prevpacket["timestamp"], '%Y-%m-%dT%H:%M:%S.%f')
        prevdate = prevdatestr.strftime('%Y-%m-%d')

    base64fig = sp.plotdatamac(env, mac, statsday)

    context={
        'user' : request.user,
        'env' : env,
        'env_num' : env_num,
        'figure' : base64fig,
        'dailystats' : dailystats,
        'day' : statsday,
        'nextdate' : nextdate,
        'prevdate' : prevdate,
        'oldest_timestamp' : oldest_timestamp,
        'newest_timestamp' : newest_timestamp,
    }

    return render(request, 'packets/stats.html', context)

# Mostrar lista de entornos
# Contar paquetes de cada lista de entornos
# Enlace ao entorno
# Recurso /environment/env_name
@login_required
def index(request):

    context = None

    oldest_timestamp = db.get_oldest_packet(MONGO_DB, MONGO_COLLECTION)
    if (oldest_timestamp):
        oldest_timestamp = oldest_timestamp.strftime('%Y-%m-%dT%H:%M')
    newest_timestamp = db.get_newest_packet(MONGO_DB, MONGO_COLLECTION)
    if (newest_timestamp):
        newest_timestamp += timedelta(minutes=1)
        newest_timestamp = newest_timestamp.strftime('%Y-%m-%dT%H:%M')

    inidate = oldest_timestamp
    enddate = newest_timestamp

    dates = helper.get_date_interval(request.GET)
    if (dates):
        inidate = dates["inidate"]
        enddate = dates["enddate"]

    env_list = []
    envs = db.get_env_list(MONGO_DB, MONGO_COLLECTION)
    for env in envs:
        env_data = {}
        env_data["name"] = env
        num = db.count_env_packets(MONGO_DB, MONGO_COLLECTION, env, inidate, enddate)
        env_data["num"] = num
        env_list.append(env_data)



    context={
        'user' : request.user,
        'env_list' : env_list,
        'oldest_timestamp' : oldest_timestamp,
        'newest_timestamp' : newest_timestamp,
        'inidate' : inidate,
        'enddate' : enddate,
    }

    return render(request, 'packets/index.html', context)

# Obter packetes do entorno
# Obter listado de protocolos e número
# Obter listado de macs e número
@login_required
def environment(request, env):


    context = None

    oldest_timestamp = db.get_oldest_env_packet(MONGO_DB, MONGO_COLLECTION, env)
    if (oldest_timestamp):
        oldest_timestamp = oldest_timestamp.strftime('%Y-%m-%dT%H:%M')
    newest_timestamp = db.get_newest_env_packet(MONGO_DB, MONGO_COLLECTION, env)
    if (newest_timestamp):
        newest_timestamp += timedelta(minutes=1)
        newest_timestamp = newest_timestamp.strftime('%Y-%m-%dT%H:%M')

    inidate = oldest_timestamp
    enddate = newest_timestamp

    dates = helper.get_date_interval(request.GET)
    if (dates):
        inidate = dates["inidate"]
        enddate = dates["enddate"]

    env_num = db.count_env_packets(MONGO_DB, MONGO_COLLECTION, env, inidate, enddate)

    protos = db.get_protocol_list(MONGO_DB, MONGO_COLLECTION, env, inidate, enddate)
    macs = db.get_mac_list(MONGO_DB, MONGO_COLLECTION, env, inidate, enddate)


    proto_list = []
    for proto in protos:
        proto_data = {}
        proto_num = db.count_protocol_packets(MONGO_DB, MONGO_COLLECTION, env, proto, inidate, enddate)
        proto_data["name"] = proto
        proto_data["num"] = proto_num
        proto_list.append(proto_data)

    mac_ipv4 = 0
    mac_ipv6 = 0
    mac_noip = 0
    mac_total = len(macs)


    mac_list = []
    for mac in macs:
        mac_data = {}
        mac_num = db.count_mac_packets(MONGO_DB, MONGO_COLLECTION, env, mac, inidate, enddate)
        mac_data["name"] = mac
        mac_data["num"] = mac_num
        mac_data["manufacturer"] = db.get_mac_manufacturer(MONGO_DB, MONGO_COLLECTION, env, mac, inidate, enddate)

        hasip = db.has_layer(MONGO_DB, MONGO_COLLECTION, env, mac, "ip", inidate, enddate)
        hasipv6 = db.has_layer(MONGO_DB, MONGO_COLLECTION, env, mac, "ipv6", inidate, enddate)
        if (hasip):
            mac_ipv4 += 1
            mac_data["ipv4"] = True
            mac_data["noip"] = False
        if (hasipv6):
            mac_ipv6 += 1
            mac_data["ipv6"] = True
        if (not hasip and not hasipv6):
            mac_noip += 1
            mac_data["noip"] = True

        mac_list.append(mac_data)

    # Obter numero de ipv4
    num_ipv4 = db.count_layer_packets(MONGO_DB, MONGO_COLLECTION, env, "ip", inidate, enddate)
    # Obter numero de ipv6
    num_ipv6 = db.count_layer_packets(MONGO_DB, MONGO_COLLECTION, env, "ipv6", inidate, enddate)
    # Obter numero de noip
    num_noip = env_num - num_ipv4 - num_ipv6


    context = {
        'user' :request.user,
        'env' : env,
        'env_num': env_num,
        'proto_list': proto_list,
        'mac_list': mac_list,
        'num_ipv4': num_ipv4,
        'num_ipv6': num_ipv6,
        'num_noip': num_noip,
        'mac_ipv4': mac_ipv4,
        'mac_ipv6': mac_ipv6,
        'mac_noip': mac_noip,
        'mac_total': mac_total,
        'newest_timestamp': newest_timestamp,
        'oldest_timestamp': oldest_timestamp,
        'inidate': inidate,
        'enddate': enddate,
    }

    return render(request, 'packets/environment.html', context)
