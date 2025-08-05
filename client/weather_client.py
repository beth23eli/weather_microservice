import grpc
from protos import weather_pb2, weather_pb2_grpc
import time


def run():

    #with grpc.insecure_channel('localhost:50051') as channel:
    with grpc.insecure_channel('grpc_server:50051') as channel:

        stub = weather_pb2_grpc.WeatherServiceStub(channel)

        for i in range(5):
            city_name = input("Enter city name: ")

            try:
                response = stub.GetWeather(weather_pb2.WeatherRequest(city_name=city_name))

                if "Failed" in response.description:
                    print(f"Error: {response.description}")
                else:
                    print(f"\nWeather for {response.city_name}:\n"
                          f"Temperature: "+"{:.2f}".format(response.temperature) +"°C\n"
                          f"Description: {response.description}\n"
                          f"Humidity: {response.humidity}%\n"
                          f"Wind Speed: "+"{:.2f}".format(response.wind_speed) +" m/s\n")
            except grpc.RpcError as e:
                print(f"RPC Error: {e.code().name} - {e.details()}")

            if i < 4:
                time.sleep(10)


if __name__=="__main__":
    run()
