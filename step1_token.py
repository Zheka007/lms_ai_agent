import truststore
truststore.inject_into_ssl()

import requests
from getpass import getpass

LMS_URL = "https://lms.mai.ru"

login = input("Логин от LMS: ")
password = getpass("Пароль: ")

response = requests.post(
    LMS_URL + "/login/token.php",
    data={
        "username": login,
        "password": password,
        "service": "moodle_mobile_app",
    },
)

print("Код ответа:", response.status_code)
print("Ответ сервера:", response.text)