from server.extensions import db

class WeatherRecord(db.Model):
    __tablename__ = 'weather_records'

    id = db.Column(db.Integer, db.Sequence('weather_records_id_seq'), primary_key=True)
    city_name = db.Column(db.String(32), nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(32), nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Float, nullable=False)
    added_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def __init__(self, city_name, temperature, description, humidity, wind_speed):
        self.city_name = city_name
        self.temperature = temperature
        self.description = description
        self.humidity = humidity
        self.wind_speed = wind_speed


    def __repr__(self):
        return f"<Weather Record: {self.city_name}, {self.temperature}, {self.description}, {self.humidity}, {self.wind_speed}>"