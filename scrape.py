from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

all_data = {}

def news_scrape():
    browser = init_browser()
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BeautifulSoup(news_html,'html.parser')
    news_title = news_soup.find('div', class_='content_title').text
    news_p = news_soup.find('div', class_='article_teaser_body').text
    output = [news_title, news_p]
    all_data['news_title'] = news_title
    all_data['news_paragraph'] = news_p
    return output

def img_scrape():
    browser = init_browser()
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    img_html = browser.html
    img_soup = BeautifulSoup(img_html, 'html.parser')
    search = img_soup.find('article')['style'].replace("background-image: url('/", "").replace("');", "")
    jpl_url = "https://www.jpl.nasa.gov/"
    featured_image_url = jpl_url + search
    all_data["mars_img"] = featured_image_url
    return featured_image_url

def twitter_scrape():
    browser = init_browser()
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = BeautifulSoup(twitter_html, 'html.parser')
    weather = twitter_soup.find_all('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")
    all_data["mars_weather"] = weather
    return weather

def facts_scrape():
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    facts_df = tables[0]
    facts_df.columns = ['Description', 'Value']
    facts_df.set_index('Description', inplace=True)
    mars_facts = facts_df.to_html()
    all_data["mars_facts"] = mars_facts
    return mars_facts

def hemi_scrape():
    browser = init_browser()
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html, 'html.parser')

    hemispheres = []

    sections = hemisphere_soup.find_all('div', class_='item')

    for section in sections:
        title = section.find('h3').text
        page_link = section.find('a')['href']
        hemi_site_url = "https://astrogeology.usgs.gov" + page_link
        browser.visit(hemi_site_url)
        ind_hemi_html = browser.html
        ind_hemi_soup = BeautifulSoup(ind_hemi_html, 'html.parser')
        dls = ind_hemi_soup.find('div', class_="downloads")
        hemi_img_url = dls.find('a')['href']
    
        print(title)
        print(hemi_img_url)
    
        hemispheres.append({"Title":title, "Img_URL":hemi_img_url})
    all_data["hemispheres"] = hemispheres
    return hemispheres