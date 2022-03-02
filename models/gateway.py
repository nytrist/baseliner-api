from db import db
from models.station import StationModel

class GatewayModel(db.Model):
	__tablename__ = 'gateways'

	id = db.Column(db.Integer, primary_key=True)

# meta data
	gw_id = db.Column(db.Integer)
	gw_model = db.Column(db.String(255))
	gw_sw = db.Column(db.String(255))
	gw_lora_addr = db.Column(db.String(255))
	gw_site = db.Column(db.String(255))
	gw_locate = db.Column(db.String(255))

	def __init__(self, gw_id, gw_model, gw_sw, gw_lora_addr, gw_site, gw_locate):
		self.gw_id = gw_id
		self.gw_model = gw_model
		self.gw_sw = gw_sw
		self.gw_lora_addr = gw_lora_addr
		self.gw_site = gw_site
		self.gw_locate = gw_locate

	def json(self):
		gw_id=self.gw_id
		gw_stations = StationModel.query.filter(StationModel.gw_id==gw_id).all()
		return{'gw_id': self.gw_id, 'gw_model': self.gw_model, 'gw_sw': self.gw_sw, 'gw_lora_addr': self.gw_lora_addr,'gw_site': self.gw_site, 'gw_locate': self.gw_locate, 'gw_stations': [station.json() for station in gw_stations]}

#search by gateway ID
	@classmethod
	def find_by_id(cls, gw_id):
		return cls.query.filter_by(gw_id=gw_id).first()

#return gw stations
	#@classmethod
	#def gw_stations(cls, self, gw_id):
	#	return object.session(self).get(Stations, self.station_id)


#insert new gateway
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

# update existing gateway
	def update_db(self):
		db.session.commit()

#delete gateway
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
