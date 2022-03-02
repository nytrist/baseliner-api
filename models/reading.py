from db import db
from sqlalchemy.orm import load_only

class ReadingModel(db.Model):
#setting up the table
	__tablename__ = 'readings'

	reading_id = db.Column(db.Integer, primary_key=True)
	live_test = db.Column(db.String(10))
	gw_date_time = db.Column(db.String(25))

#gateway diagnostics
	gw_id = db.Column(db.Integer)
	gw_rssi = db.Column(db.Integer)
	gw_conn_att = db.Column(db.Integer)
	gw_encl_temp = db.Column(db.Float(precision=2))
	gw_batt = db.Column(db.Float(precision=2))
	gw_solar_val = db.Column(db.Float(precision=2))

#sensor station diagnostics

	ss_id = db.Column(db.Integer)
	ss_num = db.Column(db.Integer)
	ss_rssi = db.Column(db.Integer)
	ss_conn_att = db.Column(db.Integer)
	ss_send_fail = db.Column(db.Integer)
	ss_encl_temp = db.Column(db.Float(precision=2))
	ss_batt = db.Column(db.Float(precision=2))
	ss_solar_val = db.Column(db.Float(precision=2))


	def __init__(self, live_test, gw_date_time, gw_id, gw_rssi, gw_conn_att, gw_encl_temp, gw_batt, gw_solar_val, ss_id, ss_num, ss_rssi, ss_conn_att, ss_send_fail, ss_encl_temp, ss_batt, ss_solar_val):
		self.live_test = live_test
		self.gw_date_time = gw_date_time

#gw diagnostics
		self.gw_id = gw_id
		self.gw_rssi = gw_rssi
		self.gw_conn_att = gw_conn_att
		self.gw_encl_temp = gw_encl_temp
		self.gw_batt = gw_batt
		self.gw_solar_val = gw_solar_val

#ss diagnostics
		self.ss_id = ss_id
		self.ss_num = ss_num
		self.ss_rssi = ss_rssi
		self.ss_conn_att = ss_conn_att
		self.ss_send_fail = ss_send_fail
		self.ss_encl_temp = ss_encl_temp
		self.ss_batt = ss_batt
		self.ss_solar_val = ss_solar_val

# return single full reading as json
	def json(self):
		return{'reading_id': self.reading_id, 'live_test': self.live_test, 'gw_date_time': self.gw_date_time, 'gw_id': self.gw_id, 'gw_rssi': self.gw_rssi, 'gw_conn_att': self.gw_conn_att, 'gw_encl_temp': self.gw_encl_temp, 'gw_batt': self.gw_batt, 'gw_solar_val': self.gw_solar_val,'ss_id': self.ss_id, 'ss_num': self.ss_num,'ss_rssi': self.ss_rssi, 'ss_conn_att': self.ss_conn_att, 'ss_send_fail': self.ss_send_fail, 'ss_encl_temp': self.ss_encl_temp, 'ss_batt': self.ss_batt, 'ss_solar_val': self.ss_solar_val}

# return single gw fields
	def json_gw(self):
		return{'reading_id': self.reading_id, 'live_test': self.live_test, 'gw_date_time': self.gw_date_time, 'gw_id': self.gw_id, 'gw_rssi': self.gw_rssi, 'gw_conn_att': self.gw_conn_att, 'gw_encl_temp': self.gw_encl_temp, 'gw_batt': self.gw_batt, 'gw_solar_val': self.gw_solar_val,'ss_id': self.ss_id, 'ss_num': self.ss_num}

# return full reading fields for specific gateway
	def json_gw_full(self):
		return{'reading_id': self.reading_id, 'live_test': self.live_test, 'gw_date_time': self.gw_date_time, 'gw_id': self.gw_id, 'gw_rssi': self.gw_rssi, 'gw_conn_att': self.gw_conn_att, 'gw_encl_temp': self.gw_encl_temp, 'gw_batt': self.gw_batt, 'gw_solar_val': self.gw_solar_val,'ss_id': self.ss_id, 'ss_num': self.ss_num, 'ss_rssi': self.ss_rssi, 'ss_conn_att': self.ss_conn_att, 'ss_send_fail': self.ss_send_fail, 'ss_encl_temp': self.ss_encl_temp, 'ss_batt': self.ss_batt, 'ss_solar_val': self.ss_solar_val}


# return single sensor fields
	def json_ss(self):
		return{'reading_id': self.reading_id, 'live_test': self.live_test, 'gw_date_time': self.gw_date_time, 'gw_id': self.gw_id, 'ss_id': self.ss_id, 'ss_num': self.ss_num,'ss_rssi': self.ss_rssi, 'ss_conn_att': self.ss_conn_att, 'ss_send_fail': self.ss_send_fail, 'ss_encl_temp': self.ss_encl_temp, 'ss_batt': self.ss_batt, 'ss_solar_val': self.ss_solar_val}

# return full reading fields for specific station
	def json_ss_full(self):
		return{'reading_id': self.reading_id, 'live_test': self.live_test, 'gw_date_time': self.gw_date_time, 'gw_id': self.gw_id, 'gw_rssi': self.gw_rssi, 'gw_conn_att': self.gw_conn_att, 'gw_encl_temp': self.gw_encl_temp, 'gw_batt': self.gw_batt, 'gw_solar_val': self.gw_solar_val,'ss_id': self.ss_id, 'ss_num': self.ss_num, 'ss_rssi': self.ss_rssi, 'ss_conn_att': self.ss_conn_att, 'ss_send_fail': self.ss_send_fail, 'ss_encl_temp': self.ss_encl_temp, 'ss_batt': self.ss_batt, 'ss_solar_val': self.ss_solar_val}


# return last 20 full readings
	@classmethod
	def return_last_entries(cls, self):
		readings = cls.query.order_by(ReadingModel.reading_id.desc()).limit(20).all()
		return readings

# return all readings for individual GW data only
	@classmethod
	def return_gw_readings(cls, self):
		readings = cls.query.options(load_only('reading_id', 'live_test', 'gw_date_time','gw_id', 'gw_rssi', 'gw_conn_att', 'gw_encl_temp','gw_batt', 'gw_solar_val', 'ss_id', 'ss_num')).order_by(ReadingModel.reading_id.desc()).all()
		return readings

# return ss data only
	@classmethod
	def return_ss_readings(cls, self):
		readings = cls.query.options(load_only('reading_id', 'live_test', 'gw_date_time','gw_id', 'ss_id', 'ss_num', 'ss_rssi', 'ss_conn_att', 'ss_send_fail', 'ss_encl_temp', 'ss_batt', 'ss_solar_val')).order_by(ReadingModel.reading_id.desc()).limit(20).all()
		return readings

#search for readings by reading_id
	@classmethod
	def find_by_id(cls, reading_id):
		return cls.query.filter_by(reading_id=reading_id).first()

#insert new reading
	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

#delete reading
	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
