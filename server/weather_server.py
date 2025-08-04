import grpc
from concurrent import futures
from protos import weather_pb2, weather_pb2_grpc
from server.config import Config
import requests




class WeatherService(weather_pb2_grpc.WeatherServiceServicer):
    def __init__(self, config:Config):
        self.config = config

    def GetWeather(self, request, context):
        city_name = request.city_name
        try:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.config.OPENWEATHER_API_KEY}&units=metric"
            )
            print(f"API response: {response.status_code}")

            if response.status_code == 200:
                weather_data = response.json()
                city = weather_data.get("name", city_name)
                main = weather_data.get("main", {})
                weather = weather_data.get("weather", [{}])[0]
                wind = weather_data.get("wind", {})

                return weather_pb2.WeatherResponse(
                    city_name=city,
                    temperature=main.get("temp", 0.0),
                    description=weather.get("description", "No description"),
                    humidity=main.get("humidity", 0),
                    wind_speed=wind.get("speed", 0.0)
                )
            else:
                return weather_pb2.WeatherResponse(
                    city_name=city_name,
                    temperature=0.0,
                    description="Failed to fetch weather.",
                    humidity=0,
                    wind_speed=0.0
                )
        except Exception as e:
            return weather_pb2.WeatherResponse(
                city_name=city_name,
                temperature=0.0,
                description=str(e),
                humidity=0,
                wind_speed=0.0
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    config = Config()
    weather_pb2_grpc.add_WeatherServiceServicer_to_server(WeatherService(config), server)
    server.add_insecure_port('[::]:50051')

    print("Server starting on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
