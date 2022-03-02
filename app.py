import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from security import authenticate, identity
from resources.user import UserRegister

from resources.reading import Reading, ReadingAdd, ReadingList, ReadingListGW, ReadingListGWFull, ReadingListSS, ReadingListSSFull,ReadingListAll
from resources.station import Station, StationMod, StationList
from resources.gateway import Gateway, GatewayMod, GatewayList
from resources.download import Download

DB_URL = 'postgresql://jacinta:local@localhost/baseliner'

# postgres://username:password@localhost:5432/database
# postgres://jacinta:Fr$%ti0N@localhost:5432/baselinerjpn

app  = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL','sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "jc"
api = Api(app)

#@app.before_first_request
#def create_tables():
#	db.create_all()

#auth - if needed to implement
jwt = JWT(app, authenticate, identity)

#allow cross domain requests
CORS(app)

#GET individual gateway / sensor station / reading
#api.add_resource(Gateway, '/gateway/<string:gw_id>') #returns specific gateway meta
api.add_resource(Gateway, '/gateway/<string:gw_id>') #returns specific gateway readings
api.add_resource(ReadingListGWFull, '/gateway/<string:gw_id>/readings')
api.add_resource(Station, '/station/<string:ss_id>') #returns individual sensor stations
api.add_resource(ReadingListSSFull, '/station/<string:ss_id>/readings') #returns individual sensor stations
api.add_resource(Reading, '/reading/<string:reading_id>') #gets, deletes a specific reading

#GET ALL
api.add_resource(GatewayList, '/') # returns active gateways
api.add_resource(StationList, '/stations') # returns active sensor stations
api.add_resource(ReadingList, '/readings') #returns last 20 readings
#api.add_resource(ReadingListGW, '/readings_gw') #returns last 20 of all GW readings
api.add_resource(ReadingListSS, '/readings_ss') #returns last 20  readings
api.add_resource(ReadingListAll, '/readings_all') #returns all readings

#Add reading, add, modify, delete, gateway and sensor station
api.add_resource(ReadingAdd, '/reading') #posts reading with data in body
api.add_resource(GatewayMod, '/gateway') #adds, deletes a gw
api.add_resource(StationMod, '/station') #adds, deletes a station

api.add_resource(Download, '/download') #downloads csv

api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5005, debug=True)
