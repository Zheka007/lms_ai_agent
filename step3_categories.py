import truststore
truststore.inject_into_ssl()

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("LMS_TOKEN")

API_URL = "https://lms.mai.ru/webservice/rest/server.php"

session = requests.Session()

def call_api(function, **params):
    data = {
        "wstoken": TOKEN,
        "wsfunction": function,
        "moodlewsrestformat": "json",
        **params,
    }

    response = session.post(API_URL, data=data, timeout=30)
    result = response.json()

    if isinstance(result, dict) and "exception" in result:
        raise RuntimeError(f"{result['errorcode']}: {result['message']}")

    return result

info = call_api("core_webservice_get_site_info")
print("Сайт:", info['sitename'])