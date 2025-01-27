import json
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
from lxml import etree as et

url = 'http://www.imdb.com/chart/top'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
response = requests.get(url,headers=headers)
print(response.status_code)
if response.status_code != 200:
    print("Failed to fetch the webpage")
    exit()
soup = BeautifulSoup(response.text, "html.parser")

script_tag = soup.find("script", type="application/ld+json")
json_data = json.loads(script_tag.string)

movies = []

for item in json_data["itemListElement"]:
    movie = item["item"]
    movie_info = {
        "title": movie["name"],
        "url" : movie["url"],
        "description": movie.get("description", "No description available"),
        "rating" : movie.get("aggregateRating", {}).get("ratingValue"),
        "genre" : movie.get("genre")
    }
    movies.append(movie_info)

# creating a json file 
df = pd.DataFrame(movies)
csv_file = "imdb_top_250.csv"
df.to_csv(csv_file, index=False, encoding="utf-8")
