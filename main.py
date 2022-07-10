# Non-local imports
import mypytoolkit as kit

# Local imports
import time
from datetime import datetime

# Project modules
import weather
import texts


def main() -> None:
    """Delivers weather update daily at 8 am."""
    while True:
        # Wait until 8 am
        while kit.time_now() != '08-00':
            time.sleep(1)
        
        # Compile message
        today_weather = weather.Weather()
        text_message = f"Today's min: {today_weather.min_max[0]} F. \n" \
            f"Today's max: {today_weather.min_max[1]} F. \n" \
            f"There's a {today_weather.rain_probability} chance of rain. \n" \
            f"The sun will set at {today_weather.sunset_time}. \n" + \
            today_weather.weather_expectation

        # Deliver message, log delivery
        texts.text_me(text_message)
        print(f'Delivered on {datetime.today()}. ')

        # Ensure no re-run until tomorrow
        time.sleep(60)


if __name__ == '__main__':
    main()
