# Weather Microservice

This app provides weather data for cities, featuring both gRPC and REST APIs, a PostgreSQL database for storage, and a ReactJS frontend for visualization.

It was built with:
- **PostgreSQL** as the relational database to store weather records. The database `weather_station_db` contains the table:
  - The `weather_records` table includes:
    - `id` – the identifier of a weather record;
    - `city_name` – the name of the city;
    - `temperature` – the recorded temperature (°C);
    - `description` – weather description (e.g., "clear sky");
    - `humidity` – humidity percentage;
    - `wind_speed` – wind speed (m/s);
    - `added_at` – timestamp when the record was added.
    <br/><br/>

- **Python with Flask and gRPC** as the backend server:
    - **Flask** exposes a REST endpoint for retrieving weather data for charting.
    - **gRPC** provides a service for querying and storing weather data for cities.
    - The backend interacts with the database to store and retrieve weather records.
    <br/><br/>

- **ReactJS** for the UI. The user interface displays weather trends and charts for selected cities.
    <br/><br/>

- **Docker Compose** for managing and running the multi-container Docker app. It creates containers for the backend server, the database, the client, and the frontend.

### Important additions:
- **Protocol Buffers (Protos)**

  - The gRPC service and messages are defined in `protos/weather.proto`.
  - To generate the Python code for gRPC communication, I ran:
    ```
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/weather.proto
    ```
  - This will create `weather_pb2.py` and `weather_pb2_grpc.py` in the `protos` directory, which are used by both the server and client for gRPC requests and responses.
- **Packages:**
    - `requests` – Used to fetch weather data from the OpenWeather API;
    - `grpcio` and `grpcio-tools` – Used for gRPC communication and code generation;
    - `Flask` – Used for REST API endpoints;
    - `SQLAlchemy` – Used for ORM mapping between Python classes and database tables.

- **ORM:**
    - `SQLAlchemy` – Used for mapping Python classes to database tables and managing relationships.

- **API Endpoints:**
    - **gRPC Service:**  
      - `GetWeather(city_name)` – Fetches and stores weather data for a given city.
    - **REST Endpoint:**  
      - `/weather-data` (GET) – Returns weather data grouped by city for charting in the frontend.

## Running this app:
You will need to have Docker installed. If you are using Windows, you can run commands in PowerShell or WSL.

__Step 1__: Clone this repo and move into the directory:
```
git clone https://github.com/beth23eli/weather_microservice.git

cd weather_microservice
```

__Step 2__: Create a `.env` file for the backend server (example in `server/.env.example`):
```
cp server/.env.example server/.env
```
Edit `server/.env` and add your OpenWeather API key and database connection string:

__Step 3__: Open **Docker Desktop**.

__Step 4__: Run the **docker-compose** file to build the images and run the containers:
```
docker-compose up --build
```

__Step 5__: (Optional) Run the client to populate the database with weather data:
```
docker-compose run --rm client
```

__Step 6__: Open the frontend in your browser at [http://localhost:3000](http://localhost:3000)

### Cleanup
To close the app, run:
```
docker-compose down
```
To also delete the volumes, run:
```
docker-compose down -v