import matplotlib.pyplot as plt
import urllib, base64
import io
import packets.apis.apimongo as db
from packets.configuration.mongo import MONGO_DB, MONGO_COLLECTION
from datetime import datetime, timedelta



# Recibe: json con estadisticas de paquetes de cada tipo
# Devolve: Impresión nunha gráfica do número de cada paquete
def plotdataenv(env, inidate):
    labels = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

    inidate = datetime.strptime(inidate, "%Y-%m-%d")
    enddate = inidate + timedelta(hours=1)

    counts = []
    hour = 0
    while hour<24:
        inidatestr = inidate.strftime('%Y-%m-%dT%H:%M.%f')
        enddatestr = enddate.strftime('%Y-%m-%dT%H:%M.%f')
        counts.append((db.count_env_packets(MONGO_DB, MONGO_COLLECTION, env, inidatestr, enddatestr)))
        inidate += timedelta(hours=1)
        enddate += timedelta(hours=1)
        hour +=1

    fig, ax = plt.subplots()
    ax.bar(labels, counts, label='Num packets')
    ax.set_ylabel('Num packets')
    ax.set_xlabel('Hour')
    ax.set_title('Packets per hour')
    ax.legend()

    # base64 transformation
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return uri

# Recibe: json con estadisticas de paquetes de cada tipo
# Devolve: Impresión nunha gráfica do número de cada paquete
def plotdatamac(env, mac, inidate):
    labels = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']

    inidate = datetime.strptime(inidate, "%Y-%m-%d")
    enddate = inidate + timedelta(hours=1)

    counts = []
    hour = 0
    while hour<24:
        inidatestr = inidate.strftime('%Y-%m-%dT%H:%M.%f')
        enddatestr = enddate.strftime('%Y-%m-%dT%H:%M.%f')
        counts.append((db.count_mac_packets(MONGO_DB, MONGO_COLLECTION, env, mac, inidatestr, enddatestr)))
        inidate += timedelta(hours=1)
        enddate += timedelta(hours=1)
        hour +=1

    fig, ax = plt.subplots()
    ax.bar(labels, counts, label='Num packets')
    ax.set_ylabel('Num packets')
    ax.set_xlabel('Hour')
    ax.set_title('Packets per hour')
    ax.legend()

    # base64 transformation
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    return uri
