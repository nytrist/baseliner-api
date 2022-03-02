from flask_restful import Resource, reqparse, request
from models.gateway import GatewayModel

import csv
import string
import time

class Gateway(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument('gw_model',
		type=str,
		required=True,
		location='form',
		help='The gateway model cannot be left blank'
		)

	parser.add_argument('gw_sw',
		type=str,
		required=True,
		help='The gateway software version cannot be left blank'
		)

	parser.add_argument('gw_lora_addr',
		type=str,
		required=True,
		help='The gateway lora address cannot be left blank'
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

#return specific gateway
	def get(self, gw_id):
		gateway = GatewayModel.find_by_id(gw_id)
		if gateway:
			return gateway.json()
		return {'message': 'Gateway not found'}, 404

class GatewayMod(Resource):
#add gateway
	def post(self):
		#data coming as form
		data = request.form
		gw_id = data['gw_id']
		if GatewayModel.find_by_id(gw_id):
			return {'message': "Gateway with id '{}' already exists.".format(gw_id)}, 400

		with open("metadata.csv", "a", ) as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([time.ctime(), gw_id, *data.values()])

		data = Gateway.parser.parse_args()
		gateway = GatewayModel(gw_id, **data)
		try:
			gateway.save_to_db()
		except:
			return{'message': 'An error occurred while creating the gateway'}, 500

		#return gateway.json(), 201
		return{'message': 'Gateway {} successfully added'.format(gw_id)}, 201

#update gateway
	def patch(self):
		data = request.form
		gw_id = data['gw_id']
		gw_update = []
		gateway = GatewayModel.find_by_id(gw_id)
		if gateway is None:
			return {'message': "Gateway id {} doesn't exist. Please add gateway first".format(gw_id)}, 405

		if 'gw_model' in data:
			gateway.gw_model = data.get('gw_model')
			gw_update.append('gw_model')

		if 'gw_sw' in data:
			gateway.gw_sw = data.get('gw_sw')
			gw_update.append('gw_sw')

		if 'gw_lora_addr' in data:
			gateway.gw_lora_addr = data.get('gw_lora_addr')
			gw_update.append('gw_lora_addr')

		if 'gw_site' in data:
			gateway.gw_site = data.get('gw_site')
			gw_update.append('gw_site')

		if 'gw_locate' in data:
			gateway.gw_locate = data.get('gw_locate')
			gw_update.append('gw_locate')

		gateway.update_db()
		gw_update = " ".join(str(elem) for elem in gw_update)
		return {'message' : "Updated {} in Gateway id {}.".format(gw_update,gw_id)}
#		return gateway.json()

#delete gateway function
	def delete(self):
		#gw_id sent via form
		data = request.form
		gw_id = data['gw_id']
		gateway = GatewayModel.find_by_id(gw_id)
		if gateway:
			gateway.delete_from_db()

		return {'message': "Gateway id {} deleted".format(gw_id)}, 200

class GatewayList(Resource):
#return gateway
	def get(self):
		return [gateway.json() for gateway in GatewayModel.query.order_by(GatewayModel.gw_id.desc()).all()]
