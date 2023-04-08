import requests
from bs4 import BeautifulSoup
import csv

def get_soup(url):
    # Récupérer le contenu de la page web et parser avec BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

# Récupérer les données du livre spécifique
url = "http://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"
soup = get_soup(url)

# Extraire les données spécifiques à partir de la page web
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

# Récupérer les URL de la catégorie "Art"
url = "http://books.toscrape.com/catalogue/category/books/art_25/index.html"
soup = get_soup(url)

# Trouver tous les liens de produit sur la page et extraire l'URL de chaque produit
product_links = soup.select("h3 a")
product_urls = [link["href"] for link in product_links]

# Parcourir les pages de pagination pour récupérer toutes les URL de produit
next_page = soup.select_one("li.next a")
while next_page:
    next_page_url = next_page["href"]
    soup = get_soup(next_page_url)
    product_links = soup.select("h3 a")
    product_urls += [link["href"] for link in product_links]
    next_page = soup.select_one("li.next a")

# Écrire les URL de produit dans un fichier CSV
with open("art_books_urls.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["product_url"])
    for url in product_urls:
        writer.writerow([url])
