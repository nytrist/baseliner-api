from db import db
from models.reading import ReadingModel

class StationModel(db.Model):
	__tablename__ = 'stations'

	id = db.Column(db.Integer, primary_key=True)

#Sensor Station Meta data
	ss_id = db.Column(db.Integer)
	ss_model = db.Column(db.String(255))
	ss_sw = db.Column(db.String(255))
	gw_id = db.Column(db.Integer)
	ss_site = db.Column(db.String(255))
	ss_num = db.Column(db.Integer)
	ss_locate = db.Column(db.String(255))

	def __init__(self, ss_id, ss_model, ss_sw, gw_id, ss_site, ss_num, ss_locate):
		self.ss_id = ss_id
		self.ss_model = ss_model
		self.ss_sw = ss_sw
		self.gw_id = gw_id
		self.ss_site = ss_site
		self.ss_num = ss_num
		self.ss_locate = ss_locate

# Returns ALL readings
	#def json_all(self):
	#	return{'ss_id': self.ss_id, 'gw_id':self.gw_id, 'ss_site': self.ss_site, 'ss_num': self.ss_num,'ss_locate': self.ss_locate, 'readings': [reading.json() for reading in self.readings.all()]}

	def json(self):
		ss_id=self.ss_id
		gw_id=self.gw_id
		ss_readings = ReadingModel.query.filter(ReadingModel.ss_id==ss_id).order_by(ReadingModel.reading_id.desc()).all() # displays all readings from this sensor station
		#ss_readings = ReadingModel.query.filter(ReadingModel.ss_id==ss_id, ReadingModel.gw_id==gw_id).all() #displays all readings from sensor statement and current paired gateway
		return{'ss_id': self.ss_id, 'ss_model': self.ss_model, 'ss_sw': self.ss_sw, 'gw_id':self.gw_id, 'ss_site': self.ss_site, 'ss_num': self.ss_num,'ss_locate': self.ss_locate, 'readings': [reading.json() for reading in ss_readings]}


#search by serial number
	@classmethod
	def find_by_id(cls, ss_id):
		return cls.query.filter_by(ss_id=ss_id).first()

#insert new node
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

#update node
	def update_db(self):
		db.session.commit()


#delete node
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
