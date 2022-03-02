from flask_restful import Resource, reqparse
import urllib.request

url = 'http://127.0.0.1:5005/readings.csv'

class Download(Resource):

	def get(self):
		print ('Download Starting ...')
		urllib.request.urlretrieve(url, r'readings.csv')
