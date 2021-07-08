from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    MarsNews_url = 'https://redplanetscience.com/'
    browser.visit(MarsNews_url)
    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #find the title
    news_title = soup.find("div", class_="content_title").text

    #find the paragraph
    news_paragraph = soup.find("div", class_="article_teaser_body").text




    # # JPL Mars Space Images - Featured Image

    #Visit the url for the Featured Space Image site
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    featured_image_url = image_url + soup.find("img", class_="headerimage fade-in")["src"]

    #Make sure to save a complete url string for this image.
    print(featured_image_url)


    # # Mars Facts

    #Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    fact_url = "https://galaxyfacts-mars.com/"
    browser.visit(fact_url)
    time.sleep(1)

    html = browser.html
    fact_table = pd.read_html(html)

    fact_df = fact_table[1]
    fact_df.columns =['Description', 'Value']
    


    #Use Pandas to convert the data to a HTML table string.
    html_table = fact_df.to_html(header=False)


    # # Mars Hemispheres

    #Visit the astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    time.sleep(1)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


    #You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.

    pictures = soup.find_all('div', class_='item')
    #Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.
    hemisphere_list = []
    for picture in pictures:
        
        title = picture.find('h3').text
        
        site_img = picture.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemisphere_url + site_img)
        
        site_html = browser.html
        
        soup_site = BeautifulSoup(site_html, 'html.parser')
        
        image_url = hemisphere_url + soup_site.find('img', class_='wide-image')['src']
        
        #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere
        
        hemisphere_list.append({"title": title, "image_url": image_url})

    mars_data = {
        'Title': news_title,
        'Paragraph': news_paragraph,
        'Image': featured_image_url,
        'Fact': fact_df.to_html(),
        'mars_Hemispheres': hemisphere_list}
    browser.quit()
    
    return mars_data

    
      
    

