from flask_restful import Resource, reqparse, request
from models.station import StationModel

import csv
import string
import time



class Station(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('ss_model',
		type=str,
		required=True,
		help='The station model cannot be left blank'
		)

	parser.add_argument('ss_sw',
		type=str,
		required=True,
		help='The station software version cannot be left blank'
		)

	parser.add_argument('gw_id',
		type=str,
		required=True,
		help='The gw id cannot be left blank'
		)
	parser.add_argument('ss_site',
		type=str,
		required=True,
		help='The ss site cannot be left blank'
		)
	parser.add_argument('ss_num',
		type=int,
		required=True,
		help='The ss num cannot be left blank'
		)

	parser.add_argument('ss_locate',
		type=str,
		required=True,
		help='The ss locate cannot be left blank'
		)

	def get(self, ss_id):
		station = StationModel.find_by_id(ss_id)
		if station:
			return station.json()
		return {'message': 'Station not found'}, 404

class StationMod(Resource):
	#insert or update a sensor station
	def post(self):
		#data coming as form data
		data = request.form
		ss_id = data['ss_id']
		if StationModel.find_by_id(ss_id):
			return {'message': "Station with id '{}' already exists.".format(ss_id)}, 400

		with open("metadata.csv", "a", ) as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([time.ctime(), ss_id, *data.values()])

		station = StationModel(**data)

		try:
			station.save_to_db()

		except:
			return{'message': 'An error occurred while creating the station'}, 500

		#return station.json(), 201
		return {'message': 'Station {} successfully added'.format(ss_id)}, 201

	def patch(self):
		data = request.form
		ss_id = data['ss_id']
		station_update = []
		station = StationModel.find_by_id(ss_id)

		if station is None:
			return {'message': "Station id {} doesn't exist. Please add station first".format(ss_id)}, 405

		if 'ss_model' in data:
			station.ss_model = data.get('ss_model')
			station_update.append('ss_model')

		if 'ss_sw' in data:
			station.ss_sw = data.get('ss_sw')
			station_update.append('ss_sw')

		if 'gw_id' in data:
			station.gw_id = data.get('gw_id')
			station_update.append('gw_id')

		if 'ss_site' in data:
			station.ss_site = data.get('ss_site')
			station_update.append('ss_site')

		if 'ss_num' in data:
			station.ss_num = data.get('ss_num')
			station_update.append('ss_num')

		if 'ss_locate' in data:
			station.ss_locate = data.get('ss_locate')
			station_update.append('ss_locate')

		station.update_db()
		station_update = " ".join(str(elem) for elem in station_update)
		return {'message' : "Updated {} in Station id {}.".format(station_update,ss_id)}
		#return station.json()

	def delete(self):

		data = request.form
		station_id = data['ss_id']
		station = StationModel.find_by_id(station_id)
		if station:
			station.delete_from_db()
		return {'message': "Station id {} deleted".format(station_id)}, 200


class StationList(Resource):
	def get(self):
		return [station.json() for station in StationModel.query.order_by(StationModel.ss_id.desc()).all()]
