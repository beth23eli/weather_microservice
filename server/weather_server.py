import grpc
from concurrent import futures
from protos import weather_pb2, weather_pb2_grpc
from server.config import Config
import requests
from server.models.WeatherRecord import WeatherRecord
from server import create_app
from server.extensions import db

app = create_app()

class WeatherService(weather_pb2_grpc.WeatherServiceServicer):
    def __init__(self, config:Config):
        self.config = config

    def GetWeather(self, request, context):
        with app.app_context():
            city_name = request.city_name

            try:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.config.OPENWEATHER_API_KEY}&units=metric"
                )
                print(f"API response: {response.status_code}")

                data = response.json()
                city = data.get("name", city_name)
                main = data.get("main", {})
                weather = data.get("weather", [{}])[0]
                wind = data.get("wind", {})

                db.session.add(
                    WeatherRecord(
                        city_name=city,
                        temperature=main.get("temp", 0.0),
                        description=weather.get("description", "No description"),
                        humidity=main.get("humidity", 0),
                        wind_speed=wind.get("speed", 0.0)
                    )
                )
                db.session.commit()

                return weather_pb2.WeatherResponse(
                    city_name=city,
                    temperature=main.get("temp", 0.0),
                    description=weather.get("description", "No description"),
                    humidity=main.get("humidity", 0),
                    wind_speed=wind.get("speed", 0.0)
                )

            except requests.exceptions.RequestException as e:
                context.abort(grpc.StatusCode.UNAVAILABLE, f"API error: {e}")
            except Exception as e:
                if response.status_code == 404:
                    context.abort(grpc.StatusCode.NOT_FOUND, f"City '{city_name}' not found.")
                db.session.rollback()

                context.abort(grpc.StatusCode.INTERNAL, f"Unexpected error: {e}")


def serve():
    with app.app_context():
        db.create_all()

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        config = Config()
        weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(config), server)
        server.add_insecure_port('[::]:50051')

        print("Server starting on port 50051...")
        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    serve()
