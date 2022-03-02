from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.reading import ReadingModel

import csv
import string
import time


class Reading(Resource):

#get individual reading
	#@jwt_required() - removed authentication
	def get(self, reading_id):
		reading = ReadingModel.find_by_id(reading_id)
		if reading:
			return reading.json()
		return{'message': 'Reading not found'}, 404


class ReadingAdd(Resource):
#add, delete reading
	def post(self):
		#csv in post body of post request
		data = request.data.decode('utf-8')

			#save reading to CSV file
		with open("readings.csv", "a", ) as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([time.ctime(), data])

		#prep data for db
		lines = data.strip().split('\n')
		for line in lines:
			#print(line)
			data = line.strip().split(',')
			live_test = data[0]
			gw_date_time = data[1]

			gw_id = data[2]
			gw_rssi = data[3]
			gw_conn_att = data[4]
			gw_encl_temp = data[5]
			gw_batt = data[6]
			gw_solar_val = data[7]

			ss_id = data[8]
			ss_num = data[9]
			ss_rssi = data[10]
			ss_conn_att = data[11]
			ss_send_fail = data[12]
			ss_encl_temp = data[13]
			ss_batt = data[14]
			ss_solar_val = data[15]

			reading = ReadingModel(live_test, gw_date_time, gw_id, gw_rssi, gw_conn_att, gw_encl_temp, gw_batt, gw_solar_val, ss_id, ss_num, ss_rssi, ss_conn_att, ss_send_fail, ss_encl_temp, ss_batt, ss_solar_val)

		try:
			#save to db
			reading.save_to_db()

		except:
			return{"message": "An error occurred inserting the reading."}, 500 # internal server error

		return reading.json(), 201

#delete readings
	def delete(self):

		data = request.form
		reading_id = data['reading_id']

		reading = ReadingModel.find_by_id(reading_id)
		if reading:
			reading.delete_from_db()
		return {'message': 'Reading deleted.'}

class ReadingList(Resource):
#get last 20 readings
	def get(self):
		readings = ReadingModel.return_last_entries(self)
		return [reading.json() for reading in readings]

		#working alternate: return [reading.json() for reading in ReadingModel.query.order_by(ReadingModel.reading_id.desc()).limit(3).all()]

class ReadingListGW(Resource):
#get all readings for individual gateway with gateway data only
	def get(self, gw_id):
		readings = ReadingModel.query.filter(ReadingModel.gw_id==gw_id).order_by(ReadingModel.reading_id.desc()).all()
		return [reading.json_gw() for reading in readings]

class ReadingListGWFull(Resource):
#get all readings for individual gateway with full data
	def get(self, gw_id):
		readings = ReadingModel.query.filter(ReadingModel.gw_id==gw_id).order_by(ReadingModel.reading_id.desc()).limit(20).all()
		return [reading.json_gw_full() for reading in readings]



#get all gw readings for all gateways
#	def get(self):
#		readings = ReadingModel.return_gw_readings(self)
#		return [reading.json_gw() for reading in readings]
#		working alternate: return [reading.json() for reading in ReadingModel.query.order_by(ReadingModel.reading_id.desc()).limit(3).all()]

class ReadingListSS(Resource):
#get sensor node only readings
	def get(self):
		readings = ReadingModel.return_ss_readings(self)
		return [reading.json_ss() for reading in readings]

		#working alternate:return [reading.json_ss() for reading in ReadingModel.query.order_by(ReadingModel.reading_id.desc()).limit(3).all()]

class ReadingListSSFull(Resource):
#get all readings for individual gateway with full data
	def get(self, ss_id):
		readings = ReadingModel.query.filter(ReadingModel.ss_id==ss_id).order_by(ReadingModel.reading_id.desc()).limit(20).all()
		return [reading.json_ss_full() for reading in readings]


class ReadingListAll(Resource):
#get all readings
	def get(self):
		return [reading.json() for reading in ReadingModel.query.order_by(ReadingModel.reading_id.desc()).all()]
