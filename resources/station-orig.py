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

	def put(self):
		data = request.form
		ss_id = data['ss_id']
		station = StationModel.find_by_id(ss_id)

		if station is None:
			station = StationModel(**data)
			station.save_to_db()
			return {'message': "A new station was added because a station with id '{}' didn't exist.".format(ss_id)}, 400

		else:

			station.ss_id = data['ss_id']
			station.ss_model = data['ss_model']
			station.ss_sw = data['ss_sw']
			station.gw_id = data['gw_id']
			station.ss_site = data['ss_site']
			station.ss_num = data['ss_num']
			station.ss_locate = data['ss_locate']


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
		return [station.json() for station in StationModel.query.all()]
