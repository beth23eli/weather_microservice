import grpc
from protos import weather_pb2, weather_pb2_grpc


def run():
    city_name = input("Enter city name: ")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = weather_pb2_grpc.WeatherServiceStub(channel)

        response = stub.GetWeather(weather_pb2.WeatherRequest(city_name=city_name))


        print(f"\nWeather for {response.city_name}:\n"
              f"Temperature: "+"{:.2f}".format(response.temperature) +"°C\n"
              f"Description: {response.description}\n"
              f"Humidity: {response.humidity}%\n"
              f"Wind Speed: "+"{:.2f}".format(response.wind_speed) +" m/s")


if __name__=="__main__":
    run()