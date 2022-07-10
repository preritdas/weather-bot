# Non-local imports
import nexmo

# Project modules
import _keys


# Instantiate client
nexmo_client = nexmo.Client(
    key = _keys.Nexmo.api_key,
    secret = _keys.Nexmo.api_secret
)
sms = nexmo.Sms(nexmo_client)


def text_me(content: str) -> None:
    """
    Texts me `content`. Phone number is declared
    in `_keys.py`
    """
    sms.send_message(
        {
            "from": _keys.Nexmo.sender,
            "to": _keys.Nexmo.my_number,
            "text": content
        }
    )
