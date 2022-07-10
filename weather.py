# Non-local imports
import requests

# Local imports
import datetime
import configparser

# Project modules
import _keys


# Config and data
config = configparser.ConfigParser()
config.read('config.ini')

class Config:
    # In int format, below
    # coordinates = tuple(list(map(lambda x: float(x), config['Location']['coordinates'].split(','))))
    coordinates: tuple[str, str] = tuple(config['Location']['coordinates'].split(','))

# Create API request URL
owm_url = "https://api.openweathermap.org/data/3.0/onecall?lat=" + \
    Config.coordinates[0] + "&lon=" + Config.coordinates[1] + \
    "&appid=" + _keys.OpenWeatherMap.api_key


# Kelvin --> farenheit converter as API returns kelvin
_kelvin_to_celsius = lambda kelvin: float(kelvin) - 273
_celsius_to_farenheit = lambda celsius: 1.8 * float(celsius) + 32
_kelvin_to_farenheit = lambda kelvin: _celsius_to_farenheit(_kelvin_to_celsius(float(kelvin)))


def _request() -> dict:
    """Calls OWM API for data."""
    response = requests.get(owm_url).json()
    # Below: when testing, so as not to unnecessarily call API
    # with open('Sample Response.json', 'r') as f:
        # return json.load(f)

    # Test for API call error
    try:
        if type(response['cod']) in [str, int]:
            raise Exception(f"API response error, code {response['cod']}.")
    except KeyError:
        pass

    return response


def day_min_max(tomorrow: bool = False, response: dict = None) -> tuple[float, float]:
    """
    Returns a tuple. First item is min, second item is max.
    Farenheit. If `tomorrow` is given `True`, returns values for tomorrow
    instead of today.
    """
    if response is None:
        response = _request()

    today: dict = response['daily'][1 if tomorrow else 0]
    min_temp, max_temp = today['temp']['min'], today['temp']['max']
    return round(_kelvin_to_farenheit(min_temp), 2), round(_kelvin_to_farenheit(max_temp), 2)


def day_rain_probability(tomorrow: bool = False, response: dict = None) -> str:
    """Returns a string, ex. 65%."""
    if response is None:
        response = _request()

    today: dict = response['daily'][1 if tomorrow else 0]
    return str(round(float(today['pop']) * 100)) + '%'


def sunset(response: dict = None) -> str:
    """
    Returns today's sunset time. Assumes all sunsets are PM
    for time processing.
    """
    if response is None:
        response = _request()

    today: dict = response['daily'][0]
    sunset_unix = int(today['sunset'])
    sunset_dt = datetime.datetime.fromtimestamp(sunset_unix)  # to datetime
    return f"{sunset_dt.hour % 12}:{sunset_dt.minute} PM"


def weather_expectation(tomorrow: bool = False, response: dict = None) -> str:
    """Returns an expectation phrase, ex. `"Expect heavy intensity rain."`"""
    if response is None:
        response = _request()

    today: dict = response['daily'][1 if tomorrow else 0]
    raw_phrase: str = today['weather'][0]['description']
    return "Expect " + raw_phrase + "."


class Weather:
    """
    Data style class wrapper around individual data gathering functions
    to allow for easy readability in the `main.py` execution.
    """
    def __init__(self):
        _response = _request()
        self._response = _response

        self.min_max: tuple[float, float] = day_min_max(response=_response)
        self.rain_probability: str = day_rain_probability(response=_response)
        self.sunset_time: str = sunset(response=_response)
        self.weather_expectation: str = weather_expectation(response=_response)
