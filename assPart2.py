import requests
from bs4 import BeautifulSoup
import pandas as pd

# create an empty list to store the data
data = []

# loop through the number of pages you want to scrape
for i in range(1, 21):
    # make a GET request to the URL
    URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1" + str(i)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # extract the product information from the HTML tags
    product_containers = soup.find_all("div", class_="product-container")
    for container in product_containers:
        product_url = container.find("a")["href"]
        product_name = container.find("a").text.strip()
        product_price = container.find("span", class_="price").text.strip()
        rating = container.find("span", class_="rating").text.strip()
        num_reviews = container.find("span", class_="num-reviews").text.strip()
        
        # add the extracted information to the data list
        data.append([product_url, product_name, product_price, rating, num_reviews])

# loop through the product URLs to extract additional information
for url in data:
    product_page = requests.get(url[0])
    soup = BeautifulSoup(product_page.content, "html.parser")
    
    # extract the product description, ASIN, manufacturer, etc.
    description = soup.find("div", class_="description").text.strip()
    asin = soup.find("span", class_="asin").text.strip()
    product_description = soup.find("div", class_="product-description").text.strip()
    manufacturer = soup.find("span", class_="manufacturer").text.strip()
    
    # add the additional information to the data list
    data[data.index(url)] += [description, asin, product_description, manufacturer]

# create a DataFrame from the extracted information and export it to a csv file
df = pd.DataFrame(data, columns=["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews", "Description", "ASIN", "Product Description", "Manufacturer"])
df.to_csv("products.csv", index=False)
