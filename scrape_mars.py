import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path)

def scrape():
    browser = init_browser()

    ## URLS 
    url_nasa = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    url_mars_facts = 'https://space-facts.com/mars/'
    url_mars_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    ### NASA title and paragraph
    browser.visit(url_nasa)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    title_first_nasa = soup.find('div', class_='content_title').a.text
    

    paragraph_nasa = soup.find('div', class_='article_teaser_body').text

    ### JPL Image

    browser.visit(url_jpl)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    jpl_url_add = "https://www.jpl.nasa.gov"

    image = soup.find('a', "button fancybox")
    jpl_image = jpl_url_add + image['data-fancybox-href'] 

    ### Mars Weather

    browser.visit(url_twitter)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #scrap latest Mars weather tweet
    mars_weather = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

    ### Mars Facts

  
    browser.visit(url_mars_facts)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tables = pd.read_html(url_mars_facts)
    tables[0]
    df1 = pd.DataFrame(tables[0])
    df2 = df1.to_html(header = False, index = False)
    df2 
    

    ### Mars Hemispheres

   
    browser.visit(url_mars_hemi)
    html = browser.html
    soup = BeautifulSoup(html)

    title = soup.find_all('h3')
    title_cerberus = title[0].text
    title_schiaparelli = title[1].text
    title_syrtis_major = title[2].text
    title_valles_marineris = title[3].text

    browser.is_text_present('/search/map/Mars/Viking/cerberus_enhanced')
    browser.click_link_by_partial_text('Cerberus Hemisphere')

    html = browser.html
    soup = BeautifulSoup(html)

    cerberus_1 = soup.find('div', class_="downloads")
    cerberus_2 = cerberus_1.find('li')
    cerberus_pic = cerberus_2.a['href']
    
    browser.back()
    browser.is_text_present('/search/map/Mars/Viking/schiaparelli_enhanced')
    browser.click_link_by_partial_text('Schiaparelli Hemisphere')

    html = browser.html
    soup = BeautifulSoup(html)

    schiaparelli_1 = soup.find('div', class_="downloads")
    schiaparelli_2 = schiaparelli_1.find('li')
    schiaparelli_pic = schiaparelli_2.a['href']
    

    browser.back()
    browser.is_text_present('/search/map/Mars/Viking/syrtis_major_enhanced')

    browser.click_link_by_partial_text('Syrtis Major Hemisphere')

    html = browser.html
    soup = BeautifulSoup(html)

    syrtis_1 = soup.find('div', class_="downloads")
    syrtis_2 = syrtis_1.find('li')
    syrtis_pic = syrtis_2.a['href']
    
    browser.back()
    browser.is_text_present('/search/map/Mars/Viking/valles_marineris_enhanced')

    browser.click_link_by_partial_text('Valles Marineris Hemisphere')
    
    html = browser.html
    soup = BeautifulSoup(html)

    valless_1 = soup.find('div', class_="downloads")
    valless_2 = valless_1.find('li')
    valless_pic = valless_2.a['href']
    

    hemisphere_image_urls = [
    {"title": title_valles_marineris, "img_url": valless_pic},
    {"title": title_cerberus, "img_url": cerberus_pic},
    {"title": title_schiaparelli, "img_url": schiaparelli_pic},
    {"title": title_syrtis_major, "img_url": syrtis_pic},
    ]

    browser.quit()

    mars_data = {'title_first_nasa': title_first_nasa, 
                'paragraph_nasa':paragraph_nasa,
                'jpl_image':jpl_image,
                'mars_weather':mars_weather,
                'df2':df2,
                'hemisphere_image_urls':hemisphere_image_urls,
                'cerberus_pic':cerberus_pic,
                'schiaparelli_pic':schiaparelli_pic,
                'syrtis_pic':syrtis_pic,
                'valless_pic':valless_pic,
                }

    return mars_data 