from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    # Mars News URL
    url = "https://mars.nasa.gov/news/"

# Retrieve page with the requests module
    html = requests.get(url)

# Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(html.text, 'html.parser')

# Establish a dictionary to store scraped information
    news_data = {}

# Get news title & paragraph description
    news_title = soup.find('div', 'content_title', 'a').get_text().strip()
    news_paragraph = soup.find('div', 'rollover_description_inner').get_text().strip()

# Add the title and description to the dictionary
    news_data["news_title"] = news_title
    news_data["news_paragraph"] = news_paragraph

    JPL_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(JPL_url) # opens up the JPL website

    JPL_html=browser.html # take out the information in html format
    JPL_soup = bs(JPL_html, 'html.parser')

# Get the featured item
    featured = JPL_soup.find('div', class_='default floating_text_area ms-layer')
    featured_image = featured.find('footer')
    featured_image_url = 'https://www.jpl.nasa.gov/' + featured_image.find('a')['data-fancybox-href']
    browser.quit()

    print(str(featured_image_url))

#mars weather url:
    mars_twitter_url = 'https://twitter.com/marswxreport?lang=en'
    mars_twitter_response = requests.get(mars_twitter_url)

# Retrieve 'mars_weather'
    mars_twitter_soup = bs(mars_twitter_response.text, 'html.parser')
    mars_twitter_result = mars_twitter_soup.find('div', class_='js-tweet-text-container')

# Assign the scraped text to a variable 'mars_weather'
    mars_weather = mars_twitter_result.find('p', class_='js-tweet-text').text
    mars_weather
    # Mars Facts Table
    mars_facts_url = 'https://space-facts.com/mars/'

    mars_facts_table = pd.read_html(mars_facts_url, index_col=0, flavor=['lxml', 'bs4'])
    mars_facts_table
    Mars_Earth_Comparison_df = mars_facts_table[0]
    Mars_Earth_Comparison_df.columns = ['Mars', 'Earth']
    Mars_Earth_Comparison_df
#Convert the data to a HTML table string.
    Mars_facts = Mars_Earth_Comparison_df.to_html()
    Mars_facts.replace("\n", "")

    Mars_Earth_Comparison_df.to_html('mars_earth_facts.html')
 #mars geology:   
    USGS_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(USGS_url)

# Retrieve the image string in html formate for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name
    USGS_html = browser.html
    USGS_soup = bs(USGS_html, 'html.parser')

    USGS_image_list = USGS_soup.find_all('div', class_='item')
    USGS_image_list
    hemispheres_title_and_image = []

    base_url ="https://astrogeology.usgs.gov" # need below

# Loop through each hemisphere and click on the link to find the large resolution image url
    for image in USGS_image_list:
        hemisphere_dict = {}
    
        href = image.find('a', class_='itemLink product-item')
        link = base_url + href['href']
        browser.visit(link)
    
        time.sleep(1)
    
        hemisphere_html_2 = browser.html
        hemisphere_soup_2 = bs(hemisphere_html_2, 'html.parser')
    
        img_title = hemisphere_soup_2.find('div', class_='content').find('h2', class_='title').text
        hemisphere_dict['title'] = img_title
    
        img_url = hemisphere_soup_2.find('div', class_='downloads').find('a')['href']
        hemisphere_dict['url_imgage'] = img_url

    # Append dictionary to hemisphere_image_urls list
        hemispheres_title_and_image.append(hemisphere_dict)


# Store data in a dictionary
    mars_data = {
        "new_data": news_data,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_table": Mars_Earth_Comparison_df,
        "hemispheres_title_and_image": hemispheres_title_and_image


    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
