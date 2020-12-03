# Dependencies
from bs4 import BeautifulSoup
import os
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests


### NASA Mars News

# URL of page to be scraped
url = 'https://mars.nasa.gov/news'

# Retrieve page with the requests module
response = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')

# Examine the results, then determine element that contains sought info
print(soup.prettify())

# results are returned as an iterable list
results = soup.find_all('div', class_="slide")

# loop over results to get slide data
for result in results:
    # scrape the article header 
    header = result.find('div', class_='content_title').text
    
    # scrape the article subheader
    subheader = result.find('div', class_='rollover_description_inner').text
    
    
    # print article data
    print('-----------------')
    print(header)
    print(subheader)


### JPL Mars Space Images - Featured Image

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url2 = "https://jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(url2)

# Scrape the browser into soup and use soup to find the image of mars
# Save the image url to a variable called `img_url`
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
image = soup.find("img", class_="thumb")["src"]
img_url = "https://jpl.nasa.gov"+image
featured_image_url = img_url

# Use the requests library to download and save the image from the `img_url` above
import requests
import shutil
response = requests.get(img_url, stream=True)
with open('img.jpg', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)

# Display the image 
from IPython.display import Image
Image(url='img.jpg')

### Mars Facts

import pandas as pd

# URL of page to be scraped
url3 = 'https://space-facts.com/mars/'

# Use the read_html function in Pandas to automatically scrape any tabular data from a page.

tables = pd.read_html(url3)
tables

df = tables[0]
df

# Generate HTML tables from DataFrames.
html_table = df.to_html()
html_table


df.to_html('table.html')

#get_ipython().system('open table.html')

### Mars Hemispheres

# Visit the USGS Astogeology site and scrape pictures of the hemispheres
url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url4)

# Use splinter to loop through the 4 images and load them into a dictionary
import time 
html = browser.html
soup = BeautifulSoup(html, 'html.parser')
hemisphere_image_urls=[]

# loop through the four tags and load the data to the dictionary

for i in range (4):
    time.sleep(5)
    images = browser.find_by_tag('h3')
    images[i].click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    partial = soup.find("img", class_="wide-image")["src"]
    img_title = soup.find("h2",class_="title").text
    img_url = 'https://astrogeology.usgs.gov'+ partial
    dictionary={"title":img_title,"img_url":img_url}
    hemisphere_image_urls.append(dictionary)
    browser.back()
    
# print data
    print('-----------------')
    print(img_title)
    print(img_url)


hemisphere_image_urls