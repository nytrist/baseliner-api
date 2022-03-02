from flask_restful import Resource, reqparse, request
from models.gateway import GatewayModel

import csv
import string
import time

class Gateway(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('gw_id',
		type=str,
		required=True,
		help='The gateway id cannot be left blank'
		)

	parser.add_argument('gw_site',
		type=str,
		required=True,
		help='The gateway site cannot be left blank'
		)

	parser.add_argument('gw_locate',
		type=str,
		required=True,
		help='The gateway location cannot be left blank'
		)

	parser.add_argument('gw_url',
		type=str,
		required=True,
		help='The gateway url cannot be left blank'
		)

	parser.add_argument('gw_dir',
		type=str,
		required=True,
		help='The gateway url directory cannot be left blank'
		)

	parser.add_argument('gw_port',
		type=int,
		required=True,
		help='The gateway url port cannot be left blank'
		)

	def get(self, gw_id):
		gateway = GatewayModel.find_by_id(gw_id)
		if gateway:
			return gateway.json()
		return {'message': 'Gateway not found'}, 404

class GatewayMod(Resource):
	def post(self):
	#csv in post body of post request
		data = request.data.decode('utf-8')

		#save reading to CSV file
		with open("metadata.csv", "a", ) as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([time.ctime(), data])

	#prep data for db
		lines = data.strip().split('\n')
		for line in lines:
			#print(line)
			data = line.strip().split(',')
			gw_id = data[0]
			gw_site = data[1]
			gw_locate = data[2]
			gw_url = data[3]
			gw_dir = data[4]
			gw_port = data[5]

			gateway = GatewayModel(gw_id, gw_site, gw_locate, gw_url, gw_dir, gw_port)


		try:
			gateway.save_to_db()
		except:
			return{'message': 'An error occurred while creating the gateway'}, 500

		return gateway.json(), 201


	def put(self):
		data = request.form
		gw_id = data['gw_id']

		gateway = GatewayModel.find_by_id(gw_id)

		if gateway is None:
			gateway = GatewayModel(gw_id, data['gw_site'], data['gw_locate'], data['gw_url'], data['gw_dir'], data['gw_port'] )
		else:
			gateway.gw_site = data['gw_site']
			gateway.gw_locate = data['gw_locate']
			gateway.gw_url = data['gw_url']
			gateway.gw_dir = data['gw_dir']
			gateway.gw_port = data['gw_port']


		gateway.save_to_db()

		return gateway.json()


	def delete(self):
		#gw_id sent via form
		data = request.form
		gw_id = data['gw_id']
		gateway = GatewayModel.find_by_id(gw_id)
		if gateway:
			gateway.delete_from_db()

		return {'message': 'Gateway deleted'}

class GatewayList(Resource):
	def get(self):
		return [gateway.json() for gateway in GatewayModel.query.all()]
