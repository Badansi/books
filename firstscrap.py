#importe de la bibliothèque CSV
import requests
from bs4 import BeautifulSoup
import csv

# Récupérer la page web du livre à recuperer
url = "http://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"
response = requests.get(url)

# Parser(annalyse et extraction à partir du html) le contenu de la page web avec BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extraire les données specifiques par ligne(ce quil faut récuperer)
product_page_url = url
upc = soup.select_one("table tr:nth-of-type(1) td").text
title = soup.select_one("h1").text
price_including_tax = soup.select_one("table tr:nth-of-type(4) td").text
price_excluding_tax = soup.select_one("table tr:nth-of-type(3) td").text
number_available = soup.select_one("table tr:nth-of-type(6) td").text.replace("In stock (", "").replace(" available)", "")
product_description = soup.select_one("article p").text
category = soup.select("ul.breadcrumb li")[2].text.strip()
review_rating = soup.select_one("div.col-sm-6 p.star-rating")["class"][1]
image_url = soup.select_one("div.item img")["src"].replace("../..", "http://books.toscrape.com")

# Écrire les données dans un fichier CSV
with open("books_data.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["product_page_url", "universal_product_code (upc)", "title", "price_including_tax", "price_excluding_tax", "number_available", "product_description", "category", "review_rating", "image_url"])
    writer.writerow([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available, product_description, category, review_rating, image_url])
