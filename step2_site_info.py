import truststore
truststore.inject_into_ssl()

import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("LMS_TOKEN")

API_URL = "https://lms.mai.ru/webservice/rest/server.php"

response = requests.post(
    API_URL,
    data={
        "wstoken": TOKEN,
        "wsfunction": "core_webservice_get_site_info",
        "moodlewsrestformat": "json",
    },
)

info = response.json()

print(info)

print("Сайт:", info["sitename"])
print("Пользователь:", info["fullname"])
print("Версия Moodle:", info["release"])

allowed = [f["name"] for f in info["functions"]]
print("Можно получить категории:", "core_course_get_categories" in allowed)
print("Можно получить курсы:", "core_course_get_courses_by_field" in allowed)