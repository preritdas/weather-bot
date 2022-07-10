# Weather Bot

Simply, Weather Bot gathers basic weather data (using [OpenWeatherMap](https://openweathermap.com)) and delivers it by text message each morning.

## Requirements

Besides PyPI packages (install with `pip install -r requirements.txt`), you need a few config and keys files for the main executor to run correctly. 

### `config.ini`

Specify the location, by coordinates, for which you want your weather data.

```ini
[Location]
coordinates = 55.55,-55.55
```

### `_keys.py`

Store API keys for OpenWeatherMap and Nexmo.

Your OpenWeatherMap key must have access to their One Call API 3.0. You get 1,000 free API calls per day. _Weather Bot only makes 1 API call per day._

```python
class OpenWeatherMap:
    api_key = 'key_goes_here'


class Nexmo:
    api_key = 'key_goes_here'
    api_secret = 'super_secret'
    sender = 'nexmo_sender_provided'
    my_number = 'your_phone_number'
```