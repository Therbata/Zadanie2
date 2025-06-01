from flask import Flask, request
import datetime
import logging
import requests

AUTHOR = "Jakub Kramek"
PORT = 8080

app = Flask(__name__)

# Konfiguracja logowania do stdout
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Mapa miast i współrzędnych
cities = {
    "warszawa": (52.23, 21.01),
    "berlin": (52.52, 13.41),
    "londyn": (51.51, -0.13),
}

def fetch_weather(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        weather = data.get("current_weather", {})
        temperature = weather.get("temperature")
        windspeed = weather.get("windspeed")

        output = "<h2>Aktualna pogoda:</h2>"
        if temperature is not None:
            output += f"<p>Temperatura: {temperature} °C</p>"
        if windspeed is not None:
            output += f"<p>Wiatr: {windspeed} km/h</p>"
        return output
    except Exception as e:
        return f"<p>Błąd pobierania pogody: {str(e)}</p>"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        city = request.form.get("miasto", "")
        if city in cities:
            lat, lon = cities[city]
            result = fetch_weather(lat, lon)
            return result + "<br><a href='/'>Wróć</a>"
        else:
            return "<p>Nieznane miasto</p><a href='/'>Wróć</a>"

    form = "<h1>Wybierz miasto</h1><form method='POST'>"
    for city in cities:
        form += f"<input type='radio' name='miasto' value='{city}'>{city}<br>"
    form += "<input type='submit' value='Sprawdź pogodę'></form>"
    return form

if __name__ == "__main__":
    logging.info("=== LOGI APLIKACJI ===")
    logging.info(f"Data uruchomienia: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Autor: {AUTHOR}")
    logging.info(f"Port: {PORT}")
    logging.info("=============================")

    app.run(host="0.0.0.0", port=PORT)
