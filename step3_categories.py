import truststore
truststore.inject_into_ssl()

import os
import requests
from dotenv import load_dotenv
import json

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

categories = call_api("core_course_get_categories")
with open("data/raw/categories.json", "w", encoding='utf-8') as file:
    json.dump(categories, file, ensure_ascii=False, indent=2)

count_high_level = 0
name_high_level = []
count_not_null_course = 0
sum_courses = 0
for cat in categories:
    if cat["parent"] == 0:
        count_high_level += 1
        name_high_level.append(cat["name"])

    if cat["coursecount"] != 0:
        count_not_null_course += 1
        sum_courses += cat["coursecount"]

print("Количество категорий верхнего уровня:", count_high_level)
print("Названия категорий верхнего уровня:", name_high_level)
print("Категории, в которых есть курсы:", count_not_null_course)
print("Количество курсов:", sum_courses)

categories_dict = {cat["id"]: cat["name"] for cat in categories}
full_names = {}
for cat in categories:
    path = cat["path"].split('/')[1:]
    name_cat = " / ".join([categories_dict[int(cat_id)] for cat_id in path])
    full_names[cat["id"]] = name_cat

print(full_names[420])