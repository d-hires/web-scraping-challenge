
# Dependencies
import pandas as pd
import requests
from sqlalchemy import create_engine
from splinter import Browser
from bs4 import BeautifulSoup
import time
import sys

def init_browser():
    executable_path = {'executable_path': 'c:\chromedriver\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(2)

    # Retrieve page with the requests module
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # print(soup.prettify())

    # results are returned as an iterable list
    html_element = soup.find('li', class_="slide")
    for h in html_element:
        news_title = h.find('div', class_='content_title').text
    # news_title

    # results are returned as an iterable list
    html_element = soup.find('li', class_="slide")
    for h in html_element:
        news_teaser = h.find('div', class_='article_teaser_body').text
    # news_teaser

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    html_element = soup.find('article', class_='carousel_item')
    # print(html_element.prettify())

    html_seg_str = str(html_element)
    str_start = html_seg_str.find("url('")
    str_end = html_seg_str.find("');")
    featured_image_url = html_seg_str[str_start + 5:str_end]
    complete_featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url
    # complete_featured_image_url

    mars_facts_url = 'https://space-facts.com/mars/'
    response = requests.get(mars_facts_url)
    mars_facts_table = pd.read_html(response.text)
    mars_facts_df = pd.DataFrame(mars_facts_table[0])
    mars_facts_df.rename(columns={1 : "Mars",}, inplace=True)
    mars_facts_df.set_index(0,inplace=True)
    # mars_facts_df

    mars_facts_html = mars_facts_df.to_html()
    mars_facts_html = mars_facts_html.replace('border="1" class="dataframe"', 'class="table"')
    # mars_facts_html
    
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    itemLink_list = browser.find_by_css('.itemLink')
    hemisphere_link_urls = []
    complete_hemisphere_image_urls = []

    for item in itemLink_list:
        if "Enhanced" in item.text:
            hemisphere_link_urls.append({"title": item.text, "img_url": item["href"]})

    # for url in hemisphere_img_urls:
    #     print(url)
    for i in range(len(hemisphere_link_urls)):
        url = hemisphere_link_urls[i]["img_url"]
        browser.visit(url)
        time.sleep(2) 

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        html_element = soup.find('div', class_='wide-image-wrapper')
        html_seg_str = str(html_element)
        str_start = html_seg_str.find('src="')
        str_end = html_seg_str.find('"/>')
        hemisphere_image_url = html_seg_str[str_start + 5:str_end] 
        complete_hemisphere_image_urls.append('https://astrogeology.usgs.gov' + hemisphere_image_url)

    # hemisphere_img_urls = []
    # hemisphere_img_urls.append(
    #     {"title": "Cerberus Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"})
    # hemisphere_img_urls.append(
    #     {"title": "Schiaparelli Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"})
    # hemisphere_img_urls.append(
    #     {"title": "Syrtis Major Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"})
    # hemisphere_img_urls.append(
    #     {"title": "Valles Marineris Hemisphere Enhanced", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"})
    # # hemisphere_img_urls

    mars = [{"news_title": news_title,
                   "news_teaser": news_teaser,
                   "featured_img": complete_featured_image_url,
                   "hemisphere_img_cerberus": complete_hemisphere_image_urls[0],
                   "hemisphere_img_schiaparelli": complete_hemisphere_image_urls[1],
                   "hemisphere_img_syrtis_major": complete_hemisphere_image_urls[2],
                   "hemisphere_img_valles_marineris": complete_hemisphere_image_urls[3],
                   }]
    # print(mars, sys.stderr)                   
    return mars

    # return_list = scrape()
    # print(return_list[0], file = sys.stderr)