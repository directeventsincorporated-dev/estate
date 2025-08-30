import os
import json
import datetime
import urllib.request
import urllib.error


def fetch_json(url: str):
    """Fetch JSON data from a URL, returning a dict with an 'error' key on failure."""
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            return json.loads(response.read().decode())
    except Exception as exc:
        return {"error": str(exc)}


def main() -> None:
    """Display local time, weather and traffic information for the current location."""
    # Determine local time from IP-based service
    time_info = fetch_json("http://worldtimeapi.org/api/ip")
    if "error" in time_info:
        print("Could not fetch time:", time_info["error"])
    else:
        dt = datetime.datetime.fromisoformat(time_info["datetime"])
        print("Local time:", dt.strftime("%Y-%m-%d %H:%M:%S"))
        print("Day of week:", dt.strftime("%A"))

    # Determine geolocation from IP
    loc_info = fetch_json("http://ip-api.com/json")
    if "error" in loc_info:
        print("Could not fetch location:", loc_info["error"])
        return

    lat, lon = loc_info.get("lat"), loc_info.get("lon")
    city = loc_info.get("city", "Unknown city")
    region = loc_info.get("regionName", "")
    country = loc_info.get("country", "")
    print(f"Location: {city}, {region}, {country}")

    # Weather information from Open-Meteo
    weather_url = (
        "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true".format(
            lat=lat, lon=lon
        )
    )
    weather_info = fetch_json(weather_url)
    if "error" in weather_info:
        print("Could not fetch weather:", weather_info["error"])
    else:
        current_weather = weather_info.get("current_weather", {})
        temperature = current_weather.get("temperature")
        windspeed = current_weather.get("windspeed")
        print(f"Weather: {temperature}°C, wind {windspeed} km/h")

    # Traffic information via TomTom API (requires API key)
    api_key = os.getenv("TOMTOM_API_KEY")
    if not api_key:
        print("Traffic: set TOMTOM_API_KEY environment variable for traffic data.")
        return

    traffic_url = (
        "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&key={key}".format(
            lat=lat, lon=lon, key=api_key
        )
    )
    traffic_info = fetch_json(traffic_url)
    if "error" in traffic_info:
        print("Could not fetch traffic:", traffic_info["error"])
    elif "flowSegmentData" in traffic_info:
        segment = traffic_info["flowSegmentData"]
        print(
            f"Traffic: current {segment.get('currentSpeed')} km/h (free flow {segment.get('freeFlowSpeed')} km/h)"
        )
    else:
        print("Traffic data unavailable.")


if __name__ == "__main__":
    main()
