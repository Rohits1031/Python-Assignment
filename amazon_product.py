import requests
from bs4 import BeautifulSoup as bs 
import pandas as pd

def get_url_response(url):

    req = requests.get(url)
    soup = bs(req.content,'html.parser')

    return soup

pro_url = []
pro_name=[]
pro_price=[]
pro_reviews=[]
pro_rating=[]

def product_url_and_info(soup):

    #___product url ____
    
    a_tag = soup.find_all('a', class_ = 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')
    for p_url in a_tag:
        url = p_url['href']
        url = 'https://www.amazon.in/'+url
        pro_url.append(url)
    
    #___product name ____
    
    name=soup.find_all('span',{'class':'a-size-medium a-color-base a-text-normal'})
    for pname in name:
        pro_name.append(pname.text)

    #___product price ____
    
    price=soup.findAll('span', class_ = 'a-price-whole')
    for amount in price:
        pro_price.append(amount.text)

    
    #___No of reviews____
    
    reviews=soup.find_all('span',{'class':'a-size-base s-underline-text'})
    for view in reviews:
        pro_reviews.append(view.text)
        
    #___product rating____
    
    rating=soup.find_all('span',{'class':'a-icon-alt'})
    for rt in rating:
        pro_rating.append(rt.text)

product_data = []

def product_details(soup):

    #  description = soup.find('span', {'id' : 'productTitle'}).text
    #  print(description)
    description = soup.find('span', class_ = 'a-size-large product-title-word-break').text
    ASIN = soup.find_all('div', class_ = "a-expander-content a-expander-section-content a-section-expander-inner")
    manu = soup.find('td', class_ = 'a-size-base prodDetAttrValue')
    pro_discrip =soup.find('div',class_='a-section a-spacing-small').text

    record={
        'description':description,
        'Asin':ASIN,
        'productDescription':pro_discrip,
        'manufucture':manu
    }
    product_data.append(record)
    


for page in range(1, 70):

    url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'+str(page)
    print(url)
 
    soup = get_url_response(url)
    product_url_and_info(soup)

df = pd.DataFrame(list(zip(pro_url, pro_name, pro_price, pro_rating, pro_reviews)),
               columns =['Product Url', 'Product Name', 'Price', 'Rating', 'Review'])

df.to_csv("Amazon_part_1 assignment.csv")
print(df)

for pdetail in pro_url:
    soup=get_url_response(pdetail)
    product_details(soup)

df = pd.DataFrame(product_data)
print(df)