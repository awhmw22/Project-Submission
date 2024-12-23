import socket
import requests

def fetch_weather(city, api_key):
    """Fetch weather data from OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract weather details
        city_name = data["name"]
        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return (f"Weather in {city_name}:\n"
                f"Temperature: {temperature}°C\n"
                f"Condition: {condition.capitalize()}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s\n")
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except KeyError:
        return "City not found."

# Server setup
def start_server(api_key):
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Weather server is running on {host}:{port}")
    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        # Receive city name from client
        city = conn.recv(1024).decode().strip()
        if not city:
            conn.close()
            continue

        print(f"Client requested weather for: {city}")

        # Fetch weather data and send response
        weather_data = fetch_weather(city, api_key)
        conn.send(weather_data.encode())

        conn.close()

if __name__ == "__main__":
    # Replace with your OpenWeatherMap API key
    API_KEY = "09c993343e0d3155076eb4bf2418cbfa"
    start_server(API_KEY)
