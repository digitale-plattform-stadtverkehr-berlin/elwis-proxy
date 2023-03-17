from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import json
import requests
import datetime
import time
import pytz
import os

TIMEZONE = pytz.timezone("Europe/Berlin")

URL = 'https://via.bund.de/wsv/elwis/rest/nts/messages/dateFrom/<FROM>/dateTo/<TO>'


HOST_NAME = os.environ.get('HOST')
PORT_NUMBER = int(os.environ.get('PORT'))

LOG_LEVEL = os.environ.get('LOG_LEVEL')
TRACE = 'TRACE'
DEBUG = 'DEBUG'
INFO = 'INFO'


def trace(message):
    if LOG_LEVEL==TRACE:
        print(message)
def debug(message):
    if LOG_LEVEL==DEBUG or LOG_LEVEL==TRACE:
        print(message)
def info(message):
    if LOG_LEVEL==INFO or LOG_LEVEL==DEBUG or LOG_LEVEL==TRACE:
        print(message)

class Server(BaseHTTPRequestHandler):
    def do_HEAD(self):
        return

    def do_GET(self):
        self.respond()

    def do_POST(self):
        return

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        content = self.get_data()
        return bytes(json.dumps(content, indent=4, sort_keys=False, ensure_ascii=False), "UTF-8")

    def respond(self):
        content = self.handle_http(200, 'application/json')
        self.wfile.write(content)

    def get_data(self):
        if 'last_update' not in self.state or (self.state['last_update']+ datetime.timedelta(hours=1) < datetime.datetime.now()):
            self.load_data()
        return self.data

    def load_data(self):
        info('Load Data')
        url = URL.replace('<FROM>', datetime.datetime.now(TIMEZONE).strftime("%Y-%m-%d")).replace('<TO>', (datetime.datetime.now(TIMEZONE)+ datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
        debug(url)
        r = requests.get(url)
        debug('HTTP-Status: '+str(r.status_code))
        if (r.status_code == 200):
            response = r.json()
            data  = {'type':'FeatureCollection','features':[]}
            for feature in response['ntsMessages']['FTM']['features']:
                if feature['properties']['messageType'] == 'OBSTRUCTION' or feature['properties']['messageType'] == 'LOCKING':
                    if self.geometryInBoundaries(feature['geometry']):
                        feature['properties']["validityPeriodStart"] = datetime.datetime.fromtimestamp(feature['properties']["validityPeriodStart"]/1000, TIMEZONE).strftime("%d.%m.%Y")
                        if feature['properties']["validityPeriodEnd"] < 253402210800000:
                            feature['properties']["validityPeriodEnd"] = datetime.datetime.fromtimestamp(feature['properties']["validityPeriodEnd"]/1000, TIMEZONE).strftime("%d.%m.%Y")
                        else:
                            feature['properties']["validityPeriodEnd"] = None
                        data['features'].append(feature)
            self.data['features'] = data['features']
            self.state['last_update'] = datetime.datetime.now()

    def geometryInBoundaries(self, geometry):
        if 'coordinates' in geometry:
            if not isinstance(geometry['coordinates'][0],list):
                if self.coordinateInBoundaries(geometry['coordinates']):
                    return True
            else:
                for coordinate in geometry['coordinates']:
                    if self.coordinateInBoundaries(coordinate):
                        return True
        if 'geometries' in geometry:
            for subGeometry in geometry['geometries']:
                if self.geometryInBoundaries(subGeometry):
                    return True

    def coordinateInBoundaries(self, coordinate):
        return coordinate[0] >= 12.5 and coordinate[0] <= 14 and coordinate[1] >= 52 and coordinate[1] <= 53
    state = {}
    data  = {'type':'FeatureCollection','features':[]}



if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), Server)
    print(time.asctime(), 'Server UP - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server DOWN - %s:%s' % (HOST_NAME, PORT_NUMBER))
