# Import Splinter, BeautifulSoup, and Pandas
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import datetime as dt

def scrape_all():
# Set the executable path and initialize the chrome browser in splinter
    executable_path = {"executable_path": "C:/Users/louisz/Downloads/Projects/10. Mission-to-Mars/chromedriver.exe"}
    browser = Browser("chrome", **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser) 
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "title": hemispheres(browser)
    }

    browser.quit()
    return data

# Full Scrape function.
def mars_news(browser):
    # Visit the mars nasa news site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None
    
    return news_title, news_p
    
    # ## JPL Space Images Featured Image

def featured_image(browser):
    # Visit the NASA JPL (Jet Propulsion Laboratory) Site
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    jpl_html = browser.html
    html_soup = soup(jpl_html, 'html.parser')
    
    # Add try/except for error handling
    try:
        jTitle = html_soup.find('div', class_='SearchResultCard')
        img_url = jTitle.find('img')['data-src']
    
    except AttributeError:
        return None

    return img_url

# ## Mars Facts
def mars_facts():

    facts_url = 'http://space-facts.com/mars/'

    try:
        mars_facts = pd.read_html(facts_url)
        mars_df = mars_facts[0]

    except AttributeError:
        return None

    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)

    return mars_df.to_html()

# ## Mars Hemispheres
def hemispheres(browser): 
    main_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(main_url)

    html_hemispheres = browser.html
    hemi_soup = soup(html_hemispheres, 'html.parser')
    items = hemi_soup.find_all('div', class_='item')
    
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 
    hemis_url = []

    for urls in items:
        items = urls.find('a')['href']
        hemis_url.append(items)

    hemisphere_image_urls = []

    for i in hemis_url: 
        astro_url = hemispheres_main_url + i
        print(astro_url) 

        browser.visit(astro_url)

        html = browser.html

        img_soup = soup(html, 'html.parser')

        raw_title = img_soup.find("h2", class_="title").text
        
        # Remove ' Enhanced' tag text from each "title" via split on ' Enhanced'.
        title = raw_title.split(' Enhanced')[0]
        
        # Locate each 'full.jpg' for all 4 Hemisphere URLs.
        img_url = img_soup.find("li").a['href']
        
        # Append both title and img_url to 'hemisphere_image_url'.
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
    
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all)
